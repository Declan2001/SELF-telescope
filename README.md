# SELF-telescope

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
