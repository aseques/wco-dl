#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import platform
from Lifter import *
from version import __version__


class Main():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='wco-dl downloads shows from wcostream.com')

        parser.add_argument('--version', action='store_true', help='Shows version and exits.')

        required_args = parser.add_argument_group('Required Arguments :')
        required_args.add_argument('-i', '--input', nargs=1, help='Inputs the URL to show.')
        parser.add_argument('-hd', '--highdef', help='If you wish to get 720p', action="store_true")
        parser.add_argument('-rn', '--range', nargs=1, help='Specifies the range of episodes to download.',
                            default='All')
        parser.add_argument('-o', '--output', nargs=1, help='Specifies the directory of which to save the files.')
        parser.add_argument("-v", "--verbose", help="Prints important debugging messages on screen.",
                            action="store_true")
        logger = "False"
        args = parser.parse_args()

        if args.verbose:
            logging.basicConfig(format='%(levelname)s: %(message)s', filename="Error Log.log", level=logging.DEBUG)
            logging.debug('You have successfully set the Debugging On.')
            logging.debug("Arguments Provided : {0}".format(args))
            logging.debug(
                "Operating System : {0} - {1} - {2}".format(platform.system(), platform.release(), platform.version()))
            logging.debug("Python Version : {0} ({1})".format(platform.python_version(), platform.architecture()[0]))
            logger = "True"

        if args.version:
            print("Current Version : {0}".format(__version__))
            exit()

        if args.highdef:
            args.highdef = '720'
        else:
            args.highdef = '480'

        if args.input is None:
            print("Please enter the required argument. Run __main__.py --help")
            exit()
        else:
            if type(args.range) == list:
                args.range = args.range[0]
            if type(args.output) == list:
                args.output = args.output[0]

            Lifter(url=args.input[0], resolution=args.highdef, logger=logger, ep_range=args.range,
                   output=args.output)
