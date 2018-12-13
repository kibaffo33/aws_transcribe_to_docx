# aws_transcribe_to_docx
Produce Word Document transcriptions using the automatic speech recognition from AWS Transcribe.

# Installation

```bash
git clone https://github.com/kibaffo33/aws_transcribe_to_docx.git
cd aws_transcribe_to_docx
pip install .
```

## Usage

```bash
trdx -f transcribe.json
```


### Logging

Use optional `-l` followed by your Log Group and Stream, to enable logging to CloudWatch Logs. 

```bash
trdx -f transcribe.json -l Transcripts Application
```


## Results

| Time    | Speaker | Comment     |
| ------- | ------- | ----------- |
| 0:00:03 | spk_0   | Is this on? |
| 0:00:05 | spk_1   | Yep.        |
| 0:00:06 | spk_0   | Great.      |


