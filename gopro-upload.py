#!/usr/bin/env python3

import subprocess
import sys
import os
import re
import glob
from datetime import datetime

def error(message):
    print(message)
    sys.exit(1)

def verify_files_exist(files):
    for file in files:
        if not os.path.isfile(file):
            error(f'Could not find file at path {file}')

def process_video(video):
    print(f'*************** Processing {video} ***************')
    index = get_video_index(video)
    created_time = get_created_time(video)
    parts = find_all_parts(video, index)
    combined = combine(parts, index)
    title = f'GOPRO {index} {created_time}'
    upload(combined, title)
    delete_all_files_with_index(video, index)

def get_video_index(video):
    filename = os.path.basename(video)
    return re.search('GOPR(\d.+).MP4', filename).group(1)

def get_created_time(file):
    return datetime.fromtimestamp(os.stat(file).st_birthtime)

def find_all_parts(video, index):
    directory = os.path.dirname(video)
    return sorted(glob.glob(os.path.join(directory, f'*{index}.MP4')))

def combine(parts, index):
    output_file = f'/tmp/{index}.mp4'
    print(f'***** Combining into {output_file} *****')
    try:
        subprocess.check_call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', create_concat_input_file(parts, index), '-c', 'copy', output_file])
    except subprocess.CalledProcessError:
        error(f'There was an issue combining the following parts with ffmpeg: {parts}')
    return output_file

def create_concat_input_file(parts, index):
    path = f'/tmp/concat_inputs_{index}.txt'
    with open(path, 'w') as file:
        for part in parts:
            file.write(f"file '{part}'\n")
    return path

def upload(video, title):
    print(f'***** Uploading {video} with title {title} *****')
    youtube_upload = os.environ['YOUTUBE_UPLOAD']
    client_secrets = os.environ['YOUTUBE_CLIENT_SECRETS']
    try:
        subprocess.check_call([
            'python3', youtube_upload,
            '--client-secrets', client_secrets,
            '--title', title,
            '--playlist', 'GOPRO',
            '--privacy', 'unlisted',
            video
        ])
    except subprocess.CalledProcessError:
        error(f'There was an issue uploading the following video: {video}')

def delete_all_files_with_index(video, index):
    print(f'***** Deleting all files associated with {video} *****')
    directory = os.path.dirname(video)
    files = glob.glob(os.path.join(directory, f'*{index}.*'))
    for file in files:
        print(f'Deleting {file}')
        os.remove(file)


if __name__ == '__main__':
    files = sorted(sys.argv[1:])
    if len(files) == 0:
        error('Please provide at least one video to upload\nUsage: gopro-upload.py VIDEO [VIDEO2 ...]')
    verify_files_exist(files)
    for video in files:
        process_video(video)
