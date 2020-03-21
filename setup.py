import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="tscribe",
    version="1.2.0",
    author="Robert Williams",
    author_email="robertedwardwilliams@me.com",
    description="Produce .docx transcriptions from AWS Transcribe output.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kibaffo33/aws_transcribe_to_docx",
    packages=setuptools.find_packages(),
    install_requires=["python-docx", "matplotlib", "pandas"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
)
