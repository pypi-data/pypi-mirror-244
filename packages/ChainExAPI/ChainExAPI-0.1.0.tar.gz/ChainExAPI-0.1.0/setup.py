from setuptools import setup, find_packages

setup(
    name='ChainExAPI',
    version='0.1.0',
    packages=find_packages(),
    description='Python client library for interacting with the ChainEx cryptocurrency exchange API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Richard A',
    author_email='richardatk01@gmail.com',
    url='https://github.com/RichardAtCT//chainexapi',
    install_requires=[
        'requests>=2.25.1',
        # Include any other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='chainex cryptocurrency exchange api',
    python_requires='>=3.6',
)
