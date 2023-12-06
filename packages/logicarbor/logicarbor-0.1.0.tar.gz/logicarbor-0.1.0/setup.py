from setuptools import setup

setup(
    name='logicarbor',
    version='0.1.0',
    description='Python client for Logicarbor API',
    author='logicarbor dev team',
    author_email='admin@logicarbor.com',
    url='https://api.logicarbor.com/v3.0/documentation.html',
    packages=['logicarbor'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
