import setuptools

setuptools.setup(
    name="aws-scribe",
    version="1.0",
    author="kibaffo33",
    author_email="robertedwardwilliams@me.com",
    description="Produce .docx transcriptions from AWS Transcribe output.",
    url="https://github.com/kibaffo33/aws_transcribe_to_docx",
    keywords=["aws", "transcribe", "docx"],
    py_modules=["scribe"],
    packages=setuptools.find_packages(),
)
