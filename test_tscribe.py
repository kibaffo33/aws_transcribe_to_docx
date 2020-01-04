import tscribe
import os


def test_multiple_speakers():
    """
    Test output exists with multiple speaker input

    # GIVEN a sample file containing multiple speakers
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx without errors

    """

    # Setup
    input_file = "sample_multiple.json"
    output_file = "sample_multiple.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("chart.png")


def test_multiple_speakers_with_save_as():
    """
    Test output exists with multiple speaker input, and save_as defined

    # GIVEN a sample file containing multiple speakers, and an output filename
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, named correctly, without errors

    """

    # Setup
    input_file = "sample_multiple.json"
    output_file = "test_sample.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("chart.png")


def test_multiple_speakers_with_save_as_with_tmp_dir():
    """
    Test output exists with multiple speaker input, and save_as defined, and tmp_dir defined

    # GIVEN a sample file containing multiple speakers, and an output filename, and a writable tmp directory
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, named correctly, without errors

    """

    # Setup
    input_file = "sample_multiple.json"
    output_file = "test_sample.docx"
    tmp_dir = "/tmp/"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file, tmp_dir=tmp_dir)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove(tmp_dir+"chart.png")


def test_single_speaker():
    """
    Test output exists with single speaker input

    # GIVEN a sample file containing single speaker
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx without errors

    """

    # Setup
    input_file = "sample_single.json"
    output_file = "sample_single.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("chart.png")


def test_single_speaker_with_save_as():
    """
    Test output exists with single speaker input, and save_as defined

    # GIVEN a sample file containing single speaker, and an output filename
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, named correctly, without errors

    """

    # Setup
    input_file = "sample_single.json"
    output_file = "test_sample.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("chart.png")


def test_single_speaker_with_save_as_with_tmp_dir():
    """
    Test output exists with single speaker input, and save_as defined, and tmp_dir defined

    # GIVEN a sample file containing single speaker, and an output filename, and a writable tmp directory
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, named correctly, without errors

    """

    # Setup
    input_file = "sample_single.json"
    output_file = "test_sample.docx"
    tmp_dir = "/tmp/"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file, tmp_dir=tmp_dir)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove(tmp_dir+"chart.png")