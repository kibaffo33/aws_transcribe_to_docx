""" Produce Word Document transcriptions using the automatic speech recognition from AWS Transcribe. """

from docx import Document
from docx.shared import Cm, Mm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json, datetime
import matplotlib.pyplot as plt
import statistics
from pathlib import Path
from time import perf_counter
import pandas
import sqlite3


def convert_time_stamp(n):
    """ Function to help convert timestamps from s to H:M:S """
    ts = datetime.timedelta(seconds=float(n))
    ts = ts - datetime.timedelta(microseconds=ts.microseconds)
    return str(ts)


def load_json(file):
    """Load in JSON file and return as dict"""

    json_filepath = Path(file)
    assert json_filepath.is_file(), "JSON file does not exist"

    data = json.load(open(json_filepath.absolute(), "r", encoding="utf-8"))
    assert "jobName" in data
    assert "results" in data
    assert "status" in data
    
    assert data["status"] == "COMPLETED", "JSON file not shown as completed."

    return data


def confidence_stats(data):
    """Confidence Statistics"""

    # Assign data to variable
    data = data

    # Stats dictionary
    stats = {
        "timestamps": [],
        "accuracy": [],
        "9.8": 0, "9": 0, "8": 0, "7": 0, "6": 0, "5": 0, "4": 0, "3": 0, "2": 0, "1": 0, "0": 0,
        "total": len(data["results"]["items"])}

    # Confidence count
    for item in data["results"]["items"]:
        if item["type"] == "pronunciation":
            stats["timestamps"].append(float(item["start_time"]))
            stats["accuracy"].append(int(float(item["alternatives"][0]["confidence"]) * 100))
            if float(item["alternatives"][0]["confidence"]) >= 0.98: stats["9.8"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.9: stats["9"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.8: stats["8"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.7: stats["7"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.6: stats["6"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.5: stats["5"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.4: stats["4"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.3: stats["3"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.2: stats["2"] += 1
            elif float(item["alternatives"][0]["confidence"]) >= 0.1: stats["1"] += 1
            else: stats["0"] += 1
    
    return stats


def make_graph(stats, dir):
    """Make scatter graph from confidence statistics"""

    # Confidence of each word as scatter graph
    plt.scatter(stats["timestamps"], stats["accuracy"])

    # Mean average as line across graph
    plt.plot([stats["timestamps"][0], stats["timestamps"][-1]], [statistics.mean(stats["accuracy"]), statistics.mean(stats["accuracy"])], "r")

    # Formatting
    plt.xlabel("Time (seconds)")
    plt.ylabel("Accuracy (percent)")
    plt.yticks(range(0, 101, 10))
    plt.title("Accuracy during transcript")
    plt.legend(["Accuracy average (mean)", "Individual words"], loc="lower center")

    # Target filename, including dir for explicit path 
    filename = Path(dir + "/chart.png")

    plt.savefig(filename)
    plt.clf()

    return str(filename)

    
def decode_transcript(data):
    """Decode the transcript into a pandas dataframe"""

    # Assign data to variable
    data = data

    decoded_data = {
        "time": [],
        "speaker": [],
        "comment": []
    }

    # If speaker identification
    if "speaker_labels" in data["results"].keys():

        # A segment is a blob of pronounciation and punctuation by an individual speaker
        for segment in data["results"]["speaker_labels"]["segments"]:

            # If there is content in the segment, add a row, write the time and speaker
            if len(segment["items"]) > 0:
                decoded_data['time'].append(convert_time_stamp(segment["start_time"]))
                decoded_data['speaker'].append(segment["speaker_label"])
                decoded_data['comment'].append("")

                # For each word in the segment...
                for word in segment["items"]:

                    # Get the word with the highest confidence
                    pronunciations = list(filter(lambda x: x["type"] == "pronunciation", data["results"]["items"]))
                    word_result = list(filter(lambda x: x["start_time"] == word["start_time"] and x["end_time"] == word["end_time"], pronunciations))
                    result = sorted(word_result[-1]["alternatives"], key=lambda x: x["confidence"])[-1]

                    # Write the word
                    decoded_data["comment"][-1] += " " + result["content"]

                    # If the next item is punctuation, write it
                    try:
                        word_result_index = data["results"]["items"].index(word_result[0])
                        next_item = data["results"]["items"][word_result_index + 1]
                        if next_item["type"] == "punctuation":
                            decoded_data["comment"][-1] += next_item["alternatives"][0]["content"]
                    except IndexError:
                        pass

    # Else no speaker identification
    else:

        decoded_data['time'].append("")
        decoded_data['speaker'].append("")
        decoded_data['comment'].append("")

        # Add words
        for word in data["results"]["items"]:

            # Get the word with the highest confidence
            result = sorted(word["alternatives"], key=lambda x: x["confidence"])[-1]

            # Write the word
            decoded_data["comment"][-1] += " " + result["content"]

            # If the next item is punctuation, write it
            try:
                word_result_index = data["results"]["items"].index(word)
                next_item = data["results"]["items"][word_result_index + 1]
                if next_item["type"] == "punctuation":
                    decoded_data["comment"][-1] += next_item["alternatives"][0]["content"]
            except IndexError:
                pass

    # Produce pandas dataframe
    df = pandas.DataFrame(decoded_data, columns=["time", "speaker", "comment"])

    # Clean leading whitespace
    df['comment'] = df['comment'].str.lstrip()

    return df


def write_docx(data, filename, **kwargs):
    """ Write a transcript from the .json transcription file. """

    output_filename = Path(filename)

    # Initiate Document
    document = Document()
    # A4 Size
    document.sections[0].page_width = Mm(210)
    document.sections[0].page_height = Mm(297)
    # Font
    font = document.styles["Normal"].font
    font.name = "Calibri"

    # Assign data to variable
    data = data

    # Document title and intro
    title = f"Transcription of {data['jobName']}"
    document.add_heading(title, level=1)
    # Set thresholds for formatting later
    threshold_for_grey = 0.98
    # Intro
    document.add_paragraph("Transcription using AWS Transcribe automatic speech recognition.")
    document.add_paragraph(datetime.datetime.now().strftime("Document produced on %A %d %B %Y at %X using the 'tscribe' python package."))
    document.add_paragraph()  # Spacing
    document.add_paragraph(f"Grey text has less than {int(threshold_for_grey * 100)}% confidence.")

    # Get stats
    stats = confidence_stats(data)

    # Display confidence count table
    table = document.add_table(rows=1, cols=3)
    table.style = document.styles["Light List Accent 1"]
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Confidence"
    hdr_cells[1].text = "Count"
    hdr_cells[2].text = "Percentage"
    row_cells = table.add_row().cells
    row_cells[0].text = str("98% - 100%")
    row_cells[1].text = str(stats["9.8"])
    row_cells[2].text = str(round(stats["9.8"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("90% - 97%")
    row_cells[1].text = str(stats["9"])
    row_cells[2].text = str(round(stats["9"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("80% - 89%")
    row_cells[1].text = str(stats["8"])
    row_cells[2].text = str(round(stats["8"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("70% - 79%")
    row_cells[1].text = str(stats["7"])
    row_cells[2].text = str(round(stats["7"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("60% - 69%")
    row_cells[1].text = str(stats["6"])
    row_cells[2].text = str(round(stats["6"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("50% - 59%")
    row_cells[1].text = str(stats["5"])
    row_cells[2].text = str(round(stats["5"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("40% - 49%")
    row_cells[1].text = str(stats["4"])
    row_cells[2].text = str(round(stats["4"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("30% - 39%")
    row_cells[1].text = str(stats["3"])
    row_cells[2].text = str(round(stats["3"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("20% - 29%")
    row_cells[1].text = str(stats["2"])
    row_cells[2].text = str(round(stats["2"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("10% - 19%")
    row_cells[1].text = str(stats["1"])
    row_cells[2].text = str(round(stats["1"] / stats["total"] * 100, 2)) + "%"
    row_cells = table.add_row().cells
    row_cells[0].text = str("0% - 9%")
    row_cells[1].text = str(stats["0"])
    row_cells[2].text = str(round(stats["0"] / stats["total"] * 100, 2)) + "%"
    # Add paragraph for spacing
    document.add_paragraph()

    graph = make_graph(stats, str(output_filename.parent))
    document.add_picture(graph, width=Cm(14.64))
    document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_page_break()

    # Process and display transcript by speaker segments
    table = document.add_table(rows=1, cols=3)
    table.style = document.styles["Light List Accent 1"]
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Time"
    hdr_cells[1].text = "Speaker"
    hdr_cells[2].text = "Content"

    # If speaker identification
    if "speaker_labels" in data["results"].keys():

        # A segment is a blob of pronounciation and punctuation by an individual speaker
        for segment in data["results"]["speaker_labels"]["segments"]:

            # If there is content in the segment, add a row, write the time and speaker
            if len(segment["items"]) > 0:
                row_cells = table.add_row().cells
                row_cells[0].text = convert_time_stamp(segment["start_time"])
                row_cells[1].text = str(segment["speaker_label"])

                # For each word in the segment...
                for word in segment["items"]:

                    # Get the word with the highest confidence
                    pronunciations = list(filter(lambda x: x["type"] == "pronunciation", data["results"]["items"]))
                    word_result = list(filter(lambda x: x["start_time"] == word["start_time"] and x["end_time"] == word["end_time"], pronunciations))
                    result = sorted(word_result[-1]["alternatives"], key=lambda x: x["confidence"])[-1]

                    # Write the word
                    run = row_cells[2].paragraphs[0].add_run(" " + result["content"])
                    if float(result["confidence"]) < threshold_for_grey:
                        font = run.font
                        font.color.rgb = RGBColor(204, 204, 204)

                    # If the next item is punctuation, write it
                    try:
                        word_result_index = data["results"]["items"].index(word_result[0])
                        next_item = data["results"]["items"][word_result_index + 1]
                        if next_item["type"] == "punctuation":
                            run = row_cells[2].paragraphs[0].add_run(next_item["alternatives"][0]["content"])
                    except IndexError:
                        pass

    # Else no speaker identification
    else:

        # Start the first row
        row_cells = table.add_row().cells

        # Add words
        for word in data["results"]["items"]:

            # Get the word with the highest confidence
            result = sorted(word["alternatives"], key=lambda x: x["confidence"])[-1]

            # Write the word
            run = row_cells[2].paragraphs[0].add_run(" " + result["content"])
            if float(result["confidence"]) < threshold_for_grey:
                font = run.font
                font.color.rgb = RGBColor(204, 204, 204)

            # If the next item is punctuation, write it
            try:
                word_result_index = data["results"]["items"].index(word)
                next_item = data["results"]["items"][word_result_index + 1]
                if next_item["type"] == "punctuation":
                    run = row_cells[2].paragraphs[0].add_run(next_item["alternatives"][0]["content"])
            except IndexError:
                pass

    # Formatting transcript table widthds
    widths = (Inches(0.6), Inches(1), Inches(4.5))
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = width

    # Save
    document.save(filename)


def write(file, **kwargs):
    """Main function, write transcript file from json"""

    # Performance timer start
    start = perf_counter()

    # Load json file as dict
    data = load_json(file)

    # Decode transcript
    df = decode_transcript(data)

    # Output
    output_format = kwargs.get("format", "docx")

    # Deprecated tmp_dir by improving save_as
    if kwargs.get("tmp_dir"):
        import warnings
        warnings.warn("tmp_dir is deprecated, specify path in save_as instead", DeprecationWarning)
    
    # Output to docx (default behaviour)
    if output_format == "docx":
        filename = kwargs.get("save_as", f"{data['jobName']}.docx")
        write_docx(data, filename)
    
    # Output to CSV
    elif output_format == "csv":
        filename = kwargs.get("save_as", f"{data['jobName']}.csv")
        df.to_csv(filename)
    
    # Output to sqlite
    elif output_format == "sqlite":
        filename = kwargs.get("save_as", f"{data['jobName']}.db")
        conn = sqlite3.connect(str(filename))
        df.to_sql("transcript", conn)
        conn.close()

    else:
        raise Exception("Output format should be 'docx', 'csv' or 'sqlite'")

    # Performance timer finish
    finish = perf_counter()
    duration = round(finish - start, 2)

    print(f"{filename} written in {duration} seconds.")
