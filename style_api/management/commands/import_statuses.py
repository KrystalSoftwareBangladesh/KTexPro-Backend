from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

import json
import os

from style_api.models import StyleStatus


class Command(BaseCommand):
    help = 'Import style statuses from JSON file into StyleStatus model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=None,
            help='Path to the JSON file containing style statuses data (default: resources/statuses.json)'    # noqa
        )

    def handle(self, *args, **options):
        file_path = options['file']

        # Use default path if not provided
        if file_path is None:
            # Get project root directory (where manage.py is located)
            base_dir = settings.BASE_DIR
            file_path = os.path.join(
                base_dir, 'resources', 'statuses.json')

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
        if not isinstance(data, dict) or 'style_statuses' not in data:
            self.stdout.write(
                self.style.ERROR(
                    'Invalid data structure. Expected {"style_statuses": [...]}')           # noqa
            )
            return

        statuses_data = data['style_statuses']

        if not isinstance(statuses_data, list):
            self.stdout.write(
                self.style.ERROR('style_statuses must be a list')
            )
            return

        # Import statuses in two passes: first parents, then children
        created_count = 0
        skipped_count = 0
        error_count = 0

        self.stdout.write(
            self.style.WARNING(
                f'Processing {len(statuses_data)} style statuses...\n')
        )

        # Separate parent and child statuses
        parent_statuses = [s for s in statuses_data if s.get('parent') is None]
        child_statuses = [
            s for s in statuses_data if s.get('parent') is not None]

        self.stdout.write(
            self.style.WARNING(
                f'Found {len(parent_statuses)} parent statuses and {len(child_statuses)} child statuses\n')     # noqa
        )

        with transaction.atomic():
            # First pass: Create parent statuses
            self.stdout.write(self.style.SUCCESS(
                '=== Creating Parent Statuses ==='))
            for index, status_data in enumerate(parent_statuses, 1):
                try:
                    # Validate required fields
                    if 'name' not in status_data or 'code' not in status_data:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [{index}] Missing required field: name or code')        # noqa
                        )
                        error_count += 1
                        continue

                    name = status_data['name']
                    code = status_data['code']
                    order = status_data.get('order', 0)
                    is_active = status_data.get('is_active', True)
                    description = status_data.get('description', '')
                    color = status_data.get('color', '')

                    # Check if status already exists
                    if StyleStatus.objects.filter(code=code).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'  [{index}] Skipped: {name} (code "{code}" already exists)')      # noqa
                        )
                        skipped_count += 1
                        continue

                    # Create parent status
                    status = StyleStatus.objects.create(
                        name=name,
                        code=code,
                        parent=None,
                        order=order,
                        is_active=is_active,
                        description=description,
                        color=color
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  [{index}] Created Parent: {status.name} ({status.code})')       # noqa
                    )
                    created_count += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  [{index}] Error: {str(e)}')
                    )
                    error_count += 1

            # Second pass: Create child statuses
            self.stdout.write(
                '\n' + self.style.SUCCESS('=== Creating Child Statuses ==='))
            for index, status_data in enumerate(child_statuses, 1):
                try:
                    # Validate required fields
                    if 'name' not in status_data or 'code' not in status_data or 'parent' not in status_data:       # noqa
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [{index}] Missing required field: name, code, or parent')                       # noqa
                        )
                        error_count += 1
                        continue

                    name = status_data['name']
                    code = status_data['code']
                    parent_code = status_data['parent']
                    order = status_data.get('order', 0)
                    is_active = status_data.get('is_active', True)
                    description = status_data.get('description', '')
                    color = status_data.get('color', '')

                    # Check if status already exists
                    if StyleStatus.objects.filter(code=code).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'  [{index}] Skipped: {name} (code "{code}" already exists)')      # noqa
                        )
                        skipped_count += 1
                        continue

                    # Find parent status
                    try:
                        parent_status = StyleStatus.objects.get(
                            code=parent_code)
                    except StyleStatus.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [{index}] Error: Parent status with code "{parent_code}" not found for {name}')     # noqa
                        )
                        error_count += 1
                        continue

                    # Create child status
                    status = StyleStatus.objects.create(
                        name=name,
                        code=code,
                        parent=parent_status,
                        order=order,
                        is_active=is_active,
                        description=description,
                        color=color
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  [{index}] Created Child: {parent_status.name} > {status.name} ({status.code})')         # noqa
                    )
                    created_count += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'  [{index}] Error: {str(e)}')
                    )
                    error_count += 1

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Import completed!'))
        self.stdout.write(f'  Total in file: {len(statuses_data)}')
        self.stdout.write(self.style.SUCCESS(f'  Created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'  Skipped: {skipped_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  Errors: {error_count}'))
        self.stdout.write('='*60)

        # Show summary by parent
        if created_count > 0:
            self.stdout.write(
                '\n' + self.style.SUCCESS('=== Status Summary by Parent ==='))
            parent_statuses_obj = StyleStatus.objects.filter(
                parent=None).order_by('order')
            for parent in parent_statuses_obj:
                child_count = parent.children.count()
                self.stdout.write(
                    f'  {parent.name} ({parent.code}): {child_count} sub-status(es)')               # noqa
