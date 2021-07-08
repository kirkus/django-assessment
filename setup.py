from os.path import join
from setuptools import setup, find_packages


def get_version():
    with open(join('django_assessment', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')


setup(
    name='django-assessment',
    version=get_version(),
    description="Assessment model fields for Django",
    long_description=open('README.md').read(),
    author='Kirkus Reviews',
    author_email='kirkus-dev@kirkus.com',
    url='https://github.com/kirkus/django-assessment/',
    license='',
    packages=find_packages(),
    install_requires=['Django>=1.8.11'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
