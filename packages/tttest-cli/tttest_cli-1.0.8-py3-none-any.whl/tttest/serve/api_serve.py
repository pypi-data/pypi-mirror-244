import argparse

from flask import Flask

from tttest.config.cfg import l
from tttest.version import __version__

app = Flask(__name__)


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'TtTest v{__version__}',
                        help=("显示版本号", 'display tttest version')[l.n])
    parser.add_argument('--lang', choices=['zh', 'en'],
                        help=("设置工具语言", 'set language')[l.n])

    args = parser.parse_args()
    print('serve command >> tttest is running...', args)

    # 看命令行中是否设置了语言
    if args.lang:
        l.n = l.LANGS[args.lang]


