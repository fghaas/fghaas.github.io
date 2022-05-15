Title: Batch-processing stereograms with StereoscoPy
Date: 2022-05-15 21:00
Slug: batch-process-stereo
Summary: I often need to process stereograms in bulk. A Python tool named StereoscoPy is very handy in doing that.

![My camera with the Loreo 40mm stereoscopic lens attached (cross-view stereo image)](/images/loreo-stereo-lens.jpg)

I have two methods of taking stereoscopic images, both of which I use
regularly:

* The “left foot, right foot” method, which I can do with any camera,
  including that on my smart phone (I covered this method at length
  [in my 2021 FrOSCon
  talk]({filename}../presentations/froscon2021.md)). This is the method
  I prefer when doing stereograms of landscapes, buildings, statues
  and such like, and also what works very well for posed stereo
  portraits.

* My [Loreo stereoscopic
  lens](http://www.loreo.com/pages/products/loreo_3dlenscap9005-43_spec.html),
  shown in the picture above attached to my camera.

Either way, I need to post-process my images to get cross-view
stereograms like the one you’re seeing here.

In the former case the need is obvious: I start with two images and
need to make them into one stereogram.

In the latter case, it’s perhaps less so: my stereo lens obviously
already produces a stereogram, but it’s a wall-eyed one (which I’m not
particularly good at viewing), and it has an area in the centre of the
frame where the two images slightly overlap. I have found this area to
be about 6% of the total width of the image. So that means that what I
need to do, starting with the original stereo image, is this:

* Split the original image into two halves.
* Cut off 3% on the left and right of each image — on one side, that
  crop removes the overlap; on the other, it restores symmetry.
* Swap the sides of the image: the originally left side goes right,
  the right side goes left.
* For easier viewing, add a divider, and a border.

What comes in very handy here is a neat little tool:
[StereoscoPy](https://github.com/2sh/StereoscoPy) is a small Python
library and CLI that is helpful in batch-processing stereo images.

In combination with `convert` from
[ImageMagick](https://imagemagick.org/), this enables me to
batch-process a whole folder of stereo images into something that is
much more suitable for general consumption than the original images
that the Loreo lens produces.

```bash
#!/bin/bash

# Set the border/divider width, in pixels
BORDER=40

for f in *.JPG; do
    # Grab the file name, sans extension
    name=${f/.JPG/}

	# If the cross-view stereogram already exists, 
	# skip to the next original image
    if [ -e stereo/${name}-cross.jpg ]; then
       continue
    fi
	
    # Convert the wall-eyed stereogram foo.JPG 
	# into foo-0.jpg (left) and foo-1.jpg (right)
    convert $f -crop 50%x100% stereo/"${f%.JPG}".jpg
	
    # Create a cross-view image, with auto-alignment, 
	# that crops 3% off each side of the image, auto-aligns, 
	# and creates a border and divider
    StereoscoPy -x -A \
	  --div $BORDER --border $BORDER \
      -C 3% 0 3% 0 \
      stereo/${name}-0.jpg stereo/${name}-1.jpg \
      stereo/${name}-cross.jpg

    # Remove the intermediate images
    rm stereo/${name}-0.jpg stereo/${name}-1.jpg
done
```

Maybe I’ll eventually get round to submitting a patch to StereoscoPy
itself, so that the pre-processing step with `convert` is no longer
necessary and the little script above becomes an actual one-liner. But
for now this works okay for me.
