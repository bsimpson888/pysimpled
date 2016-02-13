from distutils.core import setup

setup(
    name='pysimpled',
    version='1.0.0',
    package_dir={'pysimpled': "sources/pysimpled"},
    packages=['pysimpled'],
    url='https://github.com/bsimpson888/pysimpled',
    license='Apache License',
    author='Marco Bartel',
    author_email='bsimpson888@gmail.com',
    description='Simple to use context managers for server side scripts like daemons'
)
