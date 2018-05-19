# Take inputs of VOB files and produce an mp3 with only the audio (audio-only.mp3)
# Requires ffmpeg

print('# Extract audio from VOB files')

import os

VOBS = []
def get_vobs():
    for i in os.listdir():
        if '.VOB' in i:
            VOBS.append(i)
    print(str(len(VOBS)), '.VOB files found.')

def single(v):
    # Input string of filename and receive single mp3 result
    os.system('ffmpeg -i ' + v + ' -map 0:2 -vn -acodec copy -f mp2 audio-only.mp3')

def multiple(vs):
    # Input list of .vob filenames and receive single mp3 result
    filenames = str()
    for i in vs:
        filenames = filenames + i + ' '
    os.system('cat ' + filenames + '| ffmpeg -i - -map 0:2 -vn -acodec copy -f mp2 audio-only.mp3')

get_vobs()

if len(VOBS) == 1:
    single(VOBS[0])

elif len(VOBS) > 1:
    multiple(VOBS)

if len(VOBS) > 0:
    print ('# audio-only.mp3 created for ' + str(VOBS))
