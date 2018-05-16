# aws_transcribe_to_docx
Procude Word Document transcriptions using the automatic speech recognition from AWS Transcribe.



## Usage

With `application.py` in the same folder as your aws transcribe `output.json`:

```bash
python3 application.py 'output.json'
```

The python app will produce a .docx transcript from the .json output of AWS transcribe.

The .docx filename will be the same as the transcript job name.



## Dependencies

```bash
pip install -r requirements.txt
```




## Recommened use in a virtualenv

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python3 application.py 'output.json'

deactivate
```



