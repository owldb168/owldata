from setuptools import setup

with open('requirements.txt') as fid:
    requires = [line.strip() for line in fid]

setup(
    name = 'owl_api',
    version = '0.0.1',
    description = 'Testing version for owl',
    author = 'CMoney Corp.',
    author_email = 'danny657031@gmail.com',
    # install_requires = ['pandas', 'requests'],
    install_requires = requires,
    url = 'https://owl.cmoney.com.tw/Owl/',
    packages = ['owl_api']
)
