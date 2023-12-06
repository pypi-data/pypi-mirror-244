"""exampleLSPServer package."""

#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import logging
import \
    os

from .server import example_server

# TODO debug
from pprint import pprint
if "." in __name__:
    pprint(f'.{__name__}')
else:
    pprint(__name__)

logging.basicConfig(filename="exampleDSL_pygls.log", level=logging.DEBUG, filemode="w")


def add_arguments(parser):
    parser.description = "dsl server example"

    parser.add_argument(
        "--tcp", action="store_true",
        help="Use TCP server"
    )
    parser.add_argument(
        "--ws", action="store_true",
        help="Use WebSocket server"
    )
    parser.add_argument(
        "--host", default="127.0.0.1",
        help="Bind to this address"
    )
    parser.add_argument(
        "--port", type=int, default=2087,
        help="Bind to this port"
    )
    parser.add_argument(
            "-f", "--file", dest="file", type=file_path, default="some_file",
            help="Path to file"
    )


def file_path(path: str):
    """
    Check for valid file path.

    :param path: readable file path
    :return: valid path
    """
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable path:'{path}' is not a valid path")


def main():
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    if args.tcp:
        example_server.start_tcp(args.host, args.port)
    elif args.ws:
        example_server.start_ws(args.host, args.port)
    else:
        example_server.start_io()


if __name__ == '__main__':
    main()
