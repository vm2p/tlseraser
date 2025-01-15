#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Copyright (c) 2019 Adrian Vollmer
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the
#  "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to permit
#  persons to whom the Software is furnished to do so, subject to the
#  following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
#  NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#  USE OR OTHER DEALINGS IN THE SOFTWARE.


def main():
    from tlseraser.tlseraser import TLSEraser
    from tlseraser.args import args

    import logging

    level = logging.getLevelName(args.LOG_LEVEL)
    logging.basicConfig(level=level)
    log = logging.getLogger(__name__)

    try:
        print(args.LPORT, args.LHOST, args.TARGET, args.NETNS_NAME,)
        TLSEraser(
            args.LPORT,
            args.LHOST,
            target=args.TARGET,
            netns_name=args.NETNS_NAME,
        ).run()
    except KeyboardInterrupt:
        print('\r', end='')  # prevent '^C' on console
        log.info('Caught Ctrl-C, exiting...')


if __name__ == '__main__':
    main()