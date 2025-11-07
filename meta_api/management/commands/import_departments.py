from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

import json
import os

from meta_api.models import Department


class Command(BaseCommand):
    help = 'Import departments from JSON file into Department model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=None,
            help='Path to the JSON file containing departments data (default: departments.json)'    # noqa
        )

    def handle(self, *args, **options):
        file_path = options['file']

        if file_path is None:
            base_dir = settings.BASE_DIR
            file_path = os.path.join(base_dir, 'resources', 'departments.json')

        # Check if file exists
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File not found: {file_path}')
            )
            return

        # Read JSON file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON format: {e}')
            )
            return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading file: {e}')
            )
            return

        # Validate data structure
        if not isinstance(data, dict) or 'departments' not in data:
            self.stdout.write(
                self.style.ERROR(
                    'Invalid data structure. Expected {"departments": [...]}')
            )
            return

        departments_data = data['departments']

        if not isinstance(departments_data, list):
            self.stdout.write(
                self.style.ERROR('departments must be a list')
            )
            return

        # Import departments
        created_count = 0
        skipped_count = 0
        error_count = 0

        self.stdout.write(
            self.style.WARNING(
                f'Processing {len(departments_data)} departments...\n')
        )

        with transaction.atomic():
            for index, department_data in enumerate(departments_data, 1):
                try:
                    # Validate required fields
                    if 'name' not in department_data:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [{index}] Missing required field: name')
                        )
                        error_count += 1
                        continue

                    name = department_data['name']
                    description = department_data.get('description', '')

                    # Check if department already exists
                    if Department.objects.filter(name=name).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'  [{index}] Skipped: {name} (already exists)')    # noqa
                        )
                        skipped_count += 1
                        continue

                    # Create department
                    department = Department.objects.create(
                        name=name,
                        description=description
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  [{index}] Created: {department.name}')
                    )
                    created_count += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  [{index}] Error: {str(e)}')
                    )
                    error_count += 1

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Import completed!'))
        self.stdout.write(f'  Created: {created_count}')
        self.stdout.write(f'  Skipped: {skipped_count}')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  Errors: {error_count}'))
        self.stdout.write('='*50)
