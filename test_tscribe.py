import tscribe
import os


def test_process():
    assert os.access("test_sample.json", os.F_OK), "Input file not found"
    tscribe.write("test_sample.json", save_as="test_sample.docx")
    assert os.access("test_sample.docx", os.F_OK), "Output file not found"
    os.remove("test_sample.docx")
