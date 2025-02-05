#!/usr/bin/env python3
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

import argparse
import logging
log = logging.getLogger(__name__)

_LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

parser = argparse.ArgumentParser(
    description="Terminate TLS encrpytion and mirror the clear text traffic "
                "on another device"
)

parser.add_argument(
    '-p',
    '--lport',
    default=1234,
    dest="LPORT",
    type=int,
    help="the local port to listen on (default: 1234)"
)

parser.add_argument(
    '-l',
    '--lhost',
    default="0.0.0.0",
    dest="LHOST",
    type=str,
    help="the IP address to listen on (default: 0.0.0.0)"
)

parser.add_argument(
    '-m',
    '--mirror-subnet',
    default="192.168.253",
    dest="MIRROR_SUBNET",
    type=str,
    help="the IP subnet of the pcap mirror (default: %(default)s)"
)

parser.add_argument(
    '-n',
    '--netns-name',
    default="mirror",
    dest="NETNS_NAME",
    type=str,
    help="the name of the mirror network namespace (default: %(default)s)"
)

parser.add_argument(
    '-f',
    '--forwarder',
    default="default",
    dest="FORWARDER",
    choices=['default', 'flipper'],
    type=str,
    help="The Forwarder module to use (default: %(default)s)"
)

parser.add_argument(
    '-t',
    '--target',
    dest="TARGET",
    default=None,
    type=str,
    help='the target service as <HOST>:<IP>; if none is given '
    '(the default), the original destination of NATed TCP packets is '
    'determined via SO_ORIGINAL_DST',
)

parser.add_argument(
    '--log-level',
    dest="LOG_LEVEL",
    default='INFO',
    type=str,
    choices=_LOG_LEVEL_STRINGS,
    help='the logging level (default: %(default)s)',
)

args = parser.parse_args()