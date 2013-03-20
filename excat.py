#!/usr/bin/env python

# Usage:
#   excat <source dir>

# TODO:
# --copy (move by default)
# --dry-run
# --tag (eg. Exif.Image.Model, model, Exif.Image.DateTime)
# --stats (view the number of files per tag value)
# --min (move files only if there is more than n of them for a certain
#   tag value)
# --move-twin-files (also move files with the same basename)

from argparse import ArgumentParser
import pyexiv2
import os, glob, shutil

EXIF_MODEL_KEY = 'Exif.Image.Model'
JPEG_EXTENSIONS = ('[jJ][pP][gG]', '[jJ][pP][eE][gG]')

def main():
    parser = ArgumentParser(description="Move JPEG files into"
            " subdirectories depending on the value of the EXIF tag")
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
        # Read EXIF metadata
        metadata = pyexiv2.ImageMetadata(f)
        metadata.read()
        cam_model = metadata[EXIF_MODEL_KEY].value\
                if EXIF_MODEL_KEY in metadata.exif_keys else 'Unknown'
        
        # Replace '/'s in the model string
        if '/' in cam_model:
            cam_model = cam_model.replace('/', '_')

        # Create the directory
        cam_dir_path = os.path.join(directory, cam_model)
        if not os.path.exists(cam_dir_path):
            print "Creating directory '%s'..." % cam_dir_path,
            os.mkdir(cam_dir_path)
            print 'Done'

        file_name = os.path.basename(os.path.join(cam_dir_path, f))
        moved_file_path = os.path.join(cam_dir_path, file_name)

        # Do the moves
        print '%s -> %s ...' % (file_name, moved_file_path),
        shutil.move(f, moved_file_path)
        print 'Done'

if __name__ == "__main__":
    main()
