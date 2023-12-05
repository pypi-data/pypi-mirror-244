# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aget']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.25']

entry_points = \
{'console_scripts': ['aget = aget:main']}

setup_kwargs = {
    'name': 'aget',
    'version': '0.2.0',
    'description': 'Aget - An Asynchronous Downloader',
    'long_description': '# Aget - Asynchronous Downloader\n\n[中文](https://github.com/PeterDing/aget/blob/master/README_zh.md)\n\nAget is an asynchronous downloader operated in command-line, running on Python > 3.5.\n\nIt supports HTTP(S), using [httpx](https://github.com/encode/httpx) request library.\n\nAget continues downloading a partially downloaded file as default.\n\n### Installion\n\n```shell\n$ pip3 install aget\n```\n\n### Usage\n\n```shell\naget https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png\n\n# get an output name\naget https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png -o \'google.png\'\n\n# set headers\naget https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png -H "User-Agent: Mozilla/5.0" -H "Accept-Encoding: gzip"\n\n# set concurrency\naget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.9.tar.xz -s 10\n\n# set request range size\naget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.9.tar.xz -k 1M\n```\n\n### Options\n\n```shell\n-o OUT, --out OUT             # output path\n-H HEADER, --header HEADER    # request header\n-X METHOD, --method METHOD    # request method\n-d DATA, --data DATA          # request data\n-t TIMEOUT, --timeout TIMEOUT # timeout\n-s CONCURRENCY, --concurrency CONCURRENCY   # concurrency\n-k CHUCK_SIZE, --chuck_size CHUCK_SIZE      # request range size\n```\n\n### For Developer\n\n#### logging\n\nUse environment variable `AGET_LOG_LEVEL` to setting logging level.  \nThe default level is `CRITICAL`.\n',
    'author': 'PeterDing',
    'author_email': 'dfhayst@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PeterDing/aget',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
