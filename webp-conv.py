#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Converts any PNG, JPG or JPEG to WEBP, using Google's cwebp conversion tool:
# https://developers.google.com/speed/webp/
#
# Sample usage:
#   webp-conv -s /path/to/pics/ -q 80 --remove
#
# Copyright 2017 llobile
# Licensed under the Apache License, Version 2.0 (the "License")

import os
from optparse import OptionParser
from subprocess import check_call

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")
CURRENT_WORKING_DIR = os.getcwd()
COMPRESSION_QUALITY_LEVEL = 80


def is_cwebp_available():
    try:
        with open(os.devnull, 'w') as devnull:
            check_call(['cwebp', '-version'], stdout=devnull)
        return True
    except:
        return False


def find_files(directory, extensions=IMAGE_EXTENSIONS):
    found = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(extensions):
                found.append(os.path.join(root, f))
    return found


def replace_extension(path, extension):
    name = os.path.splitext(path)[0]
    return '{}.{}'.format(name, extension)


def convert_to_webp(path, parser_options):
    webp_path = replace_extension(path, 'webp')

    # Don't overwrite existing files by accident.
    if os.path.isfile(webp_path):
        raise ValueError('webp image for {} already exists'.format(path))

    quality = parser_options.quality
    check_call(['cwebp', '-q', str(quality), path, '-o', webp_path])

    # Remember the original and converted size.
    original = os.path.getsize(path)
    converted = os.path.getsize(webp_path)

    if parser_options.remove:
        os.remove(path)

    return original, converted


def convert(parser_options):
    original = 0
    converted = 0

    files = find_files(parser_options.source)
    for f in files:
        original, converted = convert_to_webp(f, parser_options)
        original += original
        converted += converted

    return len(files), original, converted


def create_parser():
    parser = OptionParser()
    parser.add_option("-q", "--quality",
                      type="float",
                      dest="quality",
                      default=COMPRESSION_QUALITY_LEVEL,
                      help="Compression factor for RGB channels")
    parser.add_option("-s", "--source",
                      dest="source",
                      default=CURRENT_WORKING_DIR,
                      help="Source directory")
    parser.add_option("--remove",
                      action="store_true",
                      dest="remove",
                      help="Remove source file upon conversion")
    return parser


def log(message):
    print message


def main():
    if not is_cwebp_available():
        message = """
        cwebp script unavailable, add it to path or get it here:
        https://developers.google.com/speed/webp/
        """
        raise ValueError(message)

    parser = create_parser()
    options, args = parser.parse_args()

    # Validate input.
    source = options.source
    if not os.path.isdir(source):
        raise ValueError('{} is not a directory.'.format(source))

    quality = options.quality
    if not 0 < quality <= 100:
        raise ValueError('quality must be between 1-100')

    # If remove option is on, double check that's intended.
    if options.remove:
        answer = raw_input("Remove files upon conversion? (y/n) ")
        if answer.strip().lower() != 'y':
            raise ValueError('exiting script, nothing was altered')

    # Do the magic.
    count, original_size, converted_size = convert(options)
    if count:
        percent = 100.0 * (original_size - converted_size) / original_size
        log('converted {} items'.format(count))
        log('old size={} bytes, new size={} bytes, saved {:.2f}%'
            .format(original_size, converted_size, percent))
    else:
        log('no files converted')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(e.message)
