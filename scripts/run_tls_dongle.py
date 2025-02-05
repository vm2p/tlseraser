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
    
    parser.add_argument("-l", "--lport", 
                        type=int, 
                        default=1234, 
                        help="local port")        

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

        exit = False
        while (True):

            with console.status(f"Assessing: {config.url}\n" , spinner="earth"):            
                # check the target service for TLS version
                tls_ver = check_tls(target_host=config.url, target_port=config.port)
                time.sleep(2.0)

            if tls_ver in bad_tls:
                print(f":thumbs_down: TLS Version for {config.url} using port: {config.port} is: {tls_ver}")
                print(f":x: Your connection to this website uses weak encryption and is not private. Other users can view your information or modify the website's behavior.")

                # get confirmation to proceed with TLS Proxy deployment
                answer = ask_user(input_prompt="Deploy TLS Proxy?")

                if answer == "y":
                    if 'macos' in os_platform:
                        # running on a macOS
                        log.info(f"Running on a MacOS!")
                        
                        # start wireshark instance listening on a desired interface
                        log.info(f"Initiating Wireshark instance...")
                        os.system("open -a wireshark.app -n")

                        # todo: open a new terminal window and run the modified TLSEraser from it
                        log.info(f"Deploying TLS Proxy...")
                        os.system("open -a iTerm.app -n")
                        # os.system(f"tlseraser-venv/bin/tlseraser --target {config.url}:443")
                    else:
                        # running on Linux (default)
                        log.info(f"Running on Linux")

                        # todo: open a new terminal window and run the modified TLSEraser from it
                        log.info(f"Deploying TLS Proxy...")
                        os.system(f"gnome-terminal --tab --title=CACH-TLSProxy -- sudo tlseraser-venv/bin/tlseraser --target {config.url}:{config.port} -p {config.lport} &")  
                        
                        # start wireshark instance listening on a desired interface
                        answer = ask_user(input_prompt="Do you want to monitor via Wireshark")
                        if answer == "y":
                            log.info(f"Initiating Wireshark instance...")
                            os.system("gnome-terminal --tab --title=Wireshark-Instance -- sudo wireshark -i any -k")                        

                    time.sleep(5.0)
                    # validate TLS use after proxy deployment
                    answer = ask_user(input_prompt="Re-assess TLS version?")
                    if answer == "y":
                        tls_ver = check_tls(target_host='localhost', target_port=config.lport)
                        if tls_ver in bad_tls:
                            print(f":thumbs_down: Failed to upgrade! TLS Version is: {tls_ver}")
                        else:
                            print(f":thumbs_up: Success! TLS Version is: {tls_ver}")
                            print(f":white_check_mark: The website you are viewing was encrypted before being transmited over the Internet.")  

                    answer = ask_user(input_prompt="End CACH-TLSProxy?")
                    if answer == "y":
                        os.system(f"pkill -P $$ --signal 9") 
                        break
                else:
                    print(f"Thank you for using CAC-H!")
                    os.system(f"pkill -P $$ --signal 9") 
                    break
            else:
                print(f":thumbs_up: TLS Version for {config.url} using port: {config.port} is: {tls_ver}")  
                print(f":white_check_mark: The website you are viewing was encrypted before being transmited over the Internet.")
                break
    else:
        log.error(f"Please provide a correct service path!")

    log.info(f"Execution completed in {time.time() - start_time} seconds.")


if __name__ == '__main__':
    main()