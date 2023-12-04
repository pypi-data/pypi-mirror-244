from setuptools import setup

setup(
    name='mbd-formatter',
    version='1.0.0',
    author='maberdeb',
    author_email='maxime@maberdeb.com',
    description='a formater for print',
    packages=['mbd_formatter'],  # Replace 'your_module' with your actual module name
    install_requires=[
        'colorama',
        'ntplib'
    ],  # Add any dependencies required for your module
)
