import argparse
import logging
import sys
from pyPackage import Package, Options
from pyBaseApp import Configuration

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='create a default app with package feature')
    parser.add_argument(
        'package', help='package the app thanks to package.yml settings available from project root')
    args = parser.parse_args()

    if not args.package:
        parser.print_help(sys.stderr)
        sys.exit(1)

    settings = Configuration().settings('package.yml')
    if not settings:
        logging.error('please supply a valid package.yml file in root folder')
        sys.exit(1)

    data = settings['data'] if 'data' in settings else None

    try:
        options = Options(settings)
        Package(options, data)
    except ValueError:
        logging.error('package value is missing in settings')
