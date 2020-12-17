import logging
import argparse
import traceback
from pyBaseApp import Configuration, error
from datetime import datetime

if __name__ == "__main__":
    print('launching app...')
    parser = argparse.ArgumentParser(description='This is a wonderful app...')
    parser.add_argument('-l', '--log', help='define log folder path')
    parser.add_argument('-s', '--settings', help='indicates settings file path')
    args = parser.parse_args()

    settings_file = args.settings if args.settings else __file__
    conf = Configuration(args.log) if args.log else Configuration()
    settings = conf.settings(settings_file)

    # create Timestamp of current execution
    now = datetime.utcnow()
    logging.info('execution launched {} UTC'.format(now))

    try:
        logging.info(settings['message'])
    except:
        e = traceback.format_exc()
        error('message printing failed: {}'.format(e))