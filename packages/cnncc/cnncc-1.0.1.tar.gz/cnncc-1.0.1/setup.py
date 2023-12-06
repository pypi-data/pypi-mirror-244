from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cnncc',
    version='1.0.1',
    packages=find_packages(),
    description='A simple CNN for cell-cycle phase classification',
    author='F.Dumoncel, E.Billard, S. Boudouh',
    install_requires=required,
    package_data={
        'cnncc': ['models/resnet/*.pt', 'models/resnet/*.pth'],
    },
    entry_points={
        'console_scripts': [
            'cnncc = cnncc:main',
            'cnncc-dalil = cnncc:test'
        ]
    }
)