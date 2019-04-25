# aws_transcribe_to_docx
Produce Word Document transcriptions using the automatic speech recognition from AWS Transcribe.

# Installation

```bash
pip install scribe
```

## Usage

```
>>> import scribe

>>> scribe.write("output.json")
Transcript output.docx written.

>>> scribe.write("output.json", save_as="transcript.docx")
Transcript transcript.docx writen.
```

## Results

| Time    | Speaker | Comment     |
| ------- | ------- | ----------- |
| 0:00:03 | spk_0   | Is this on? |
| 0:00:05 | spk_1   | Yep.        |
| 0:00:06 | spk_0   | Great.      |


