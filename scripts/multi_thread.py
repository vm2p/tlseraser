import argparse
import socket
import logging
import os

level = logging.getLevelName(logging.INFO)
logging.basicConfig(level=level)
log = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", 
                        type=str, 
                        default="", 
                        dest="TARGET",
                        help="the targets service as <HOST1>:<PORT1>,<HOST2>:<PORT2>:...:<HOSTN>:<PORTN>")     

    args = parser.parse_args()
    return args

def get_port():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1]


def tlseraser_run(lport, lhost, target, netns_name):
    TLSEraser(
                lport,
                lhost,
                target=target,
                netns_name=netns_name,
            ).run()

def main():
    args = parse_arguments()
    ts_split = args.TARGET.split(',')
    if (len(ts_split) > 71338):
        log.info('Too many targets! TLSEraser only supports 142676 targets. Aborting...') 
        return

    try:
        for target in ts_split:
            port = get_port()
            log.info(f"Deploying TLS Proxy for {target}...")
            os.system(f"gnome-terminal --tab --title=CACH-TLSProxy-{target} -- sudo tlseraser-venv/bin/tlseraser --target {target} -p {port} &")  
    except KeyboardInterrupt:
        print('\r', end='')  # prevent '^C' on console
        log.info('Caught Ctrl-C, exiting...')

if __name__ == '__main__':
    main()