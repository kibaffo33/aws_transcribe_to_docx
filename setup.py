from setuptools import setup

setup(
    name='AWS Transcribe .json to .docx',
    version='0.1',
    py_modules=['application'],
    install_requires=[
        'Click',
        'boto3',
        'botocore',
        'cycler',
        'docutils',
        'jmespath',
        'kiwisolver',
        'lxml',
        'matplotlib',
        'numpy',
        'pyparsing',
        'python-dateutil',
        'python-docx',
        'pytz',
        's3transfer',
        'six',
        'statistics'
    ],
    entry_points='''
        [console_scripts]
        trdx=application:make_document
    ''',
)
