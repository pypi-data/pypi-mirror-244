import setuptools
from pathlib import Path


def get_install_requirements():
    """
    Extract packages from requirements.txt file to list

    Returns:
        list: list of packages
    """
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setuptools.setup(name='opsys-relay-controller',
                 version='0.0.2',
                 description='python package for relay device control',
                 url='https://bitbucket.org/opsys_tech/opsys-relay-controller/src/master/',
                 download_url='https://bitbucket.org/opsys_tech/opsys-relay-controller/src/master/',
                 author='dmitry.borovensky',
                 install_requires=get_install_requirements(),
                 author_email='dmitry.borovensky@opsys-tech.com',
                 packages=setuptools.find_packages(),
                 zip_safe=False)