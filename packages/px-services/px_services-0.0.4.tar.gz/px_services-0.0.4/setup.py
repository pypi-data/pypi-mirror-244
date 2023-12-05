from setuptools import setup, find_packages

classifiers = [
'Development Status :: 2 - Pre-Alpha',
'Intended Audience :: Developers',
'Environment :: Console',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3',
'Topic :: Software Development',
'Topic :: Utilities',
]

setup(
name='px_services',
version='0.0.4',
description='A blockchain Wallet Service APIs',
long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
url='',
author= 'Prince Foli',
author_email='princefoli@qodehub.com',
license= 'MIT',
classifiers=classifiers,
keywords='Blockchain, Wallet, HDWallet, BlockCypher',
packages=find_packages(),
install_requires=['blockcypher','bitcoinlib']
)