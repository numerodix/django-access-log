from os.path import dirname
from os.path import join
from setuptools import find_packages
from setuptools import setup


setup(
    name='django-access-log',
    version='0.1',
    description='Simple traffic analysis',
    long_description=open('README.md').read(),
    author='Martin Matusiak',
    author_email='numerodix@gmail.com',
    url='https://github.com/numerodix/django-access-log',
    download_url='https://github.com/numerodix/django-access-log',
    license='GPL',
    install_requires=open(join(dirname(__file__), 'requirements.txt')).read(),
)
