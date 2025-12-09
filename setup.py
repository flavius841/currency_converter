from setuptools import setup, find_packages

setup(
    name='currency_converter',
    version='0.0.1',
    description='A simple CLI project to convert currencies using real-time exchange rates.',
    author='Flavius Pintilie',
    author_email='flaviusepintilie@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "convert_currency=main_folder.entry:main",
        ],
    },
    install_requires=[
        "colorama",
        'requests',
        'prompt_toolkit',
    ],
)
