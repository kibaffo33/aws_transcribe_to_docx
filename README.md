# aws_transcribe_to_docx
Procude Word Document transcriptions using the automatic speech recognition from AWS Transcribe.



## Usage

With `application.py` in the same folder as your aws transcribe `output.json`:

```bash
python3 application.py output.json
```

The python app will produce a .docx transcript from the .json output of AWS transcribe.

The .docx filename will be the same as the transcript job name.

### Logging

Use optional `log` argument to enable logging to CloudWatch Logs. Defaults to Log Group 'Transcripts' and Log Stream 'Application'

```bash
python3 application.py output.json log
```



## Dependencies

```bash
pip install -r requirements.txt
```

## Results

| Time    | Speaker | Comment     |
| ------- | ------- | ----------- |
| 0:00:03 | spk_0   | Is this on? |
| 0:00:05 | spk_1   | Yep.        |
| 0:00:06 | spk_0   | Great.      |


