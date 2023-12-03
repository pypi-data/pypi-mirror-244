from setuptools import setup, find_packages

setup(
    name='gcpmate',
    version='1.0.2',
    author='Tomek Porozynski',
    author_email='tomasz.porozynski@gmail.com',
    description=(
        'An OpenAI-powered assistant for managing '
        'Google Cloud Platform resources.'
    ),
    packages=find_packages(),
    install_requires=[
        'openai~=1.1.1',
        'prettytable~=3.6.0',
    ],
    entry_points={
        'console_scripts': [
            'gcpmate = gcpmate.gcpmate:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ontaptom/gcpmate',
)