#!/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    if not 'RUN_MAIN' in os.environ:
        print '''\
;-.                            .
|  )               o           |
|-'  ;-. ,-. ;-.-. . ,-. ,-.   | . .
|    |   | | | | | | `-. |-'   | | |
'    '   `-' ' ' ' ' `-' `-' o ' `-|
                                 `-' '''
    execute_from_command_line(sys.argv)
