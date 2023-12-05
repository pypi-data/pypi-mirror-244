from setuptools import setup, find_packages

setup(
    name='transferability_metric',
    version='0.1',
    author='Enming Zhang',
    author_email='1229454906@qq.com',
    description='My Python Package',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
    ]
)
