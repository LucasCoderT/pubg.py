from setuptools import setup
import os
import re

try:
    import pypandoc

    description = pypandoc.convert("README.md", "rst")
except (IOError, ImportError):
    description = "wrapper for https://pubgtracker.com/site-api api using aiohttp"

on_rtd = os.getenv('READTHEDOCS') == 'True'

requirements = ["aiohttp>=2.2.3"]

if on_rtd:
    requirements.append('sphinxcontrib-napoleon')
    requirements.append('sphinxcontrib-asyncio')

version = ''
with open('pubg/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

setup(
    name='pubg.py',
    version=version,
    packages=['pubg'],
    python_requires='>=3.4.2',
    url='https://github.com/datmellow/pubg.py',
    license='MIT',
    author='datmellow',
    install_requires=requirements,
    author_email='',
    description='wrapper for https://pubgtracker.com/site-api api using aiohttp'
)
