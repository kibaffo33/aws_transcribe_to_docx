# aws_transcribe_to_docx

Produce Word Document transcriptions using the automatic speech recognition from AWS Transcribe. Requires  Python 3.7+

[![Build Status](https://travis-ci.com/kibaffo33/aws_transcribe_to_docx.svg?branch=master)](https://travis-ci.com/kibaffo33/aws_transcribe_to_docx)

# Installation

```bash
pip install tscribe
```

## Usage

```
>>> import tscribe

>>> tscribe.write("output.json")
Transcript output.docx written.

>>> tscribe.write("output.json", save_as="transcript.docx")
Transcript transcript.docx writen.
```

## Results

| Time    | Speaker | Comment     |
| ------- | ------- | ----------- |
| 0:00:03 | spk_0   | Is this on? |
| 0:00:05 | spk_1   | Yep.        |
| 0:00:06 | spk_0   | Great.      |


