import argparse
import socket

import psutil
from flask import Flask

from tttest.config.cfg import l
from tttest.version import __version__

app = Flask(__name__)


@app.route('/test')
def handle_test():
    return 'tttest is running!!'


def mock():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'TtTest v{__version__}',
                        help=("显示版本号", 'display tttest version')[l.n])
    parser.add_argument('--lang', choices=['zh', 'en'],
                        help=("设置工具语言", 'set language')[l.n])
    parser.add_argument('--port', default=9528, type=int,
                        help=("设置启动mock服务端口默认9527", 'set mock serve port,default 9528')[l.n])
    parser.add_argument('--debug', default=False, type=bool,
                        help=("设置启动mock服务debug模式", 'set mock serve debug mode')[l.n])
    parser.add_argument('--start', action='store_true',
                        help=("启动mock服务", 'start mock serve')[l.n])
    parser.add_argument('--stop', action='store_true',
                        help=("停止mock服务", 'stop mock serve')[l.n])

    args = parser.parse_args()

    # 看命令行中是否设置了语言
    if args.lang:
        l.n = l.LANGS[args.lang]

    if args.start:
        start_flask(args)

    if args.stop:
        shutdown_flask(args)


def start_flask(args):
    run(args)

    # process = multiprocessing.Process(target=run, args=(args,), name=threadName)
    # process.start()

    # thread = threading.Thread(target=run, args=(args,), name=threadName)
    # thread.start()
    # if not thread.is_alive():
    #     raise RuntimeError("Failed to start thread")


def shutdown_flask(args):
    print('关闭中...')
    for conn in psutil.net_connections():
        if conn.laddr.port == args.port and conn.status == 'LISTEN':
            p = psutil.Process(conn.pid)
            p.terminate()
            print('关闭完成')


def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0


def run(args):
    if check_port(args.port):
        print(f'Port {args.port} is in use, web server will not start.')
    else:
        print(f'Starting web server on port {args.port}')
        app.run(port=args.port, debug=args.debug)
