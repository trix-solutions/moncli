try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'Moncli, a pythonic/DDD client for Monday.com',
    'author': 'Andrew Shatz, Trix Solutions',
    'url': r'https://github.com/trix-solutions/moncli',
    'download_url': r'https://github.com/trix-solutions/moncli',
    'author_email': 'andrew.shatz@trix.solutions',
    'version': '0.1.6',
    'install_requires': [
        'requests>=2.22.0'
    ],
    'tests_require': [
        'nose>=1.3.7'
    ],
    'packages': [
        'moncli',
        'moncli.api_v1',
        'moncli.api_v2',
        'moncli.entities'
    ],    
    'scripts': [],
    'name': 'moncli'
}

setup(**config)
