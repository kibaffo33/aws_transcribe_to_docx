""" Produce Word Document transcriptions using the automatic speech recognition from AWS Transcribe. """

from docx import Document
from docx.shared import Cm, Mm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json, datetime
import matplotlib.pyplot as plt
import statistics


def convert_time_stamp(n):
    """ Function to help convert timestamps from s to H:M:S """
    ts = datetime.timedelta(seconds=float(n))
    ts = ts - datetime.timedelta(microseconds=ts.microseconds)
    return str(ts)


def write(file, **kwargs):
    """ Write a transcript from the .json transcription file. """

    # Initiate Document
    document = Document()
    # A4 Size
    document.sections[0].page_width = Mm(210)
    document.sections[0].page_height = Mm(297)
    # Font
    font = document.styles['Normal'].font
    font.name = 'Calibri'

    # Load Transcription output
    data = json.load(open(file, 'r'))

    # Document title and intro
    title = f"Transcription of {data['jobName']}"
    document.add_heading(title, level=1)
    # Set thresholds for formatting later
    threshold_for_grey = 0.98
    # Intro
    document.add_paragraph('Transcription using AWS Transcribe automatic speech recognition.')
    document.add_paragraph(datetime.datetime.now().strftime('Document produced on %A %d %B %Y at %X.'))
    document.add_paragraph()  # Spacing
    document.add_paragraph(f"Grey text has less than {int(threshold_for_grey * 100)}% confidence.")

    # Stats dictionary
    stats = {
        'timestamps': [],
        'accuracy': [],
        '9.8': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0, '1': 0, '0': 0,
        'total': len(data['results']['items'])}

    # Confidence count
    for item in data['results']['items']:
        if item['type'] == 'pronunciation':
            stats['timestamps'].append(float(item['start_time']))
            stats['accuracy'].append(int(float(item['alternatives'][0]['confidence']) * 100))
            if float(item['alternatives'][0]['confidence']) >= 0.98: stats['9.8'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.9: stats['9'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.8: stats['8'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.7: stats['7'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.6: stats['6'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.5: stats['5'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.4: stats['4'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.3: stats['3'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.2: stats['2'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.1: stats['1'] += 1
            else: stats['0'] += 1
    # Display confidence count table
    table = document.add_table(rows=1, cols=3)
    table.style = document.styles['Light List Accent 1']
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Confidence'
    hdr_cells[1].text = 'Count'
    hdr_cells[2].text = 'Percentage'
    row_cells = table.add_row().cells
    row_cells[0].text = str('98% - 100%')
    row_cells[1].text = str(stats['9.8'])
    row_cells[2].text = str(round(stats['9.8'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('90% - 97%')
    row_cells[1].text = str(stats['9'])
    row_cells[2].text = str(round(stats['9'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('80% - 89%')
    row_cells[1].text = str(stats['8'])
    row_cells[2].text = str(round(stats['8'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('70% - 79%')
    row_cells[1].text = str(stats['7'])
    row_cells[2].text = str(round(stats['7'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('60% - 69%')
    row_cells[1].text = str(stats['6'])
    row_cells[2].text = str(round(stats['6'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('50% - 59%')
    row_cells[1].text = str(stats['5'])
    row_cells[2].text = str(round(stats['5'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('40% - 49%')
    row_cells[1].text = str(stats['4'])
    row_cells[2].text = str(round(stats['4'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('30% - 39%')
    row_cells[1].text = str(stats['3'])
    row_cells[2].text = str(round(stats['3'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('20% - 29%')
    row_cells[1].text = str(stats['2'])
    row_cells[2].text = str(round(stats['2'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('10% - 19%')
    row_cells[1].text = str(stats['1'])
    row_cells[2].text = str(round(stats['1'] / stats['total'] * 100, 2)) + '%'
    row_cells = table.add_row().cells
    row_cells[0].text = str('0% - 9%')
    row_cells[1].text = str(stats['0'])
    row_cells[2].text = str(round(stats['0'] / stats['total'] * 100, 2)) + '%'
    # Add paragraph for spacing
    document.add_paragraph()
    # Display scatter graph of confidence
    # Confidence of each word as scatter graph
    plt.scatter(stats['timestamps'], stats['accuracy'])
    # Mean average as line across graph
    plt.plot([stats['timestamps'][0], stats['timestamps'][-1]],
             [statistics.mean(stats['accuracy']), statistics.mean(stats['accuracy'])], 'r')
    # Formatting
    plt.xlabel('Time (seconds)')
    # plt.xticks(range(0, int(stats['timestamps'][-1]), 60))
    plt.ylabel('Accuracy (percent)')
    plt.yticks(range(0, 101, 10))
    plt.title('Accuracy during video')
    plt.legend(['Accuracy average (mean)', 'Individual words'], loc='lower center')
    plt.savefig('chart.png')
    document.add_picture('chart.png', width=Cm(14.64))
    document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_page_break()

    # Process and display transcript by speaker segments
    table = document.add_table(rows=1, cols=3)
    table.style = document.styles['Light List Accent 1']
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Time'
    hdr_cells[1].text = 'Speaker'
    hdr_cells[2].text = 'Content'

    for segment in data['results']['speaker_labels']['segments']:
        # If there is content in the segment
        if len(segment['items']) > 0:
            # Add a row, write the time and speaker
            row_cells = table.add_row().cells
            row_cells[0].text = convert_time_stamp(segment['start_time'])
            row_cells[1].text = str(segment['speaker_label'])

            # Segments group individual word results by speaker. They are cross-referenced by time.
            # For each word in the segment...
            for word in segment['items']:
                # Run through the word results and get the corresponding result
                for result in data['results']['items']:
                    if result['type'] == 'pronunciation':
                        if result['start_time'] == word['start_time']:

                            # Get the word with the highest confidence
                            if len(result['alternatives']) > 0:
                                current_word = dict()
                                confidence_scores = []
                                for score in result['alternatives']:
                                    confidence_scores.append(score['confidence'])
                                for alternative in result['alternatives']:
                                    if alternative['confidence'] == max(confidence_scores):
                                        current_word = alternative.copy()

                                # Write and format the word
                                run = row_cells[2].paragraphs[0].add_run(' ' + current_word['content'])
                                if float(current_word['confidence']) < threshold_for_grey:
                                    font = run.font
                                    font.color.rgb = RGBColor(204, 204, 204)

                                # If the next item is punctuation, add it
                                try:
                                    if data['results']['items'][data['results']['items'].index(result) + 1]['type'] == 'punctuation':
                                        run = row_cells[2].paragraphs[0].add_run(data['results']['items'][data['results']['items'].index(result) + 1]['alternatives'][0]['content'])
                                # Occasional IndexErrors encountered
                                except:
                                    pass

    # Formatting transcript table widthds
    widths = (Inches(0.6), Inches(1), Inches(4.5))
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = width

    # Save
    filename = kwargs.get('save_as', f"{data['jobName']}.docx")
    document.save(filename)
    print(f"Transcript {filename} writen.")
