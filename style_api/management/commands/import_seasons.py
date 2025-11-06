from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

import json
import os

from style_api.models import Season


class Command(BaseCommand):
    help = 'Import seasons from JSON file into Season model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=None,
            help='Path to the JSON file containing seasons data (default: seasons.json)'    # noqa
        )

    def handle(self, *args, **options):
        file_path = options['file']

        if file_path is None:
            base_dir = settings.BASE_DIR
            file_path = os.path.join(base_dir, 'resources', 'seasons.json')

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
        if not isinstance(data, dict) or 'seasons' not in data:
            self.stdout.write(
                self.style.ERROR(
                    'Invalid data structure. Expected {"seasons": [...]}')
            )
            return

        seasons_data = data['seasons']

        if not isinstance(seasons_data, list):
            self.stdout.write(
                self.style.ERROR('seasons must be a list')
            )
            return

        # Import seasons
        created_count = 0
        skipped_count = 0
        error_count = 0

        self.stdout.write(
            self.style.WARNING(f'Processing {len(seasons_data)} seasons...\n')
        )

        with transaction.atomic():
            for index, season_data in enumerate(seasons_data, 1):
                try:
                    # Validate required fields
                    if 'name' not in season_data:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  [{index}] Missing required field: name')
                        )
                        error_count += 1
                        continue

                    name = season_data['name']
                    code = season_data.get('code', '')
                    order = season_data.get('order', 0)
                    description = season_data.get('description', '')

                    # Check if season already exists
                    if Season.objects.filter(name=name).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'  [{index}] Skipped: {name} (already exists)')    # noqa
                        )
                        skipped_count += 1
                        continue

                    # Check if code already exists (if code is provided)
                    if code and Season.objects.filter(code=code).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'  [{index}] Skipped: {name} (code "{code}" already exists)'   # noqa
                            )
                        )
                        skipped_count += 1
                        continue

                    # Create season
                    season = Season.objects.create(
                        name=name,
                        code=code,
                        order=order,
                        description=description
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  [{index}] Created: {season.name}')
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
