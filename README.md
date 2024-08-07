# SELF-telescope

## Zemax
- ZPL: Zemax Macros
- ZOS: Zemax lens data
- ZDA and CFG: I do not fully know, but added them here for completetion, but I have never needed them. The ZDA file seems to act very similarly to the ZOS file
- ZIP: folder contains all the data I am using in the python program

### Open Zemax:
1) Open ANSYS License Management Center
- App on the computer so use windows key and search
- Click start (if takes more than 1 min then it is stuck in a loop restart the app and try again) (happens a lot :/ )
2) Open Ansys Zemax Optics Studio
- Open a file; locate yellow folder in very top left corner
- You are in the wrong folder, go back one folder to Zemax, then locate Declan/SELF_decenter/SELF-decenter.zos
3) You should see the lens data and the lens layout graphic
- If you don't see the lens layout graphic go to the "Analysis" tab and click 3D Viewer (NOT cross section that is 2D)
4) Lens layout Graphic
- In the lens layout graphic if you right click then you can fix the rotation if it is messed up
- If there is a zooming error, click the black circle with white arrow in it on the toolbar tab within the 3D layout window
- There is a rotate, a zoom, and a panning feature

### Zemax Macros usage
1) Go to the "Programming" tab
2) Click edit/run
3) Choose the correct file
- Choose "SELF-MultiRayTrace.ZPL"
- I named all of my files SELF-*
4) If you want to edit it or see the code click "Edit" or just click "Execute" to run the code
5) This will save code to "C:\Users\MorphUser\Documents\Zemax\Declan\SELF_RAYTRACE_DATA"
- sometimes it will not overwrite files if they are already there so I usually delete all the contents of the folder first then run the code
6) Next I send this to where ever my Python code can get a hold of it
- For me that is zipping the file and emailing it to myself so my other computer can get to it

### Zemax Macro explained
1) The code itself for MultiRayTrace is pretty well documented. It can always be supplemented by using the "Macros Help" under the "Programming" tab. 
2) The purpose of the code is to perform multiple raytraces over vary parameters. For example, the tip angle of the subaperture of M2 can be changed.
3) All the features of the code that need to be changed are at the top: radius, step_size, deg, deg_step would be the only parameters I would change
4) The other feature that can be changed is the "OUTPUT file$" which can be toggled on and off by making it a comment or not. This just says if it should be printed to the screen or to the file.

### Miscellaneous 
1) If image plane not at correct location
- first make sure there is no tip/decenter on ellipse (M2) so double click on "standard" for surface 6 in the lens diagram, go to "Tilt/Decenter" tab and make sure before AND after are all set to zero
- return to the original lens table and change the thickness of ellipse to "1292" then go to the "Optimize" tab and click "Quick Focus" this should then focus the image plane. For me it gets it to 1e-7 clear semi diameter for the image plane

### ZEMAX CODE ISSUE! 
- When the tip is performed it is changing the z location of the image plane by a slight amount
- This is bad for when we need to add images together
- Since M2 has no piston features (in the SELF Telescope itself) it cannot be decentered in the z to fix for this issue

### Python File: "spot_diagram.py"
1) The code takes in the output from the Zemax ZPL file. There is a different file for each tip angle. It works in blocks of information. For example a block is:

Local Ap -250.0000000000 0.0000000000 0.0000000000
Local El 9.8299302380 -58.9795978291 18.8866102460
Local Img -0.0038810375 0.0885535298 0.0000000000
OPL 4742.6594111599

with two additional lines at the beginning of each file stating the tip/tilt/decenter and the effective focal length at that configuration
2) This python file will create a globally located spot diagram. Unlike Zemax spot diagram it will not put (0,0) of the image plane at the center of the ray bundle, instead it uses the global (0,0) of the image plane
3) It will also compute the Airy Disk (black ring) based off of the Effective Focal Length given by Zemax for each orientation of M2 (elliptical mirror)
4) It will compute the center of the spot diagram with a red dot

If you want to plot the aperture graph add the extra flag in plotting_rays function
- easily can be done for ellipse too if you follow same code format of aperture code (not done yet, but could be easiy done)


## Fiber Experiment
### Data location:
https://drive.google.com/drive/folders/1X3GkPLBTcU9meeKVs4_gVvm9rrM2DzEU?usp=drive_link 
- if cannot access please email: declanbaker01@gmail.com and be descriptive :)

### Useful Paper:
- Link to paper on the concept (they used a different method) (SLM cost 20K+):

### IDEA:
The idea of this experiment was to see if collimated light through a fiber optic wire could be recontructed to figure out where the point source came from. 

### SETUP:
In order to do this I fixed the wire and put one end to receive a laser and the other end to a microscope. The end with a microscope had a camera on it thus allowing us to document what the speckle pattern looked like. 

### PROCESS:
On two separate days 7/5 and 7/10 I took full length range of dataset from where the spot was all the way on the left to all the way on the right, only moving one axis. After on 7/10 I took another set of data at random points, referred to as mystery pictures or "m" in the documentation. There known values were recorded by hand and are in the name of each picture just like the rest of the pictures. When running the code. After this I created a code that took the two separate full datasets and compared them to the mystery pictures to see if the least squares model aligned to the same location on both. Look at the graphs provided

### RESULT:
The PSM seemed not to align in any helpful manner, but the AMSCOPE camera pictures of the speckle patterns seem promising. They are close.
!!!!!!!!!!!!!VERY IMPORTANT CAVEAT!!!!!!!!!!!!: 7/5 to 7/10 the setup of the fiber shifted slightly due to vibrations and life I guess. But the important part is that the middle of the speckle part was not at the same location on the z axis for both days. Thus when comparing the mystery pictures (taken on 7/10) to 7/5 there is a correction factor added. This was done with my eye, so is very susceptible to human error. However, when compared to 7/10 dataset there is no correction factor. This could be the reason why the data for 7/10 matches closer to the mystery pictures than 7/5 dataset does.

### GRAPHS: 

