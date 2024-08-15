from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='webwindow',
    version='1.2.1',
    py_modules=['webwindow'],
    license='MIT',
    platforms=['web'],
    description='WebGL Window',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Szabolcs Dombi',
    author_email='szabolcs@szabolcsdombi.com',
    url='https://github.com/szabolcsdombi/webwindow/',
    project_urls={
        'Source': 'https://github.com/szabolcsdombi/webwindow/',
        'Bug Tracker': 'https://github.com/szabolcsdombi/webwindow/issues/',
    },
    keywords=[
        'WebGL',
        'window',
    ],
)
