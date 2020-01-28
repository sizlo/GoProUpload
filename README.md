GoPro Upload
============

Script to upload videos from a go pro to youtube.

All the files that make up one video are located, concatenated with [ffmpeg](https://www.ffmpeg.org), uploaded with [youtube-upload](https://github.com/tokland/youtube-upload), then deleted from local storage.

Videos are uploaded as unlisted with the title `GOPRO {video index} {video created date/time}` e.g `GOPRO 0273 2020-01-27 08:37:47`. Videos are uploaded into a `GOPRO` playlist.

# Dependencies
[ffmpeg](https://www.ffmpeg.org) - Ffmpeg commands are run directly from this script so it must be available on the `$PATH` environment variable

[youtube-upload](https://github.com/tokland/youtube-upload) - This script must be available at the `$YOUTUBE_UPLOAD` environment variable. Follow the setup in this projects README to configure the youtube api, the `client-secrets.json` file produced from this must be available at the `$YOUTUBE_CLIENT_SECRETS` environment variable. The `youtube-upload` script requires some specific versions of it's dependencies, the following seems to work:

`pip3 install 'google-api-python-client==1.7.4'`

`pip3 install 'httplib2<0.16.0'`

# Usage
`gopro-upload.py VIDEO [VIDEO2 ...]`

Where `VIDEO` is the mp4 file for the first part of the video.
