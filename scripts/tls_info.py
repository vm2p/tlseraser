"""Extract TLS info from a given Website URL

Sample run:
  python scripts/tls_info.py -u sri.com -p 443

Returns:
    TLS Version for sri.com using port: 443 is: TLSv1.2
    Certificate details:
    {
        'subject': ((('commonName', 'sri.com'),),),
        'issuer': ((('countryName', 'US'),), (('organizationName', "Let's Encrypt"),), (('commonName', 'R11'),)),
        'version': 3,
        'serialNumber': '041C634574298E9DA79BABE1146D27212AB2',
        'notBefore': 'Sep 22 08:23:21 2024 GMT',
        'notAfter': 'Dec 21 08:23:20 2024 GMT',
        'subjectAltName': (('DNS', 'sri.com'),),
        'OCSP': ('http://r11.o.lencr.org',),
        'caIssuers': ('http://r11.i.lencr.org/',)
    }
"""

from __future__ import print_function
import os
import sys
import argparse
import time
import logging

import ssl
import socket

from rich.logging import RichHandler
from rich import print

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


def check_tls(target_host: str, target_port: int) -> str:
    """Based on: https://medium.com/@sotiraq.sima/how-to-check-the-tls-of-your-website-with-python-1931a8abcf8e"""

    tls_version = ""
    cert_info = ""
    context = ssl.create_default_context()
    with socket.create_connection((target_host, target_port)) as sock:
        with context.wrap_socket(sock, server_hostname=target_host) as ssock:
            tls_version = ssock.version()
            cert_info = ssock.getpeercert()
    
    sock.close()

    return tls_version, cert_info


def main():
    start_time = time.time()
    config = parse_arguments()
    
    if config.url != "":
        log.info(f"Assessing: {config.url}")

        tls_ver, ssl_cert_data = check_tls(target_host=config.url, target_port=config.port)
        print(f"TLS Version for {config.url} using port: {config.port} is: {tls_ver}")
        print(f"Certificate details:")
        print(ssl_cert_data)
    else:
        log.error(f"Please provide a correct service path!")

    log.info(f"Execution completed in {time.time() - start_time} seconds.")


if __name__ == '__main__':
    main()