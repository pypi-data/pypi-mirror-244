from setuptools import setup, find_packages

setup(
    name='tefas',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
     'selenium','pandas'
    ],
    author='Atahan Uz',
    author_email='atahanuz23@gmail.com',
    description="Extract text from a YouTube video in a single command, using OpenAi's Whisper speech recognition model",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_data={
        'lol_stats': ['data/*', 'templates/*'],
    },
    url='https://github.com/atahanuz/tefas',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)