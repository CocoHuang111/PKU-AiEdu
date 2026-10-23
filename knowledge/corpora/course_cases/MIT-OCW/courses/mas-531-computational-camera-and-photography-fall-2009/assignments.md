- Source: https://ocw.mit.edu/courses/mas-531-computational-camera-and-photography-fall-2009/pages/assignments/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Assignments

This page describes the four homework assignments for the class. The final project with some example student work is presented on the [projects](https://ocw.mit.edu/courses/mas-531-computational-camera-and-photography-fall-2009/pages/projects/) page.

Graduate students (enrolled in MAS.531) will complete four homework assignments, while undergraduates (enrolled in MAS.131) will complete the first three of these assignments.

Students are encouraged to program in MATLAB® for image analysis. C++, OpenGL and visual programming may be needed for some hardware assignments.

The [MAS.131/MAS.531 Flickr group pool](http://www.flickr.com/groups/1233829@N23/) contains some images produced by students for the assignments and final project.

### Homework 1: Relighting

Combine two photos by mixing the color channels. Take multiple photos by changing lighting and other parameters. Be creative. Then mix and match color channels to relight.

You can use these for inspiration:

- Haeberli, Paul. [*Synthetic Lighting for Photography*](http://www.graficaobscura.com/synth/index.html). January, 1992.
- Raskar, Ramesh, Adrian Ilie, and Jingyi Yu. [*Image Fusion for Context Enhancement and Video Surrealism*](http://web.media.mit.edu/~raskar/NPAR04/). Presented at NPAR 2004.

MATLAB resources:

- Sigmon, Kermit. [*MATLAB Primer*](http://www.math.ucsd.edu/~bdriver/21d-s99/matlab-primer.html). 2nd ed., 1992.
- The MathWorks. [*Image Processing Toolbox*](http://www.mathworks.com/products/image/).

Create a Web page for all your homework assignments. The Web page for each assignment should at least have well commented source code, all input images, intermediate results and final output. Please include some description below each image.

Here is good example of how to assemble your homework into a Web page:

- “[The Vertigo Shot](http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15463-f08/www/proj0/www/fpalermo/)” from a Carnegie Mellon Computational Photography class (Fall 2008).

On your Webpage, you should have sourcecode and other details. Please include intermediate results, if any.

### Homework 2: Optics

Purpose: Playing with rays, lens, focus and creating see-through effects.

Select one of these three sub-assignments, based on your background and interests.

- Assignment 2A: Virtual Optical Bench: Modify software to shoot rays
- Assignment 2B: Lightfield Photography: Take photos, shift each photo and average (using Photoshop/HDRshop/Matlab/OpenCV/Flash/Java, whatever you like)
- Assignment 2C: Same as 2B but render input photos in software

#### Assignment 2A. Virtual Optical Bench

We will study how rays can be propagated thru free space and optical elements. The basic idea is simple. Each ray is four dimensional: it has a position (x,y) + angle (theta, phi). For each element (free space, lens, mirror etc), there is a simple formula to ’transfer’ the ray into a new ray:

- Wikipedia: [Ray transfer matrix analysis](http://en.wikipedia.org/wiki/Ray_transfer_matrix_analysis).

Part 1

Use ray-matrix operations and the ‘ray’ class to create an interface similar to Andrew Adam’s [LensToy software](http://graphics.stanford.edu/~abadams/lenstoy.swf). (Opens a Shockwave file, requires Adobe Flash Player)

You can directly start with his software or write your own in OpenGL or MATLAB.

Then add new elements such as (i) prism (ii) lenslet (iii) ability to change focal length of lens etc.

Part 2

The LensToy only draws rays but does not form an intensity image.

Create images of 3D and 2D objects. To compute intensity at a point, you have to add up radiance of all rays incident at that point. Show effects like depth of field using aperture or capture lightfield by selectively blocking the aperture.

#### Assignment 2B: Lightfield Photography

Please read the Lightfield Camera papers very carefully.

- Bennett, W., et al. “[High Performance Imaging Using Large Camera Arrays](http://graphics.stanford.edu/papers/CameraArray/).” 2005.

Digital refocusing using photos taken by an array of cameras is easy. If you compute an average of all the photos, the digital focus is at infinity. If you shift each photo cumulatively, e.g. shift each photo a pixel with respect to its immediate left neighbor, and then compute an average, the focus plane is closer. This simple shift+add strategy is sufficient to achieve reasonable refocusing effects.

Part 1

Use only 16 images along the horizontal translation. You will test your code on this dataset.

Part 2

Translate camera and take photos at fixed distance intervals. Place the camera on a ruler (or create a Lego Robot) for precise positioning. You are trying to imitate a camera array. Ideally, control the camera using Remote Capture software from your computer. Take 16 photos. Choose objects with vibrant bright saturated colors. If you can’t think of a scene, try this. The foreground scene is a flat red colored paper with see through vertical stripes creating a FENCE. Background scene is a flat book cover or painting with very little red in it.

Part 3

Show refocusing and see-thru effects. See examples at the [Stanford Light Field Archive](http://lightfield.stanford.edu/index.html).

Submit all input images, source code and output for each item. Use high depth complexity, colorful, point specular (sphere) objects. To create multiple camera views, you can also aim at an array of mirrors, put the camera on a robot or x-y platform. Be creative with camera configurations, maybe with very large baseline or with a microscope. You can also use unstructured positions and use a calibration target (or structure from motion or Photosynth software) to find the positions.

More projects are described at the Stanford Computer Graphics Laboratory’s “[Light fields and computational photography](http://graphics.stanford.edu/projects/lightfield/)” page.

Other ways to create lightfields include:

- Flatbed scanner + lenticulars — See Yang, Jason C. “A Light Field Camera For Image Based Rendering.” Master’s Thesis, MIT, 2000. ([PDF - 1.7MB](http://groups.csail.mit.edu/graphics/pubs/thesis_jcyang.pdf))
- Masks — See Veeraraghavan, A., et al. “[Dappled Photography: Mask Enhanced Cameras for Heterodyned Light Fields and Coded Aperture Refocusing](http://web.media.mit.edu/~raskar/Mask/).” ACM SIGGRAPH 2007.

#### Assignment 2C: Lightfield Photography (same as 2B) but with Input Photos Rendered in Software

Part 1: Programmable focus

Compute images with plane of focus at different depth (shift each photo by a specific amount successively and compute an average).

Output 1: Digitally focus at infinity (average of all photos)

Output 2: Digitally focus on back plane (shift some and average)

Output 3: Digitally focus on front plane (shift more and average)

This is the key part of this assignment: The Output2 should demonstrate a see-thru effect.

Part 2: Extra Credit and Completely Optional

Find depth of each pixel using max-contrast operator.

Produce see-through effect by eliminating foreground color pixels. For rejecting a given plane, instead of taking average of 16 values, take the majority vote. Median of 16 values will work in some cases, but the most common value will be a more robust choice. If there is no clear majority, i.e. if the most common count is say below 5, set the pixel to black.

Compute images with variable depth of field (Use fewer photos picked from near the center position. Fewer photos means a larger depth of field.)

Compute images with slanted plane of focus.

- Wikipedia [Scheimpflug principle](http://en.wikipedia.org/wiki/Scheimpflug_principle).
- Vaish, Vaibhav, et al. “[Synthetic Aperture Focusing using a Shear-Warp Factorization of the Viewing Transform](http://graphics.stanford.edu/papers/shear-warp/).” A3DISS (at CVPR), 2005.

Create new bokeh (point spread function).

### Homework 3: Human Computer Interaction (HCI) using Multi-Flash Camera

Track hand or finger using shadows from colored RGB lights, video camera.

Most of source code is available online; you will have to modify for your task. ([GZ](https://web.media.mit.edu/~raskar/NprCamera/Slides/MoreCode/NPRCameraSrc.tar.gz))

References

- [Kar-Han Tan’s Web site](http://karhantan.com/)
- Raskar, R., K-H Tan, R. Feris, J. Yu, and M. Turk. “[Non-photorealistic Camera: Depth Edge Detection and Stylized Rendering using Multi-Flash Imaging](http://web.media.mit.edu/~raskar/NprCamera/).” *Proceedings of ACM SIGGRAPH*, August 2004. [Includes source code]
- [Rogiero Feris’ Web site](http://rogerioferis.com/)
- Vaquero, D., R. Feris, M. Turk, and R. Raskar. “[Multiflash Imaging and Applications](https://web.archive.org/web/20150322033216/http://ilab.cs.ucsb.edu/index.php/component/content/article/12/58).”

Part 1:

- Turn on 1 LED at a time, take 3 (or 4) photos
- Find silhouette from shadow
- Do region filling to indicate (render) hand against textured background on table

Part 2:

- Turn on 3 LEDs: R, G, B
- From one photo, decompose 3 photos using RGB channels
- Find shadows, do region filling and find foreground

Extra credit:

- Let two hands overlap, find internal silhouettes (i.e. boundary between two hands), indicate the two hands in different color in rendering
- On table, have printed photos of hand (so ordinary camera will be confused) or other crazy texture

### Homework 4: Multispectral Imaging

#### Option 1: Open ended

Your own choice … send me an email to get the approval. You can do some background work for your final project as HW 4 but this should be sufficiently different from your final project.

#### Option 2: Wavelength and Color

You will use a multi-spectral database and create the appearance of objects under light sources with given color profiles.

| STEPS | DESCRIPTIONS | RESOURCES |
| --- | --- | --- |
| Step 1 | Recover multiple wavelength bands of a scene (using online database) | [CAVE Multispectral Image Database](http://www1.cs.columbia.edu/CAVE/databases/multispectral/) <br> with 31 bands <br> You should try on at least 2 datasets among the 5 sections of this set: <br> Lemon slices (and color chart) from the section “ [Real and Fake](http://www1.cs.columbia.edu/CAVE/databases/multispectral/real_and_fake/) ” <br> One other set of your choice |
| Step 2 | Get the wavelength profile of at least two light sources (e.g. mercury vapor and sunlight), using curves available online or computing the curve yourself using a spectroscope) | Instructions to build your own spectroscope: Turricchia, A., and A. Majcher. “Amateur spectroscope.” ( <br> [PDF](https://www.if.ufrgs.br/~fatima/fis2004/arquivos/spectroscope.pdf) <br> ) |
| Step 3 | Multiply each band of scene with corresponding intensity of light source in that band | Graph of human eye spectral sensitivity, to estimate “red,” “green,” and “blue” target values ( <br> [JPG](http://www.normankoren.com/Human_spectral_sensitivity_small.jpg) <br> ) <br> More about eye response: Koren, N. “ <br> [Color management and color science: Introduction](http://www.normankoren.com/color_management.html) <br> ” |
| Step 4 | Create a weighted combination for ‘red’, ‘green’ and ‘blue’ target values |  |
| Step 5 | Render the colored scene |  |
| Extra credit | Create a Metamer (objects with two different wavelength profile that look the same in RGB under a light source with specific wavelength profile) | [Metamer applet](http://www.cs.brown.edu/exploratories/freeSoftware/repository/edu/brown/cs/exploratories/applets/spectrum/metamers_java_browser.html) |
