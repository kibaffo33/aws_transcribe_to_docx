"""Legacy tests"""

import pytest
import os
import tscribe


def test_multiple_speakers():
    """
    Test output exists with multiple speaker input

    # GIVEN a sample file containing multiple speakers
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx without errors

    """

    # Setup
    input_file = "sample_material/03-speaker-identification.json"
    output_file = "sample_material/03-speaker-identification.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("sample_material/chart.png")


def test_multiple_speakers_with_save_as():
    """
    Test output exists with multiple speaker input, and save_as defined

    # GIVEN a sample file containing multiple speakers, and an output filename
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, named correctly, without errors

    """

    # Setup
    input_file = "sample_material/03-speaker-identification.json"
    output_file = "sample_material/test_sample.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("sample_material/chart.png")


# SKIPPED - chart now writes to same directory as output through use of the Path parent
# This works on the assumption that if you have permission to write to the dir for the
# output docx, you should have permission to write an image to that dir too
# Therefore no need to explicitly specify where the chart is written to, seperate to the docx
@pytest.mark.xfail(reason="Deprecated")
def test_multiple_speakers_with_save_as_with_tmp_dir():
    """
    Test output exists with multiple speaker input, and save_as defined, and tmp_dir defined

    # GIVEN a sample file containing multiple speakers, and an output filename, and a writable tmp directory
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, with a chart, named correctly, without errors

    """

    # Setup
    input_file = "sample_multiple.json"
    output_file = "test_sample.docx"
    tmp_dir = "/tmp/"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file, tmp_dir=tmp_dir)
    assert os.access(tmp_dir + "chart.png", os.F_OK), "Chart file not found"
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove(tmp_dir + "chart.png")


def test_single_speaker():
    """
    Test output exists with single speaker input

    # GIVEN a sample file containing single speaker
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx without errors

    """

    # Setup
    input_file = "sample_material/01-plain.json"
    output_file = "sample_material/01-plain.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("sample_material/chart.png")


def test_single_speaker_with_save_as():
    """
    Test output exists with single speaker input, and save_as defined

    # GIVEN a sample file containing single speaker, and an output filename
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, named correctly, without errors

    """

    # Setup
    input_file = "sample_material/01-plain.json"
    output_file = "sample_material/test_sample.docx"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file)
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove("sample_material/chart.png")


# SKIPPED - chart now writes to same directory as output through use of the Path parent
# This works on the assumption that if you have permission to write to the dir for the
# output docx, you should have permission to write an image to that dir too
# Therefore no need to explicitly specify where the chart is written to, seperate to the docx
@pytest.mark.xfail(reason="Deprecated")
def test_single_speaker_with_save_as_with_tmp_dir():
    """
    Test output exists with single speaker input, and save_as defined, and tmp_dir defined

    # GIVEN a sample file containing single speaker, and an output filename, and a writable tmp directory
    # WHEN calling tscribe.write(...)
    # THEN produce the .docx, with a chart, named correctly, without errors

    """

    # Setup
    input_file = "sample_single.json"
    output_file = "test_sample.docx"
    tmp_dir = "/tmp/"
    assert os.access(input_file, os.F_OK), "Input file not found"

    # Function
    tscribe.write(input_file, save_as=output_file, tmp_dir=tmp_dir)
    assert os.access(tmp_dir + "chart.png", os.F_OK), "Chart file not found"
    assert os.access(output_file, os.F_OK), "Output file not found"

    # Teardown
    os.remove(output_file)
    os.remove(tmp_dir + "chart.png")
