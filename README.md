Exif categorize
===============

This is a simple script to move JPEG files into directories
depending on Exif tag values.

What works?
-----------

**Work in progress. Nothing works.**

Upcoming features:
* move files into subdirectories
* accept `--dry-run` option to display actions instead of moving files
* accept exif tag names after `--tag` option
* aliases for some tags (eg. `model` for `Exif.Image.Model`,
  `time` for `Exif.Image.DateTime`)
* accept `--stats` option to view the number of files per each tag value
* accept `--min` option to move the files only if there is more of them
  than `n` for a certain tag value

Why bother?
-----------

I was asked to recover some holiday photos from a broken harddisk.
After ddrescue/photorec procedure I ended up with 20 thousand
JPEGs, including system files, screenshots and [unrelated
pictures](http://i2.kym-cdn.com/photos/images/original/000/002/151/1180723070762.jpg).

Sorting the images by model of the camera it was taken with
seemed to be a reasonable thing to do. I would then see
what sticks - review the contents of the files starting with
a camera that made the biggest number of photos. After finding
the winner I could also sort the files by dates...

So there, I fired up python interpreter, found pyexiv2 module
and started tinkering.
