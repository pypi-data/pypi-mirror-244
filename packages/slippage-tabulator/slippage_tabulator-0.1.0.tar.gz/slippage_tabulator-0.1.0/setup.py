from setuptools import setup, find_packages

setup(
    name='slippage_tabulator',
    version='0.1.0',
    url='https://github.com/davidthegardens/slippage_tabulator.git',
    author='David Desjardins',
    author_email='david@shield3.com',
    description='Get the slippage from the uniswap universal router before execution.',
    packages=find_packages(),    
    install_requires=[],
)