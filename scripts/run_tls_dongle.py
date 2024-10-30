"""All in One script for running CAC-H TLS Proxy"""

from __future__ import print_function
import os
import sys
import time
import argparse
import logging
import platform

import ssl
import socket

from rich.logging import RichHandler
from rich.console import Console
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

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


def get_operating_platform() -> str:
    """Obtain OS information (in lowercase)"""
    return platform.platform().lower()


# TODO: Capture user choice for every command! Sync with Vitor
def ask_user(input_prompt: str) -> str:
    """Ask user a yes/no question to control the CAC-H interaction"""
    answer = Prompt.ask(input_prompt, choices=["y", "n"], default="y")
    return answer


def main():
    start_time = time.time()
    config = parse_arguments()
    
    bad_tls = ['TLSv1', 'TLSv1.1']
    os_platform = get_operating_platform()

    if config.url != "":
        create_header("CAC-H: Computer Aided Cryptography for Healthcare", "TLS Proxy Demonstration")

        with console.status(f"Assessing: {config.url}\n" , spinner="earth"):
            time.sleep(2.0)
            # check the target service for TLS version
            tls_ver = check_tls(target_host=config.url, target_port=config.port)

        if tls_ver in bad_tls:
            print(f":thumbs_down: TLS Version for {config.url} using port: {config.port} is: {tls_ver}")

            # get confirmation to proceed with TLS Proxy deployment
            answer = Prompt.ask("Deploy TLS Proxy?", choices=["y", "n"], default="y")

            if answer == "y":
                if 'macos' in os_platform:
                    # running on a macOS
                    log.info(f"Running on a MacOS!")
                    
                    # start wireshark instance listening on a desired interface
                    log.info(f"Initiating Wireshark instance...")
                    os.system("open -a wireshark.app -n")

                    # todo: open a new terminal window and run the modified TLSEraser from it
                    os.system("open -a iTerm.app -n")
                    # os.system(f"tlseraser-venv/bin/tlseraser --target {config.url}:443")
                else:
                    # running on Linux (default)
                    log.info(f"Running on Linux")

                # validate TLS use after proxy deployment
                tls_ver = check_tls(target_host='localhost', target_port=1234)
                if tls_ver in bad_tls:
                    print(f":thumbs_down: Failed to upgrade! TLS Version is: {tls_ver}")
                else:
                    print(f":thumbs_up: Success! TLS Version is: {tls_ver}")      
            else:
                print(f"Thank you for using CAC-H!")            
        else:
            print(f":thumbs_up: TLS Version for {config.url} using port: {config.port} is: {tls_ver}")



        # # start Wireshark instance listening on a desired interface
        # # todo: add interface
        # # os.system("wireshark")
        # os.system("open -a wireshark.app -n")

        # # todo: run tlseraser from the python script (note: consider running in a new terminal instance)
        # # open -a iTerm.app -n --args 'pwd'
        # os.system("open -a iTerm.app -n")
        # # os.system(f"tlseraser-venv/bin/tlseraser --target {config.url}:443")

        # # add a time delay to accommodate for changes
        # time.sleep(3.0)    

    else:
        log.error(f"Please provide a correct service path!")

    log.info(f"Execution completed in {time.time() - start_time} seconds.")


if __name__ == '__main__':
    main()