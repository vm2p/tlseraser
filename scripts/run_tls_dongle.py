"""All in One script for running CAC-H TLS Proxy"""

from __future__ import print_function
import os
import sys
import argparse
import time
import logging

import ssl
import socket

from rich.logging import RichHandler
from rich.console import Console
from rich import print
from rich.panel import Panel

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

log = logging.getLogger("rich")


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--url", 
                        type=str, 
                        default="", 
                        help="target test service")
    
    parser.add_argument("-p", "--port", 
                        type=int, 
                        default=443, 
                        help="target port")    

    args = parser.parse_args()
    return args


def create_header(title, subtitle=""):
    """Creates a stylized program header using Rich library.
       BH note: AI inspired!
    """

    header = Panel(
        f"[bold green]{title}[/]\n[italic]{subtitle}[/]",
        title_align="center",
        border_style="none",
        padding=(0, 0),
    )
    console.print(header)


def check_tls(target_host: str, target_port: int) -> str:
    """Modifications done to work with IP addresses"""

    tls_version = ""
    context = ssl.create_default_context()

    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((target_host, target_port))
        with context.wrap_socket(sock, server_hostname=target_host) as ssock:
            tls_version = ssock.version()
    
    sock.close()

    return tls_version


def main():
    start_time = time.time()
    config = parse_arguments()
    
    bad_tls = ['TLSv1.0', 'TLSv1.1']

    if config.url != "":
        create_header("CAC-H: Computer Aided Cryptography for Healthcare", "TLS Proxy Demonstration")

        with console.status(f"Assessing: {config.url}\n" , spinner="earth"):
            time.sleep(2.0)
        
        # check the target service for TLS version
        tls_ver = check_tls(target_host=config.url, target_port=config.port)
        if tls_ver in bad_tls:
            print(f":thumbs_down: TLS Version for {config.url} using port: {config.port} is: {tls_ver}")
        else:
            print(f":thumbs_up: TLS Version for {config.url} using port: {config.port} is: {tls_ver}")

        # todo: start Wireshark instance listening on a desired port

        # todo: run tlseraser from the python script (note: consider running in a new terminal instance)

        # add a time delay to accommodate for changes

        # todo: validate the TLS version again

    else:
        log.error(f"Please provide a correct service path!")

    log.info(f"Execution completed in {time.time() - start_time} seconds.")


if __name__ == '__main__':
    main()