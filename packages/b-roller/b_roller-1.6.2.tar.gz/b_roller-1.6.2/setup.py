# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'pytube'}

packages = \
['b_roller', 'b_roller.fonts', 'pytube', 'pytube.contrib']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0',
 'pillow>=10.1.0,<11.0.0',
 'python-slugify',
 'requests',
 'rich>=13.5.2,<14.0.0',
 'typer',
 'urllib3<=2']

entry_points = \
{'console_scripts': ['broll = b_roller.__main__:app']}

setup_kwargs = {
    'name': 'b-roller',
    'version': '1.6.2',
    'description': 'Download resources from several sources across the web',
    'long_description': '# B-Roller\n\nDownload B-roll footage from YouTube **for fair use purposes**.\n\n## Usage\n\n### Download from YouTube\n\n```\nbroll yt [OPTIONS] URL [START] [END]\n\n  Download content from YouTube\n\nArguments:\n  URL      A video id or a YouTube short/long url  [required]\n  [START]  The desired start of the video in seconds or the format 00:00:00\n  [END]    The desired end of the video in seconds or the format 00:00:00\n```\n\nFor example:\n\n```shell\nbroll yt "https://www.youtube.com/watch?v=QFLiIU8g-R0" 00:10 00:17\n```\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
