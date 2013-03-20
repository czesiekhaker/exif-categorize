#!/usr/bin/env python

from argparse import ArgumentParser
import os, glob, shutil
from subprocess import Popen, PIPE

EXIF_MODEL_KEY = 'Exif.Image.Model'
JPEG_EXTENSIONS = ('[jJ][pP][gG]', '[jJ][pP][eE][gG]')

def main():
    # Parse options
    # TODO: This can be easily extended with options to specify
    # target dir name and minimal dimensions
    parser = ArgumentParser(description="Move JPEG files with any"
            " dimension smaller than 600px to ./small/ directory")
    parser.add_argument("directory", help="")
    args = parser.parse_args()

    # Find the JPEGs
    directory = os.path.realpath(os.path.normcase(args.directory))
    files = []
    for extension in JPEG_EXTENSIONS:
        file_glob = "%s.%s" % (os.path.join(directory, '*'), extension)
        files.extend(glob.glob(file_glob))
    files.sort()

    for f in files:
        # Figure out the size (requires ImageMagick's identify)
        # TODO: I wonder if we can do this smarter (w/out Popen)
        x = Popen("identify " + f + " | cut -d ' ' -f 3 | cut -d 'x' -f 1",\
                stdout=PIPE, shell=True).stdout.read()
        y = Popen("identify " + f + " | cut -d ' ' -f 3 | cut -d 'x' -f 2",\
                stdout=PIPE, shell=True).stdout.read()
        x = int(x)
        y = int(y)

        # Pass if both dimentions are larger than 600px
        if x >= 600 and y >= 600:
            continue

        small_dir = 'small'
        small_dir_path = os.path.join(directory, small_dir)

        # Create target directory if necessary
        if not os.path.exists(small_dir_path):
            print "Creating directory '%s'..." % small_dir_path,
            os.mkdir(small_dir_path)
            print 'Done'

        file_name = os.path.basename(os.path.join(small_dir_path, f))
        moved_file_path = os.path.join(small_dir_path, file_name)

        # Do the moves
        print '%s -> %s' % (file_name, moved_file_path),
        shutil.move(f, moved_file_path)
        print 'Done'

if __name__ == "__main__":
    main()
