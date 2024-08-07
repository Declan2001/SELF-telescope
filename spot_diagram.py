import matplotlib.pyplot as plt
import numpy as np
import os

base_path = 'C:\\Users\\decla\\Documents\\DECLAN\\Jeff_Kuhn_Hawaii\\Zemax\\'                # you will have to change this to your file path
folder_path = "SELF_RAYTRACE_DATA"
wavelength = 0.000587 # millimeters
D = 500 #[mm] this is the M1 aperture diameter

def xyz_arrays(file_path):
    """Takes in the file and turns it into a dataframe consisting of the 'obj-x', 'obj-y', 'obj-z', 'img-x', 'img-y', 'img-z', 'OPL'
        It returns this dataframe and then also the tip/tilt/decenter values and effective focal length"""

    with open(base_path + folder_path + "\\" + file_path, 'r', encoding='utf-16') as file:
        TTP = file.readline().split()[2]                        # Tip/tilt/piston values
        EFL = file.readline().split()[1]                        # Effective focal length
        lines = file.readlines()                                # Read the rest of the lines from the file
        data = {'obj-x':[], 'obj-y':[], 'obj-z':[],
                'img-x':[], 'img-y':[], 'img-z':[],
                'OPL':[]}

        block_size = 4                                          # one raytrace has 4 lines of info then it is the next "block" of information
        for line in range(0, len(lines), block_size):
            block = lines[line:line + block_size]
            obj = block[0].split()
            img = block[2].split()
            OPL = block[3].split()[1]

            if (float(obj[2]) == 0.0000000000) & (float(obj[3])  == 0.0000000000):
                OPL_chief = float(OPL)                          # goes through the aperture stop at (x,y) = (0,0)
                print("CHIEF", OPL_chief)

            data['obj-x'].append(float(obj[2]))
            data['obj-y'].append(float(obj[3]))
            data['obj-z'].append(float(obj[4]))
            data['img-x'].append(float(img[2]))
            data['img-y'].append(float(img[3]))
            data['img-z'].append(float(img[4]))
            data['OPL'].append(float(OPL))

        data['OPL'] = [data['OPL'][i]-OPL_chief for i in range(0,len(data['OPL']))]         # subtracting the cheif ray from the other rays
    return data, TTP, EFL

def center(data):
    """This finds the center of the ray bundle and returns that obj-x, obj-y, img-x, and img-y value"""
    centers = [np.mean(data['obj-x']), np.mean(data['obj-y']), np.mean(data['img-x']), np.mean(data['img-y'])]
    return centers

def plotting_rays(data, centers, count, aperture_graph=False):
    """Plots the Airy disk, the rays, the center, and colors the rays based on their OPL subtracted from the Chief Ray OPL then divided by the wavelength to put it in units of wavelengths
        Has the additional feature of being able to plot the aperture stop graph to see where the rays are coming in from. This is a flag so it is off, but can be toggled on"""
    objx = data['obj-x']
    objy = data['obj-y']
    imgx = data['img-x']
    imgy = data['img-y']
    OPL = data['OPL']

    x_obj_cen, y_obj_cen, x_img_cen, y_img_cen = centers
    OPL_in_wavelengths = [value/wavelength for value in OPL]                # changing OPL to be in units of wavelength

    if aperture_graph:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
        ax1.scatter(objx,objy)
        ax1.scatter(x_obj_cen, y_obj_cen, color='red', marker='o')
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title('Objective Plane')

        sc = ax2.scatter(imgx, imgy, c=OPL_in_wavelengths, cmap='viridis', s=100)
        fig.colorbar(sc, ax=ax2, label="OPL minus Chief Ray OPL [wavelengths]")
        ax2.scatter(x_img_cen, y_img_cen, color='red', marker='o')
        ax2.plot(ADx1, ADy1, color='black')
        ax2.plot(ADx2, ADy2, color='black')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_title('Image Plane')

    else:
        fig, ax = plt.subplots(figsize=(10, 10))
        sc = ax.scatter(imgx, imgy, c=OPL_in_wavelengths, cmap='viridis', s=100)
        fig.colorbar(sc, ax=ax, label="OPL minus Chief Ray OPL [wavelengths]")
        ax.scatter(x_img_cen, y_img_cen, color='red', marker='o')
        ax.plot(ADx1, ADy1, color='black')
        ax.plot(ADx2, ADy2, color='black')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Image Plane')
        save_path = base_path + f"Graphs\\Tip\\{count}"
        # fig.savefig(f'{save_path}')                                                 # toggle this on if you want it to save the figs

    plt.show()
    return

def airy_disk(EFL):
    """Creates the Airy Disk based on the effective focal length, aperture diameter, and wavelength
        TIP: if there are little flanges at the end of the airy disk then just make the step_size finer to reduce their size"""
    ADx1, ADy1, ADx2, ADy2 = [], [], [], []
    EFL = np.abs(float(EFL))
    airy_disk_radius = 1.22*wavelength*EFL/D       # in millimeters
    step_size = airy_disk_radius/1000
    x_values = np.arange(-airy_disk_radius, airy_disk_radius+step_size, step_size)
    for i in x_values:
        ADy1.append(np.sqrt(np.abs(airy_disk_radius**2 - i**2)))
        ADx1.append(i)
        ADy2.append(-np.sqrt(np.abs(airy_disk_radius**2 - i**2)))
        ADx2.append(i)
    #plt.plot(ADx1, ADy1, color='black')
    #plt.plot(ADx2, ADy2, color='black')
    #plt.show()
    return ADx1, ADy1, ADx2, ADy2, airy_disk_radius

database = {
    'TTP': [], 'data':[], 'centers':[]
}


###### This runs the functions above ########
"""
If you want the full range of pictures uncomment the "for loop", comment out "file_name = ...", then indent all the rest of the lines so they are inside the for loop.
Be careful because this will give you multiple pictures. It will also take a while to compute. So this is used if you want to save the graphs. If you want to save the graphs go up the
"plotting_rays" function uncomment the save fig command (make sure pathing is correct) and comment out the "plt.show()" command or each image will pop up on the screen.

I suggest you leave it the way it is and just change what file you want to use for testing. Then when it is ready follow the instructions detailed above.
"""


count=0
#for file_name in os.listdir(base_path+folder_path): 
file_name = '-Tip0.0020000000-Tilt0.0000000000-Piston0.0000000000-Declan.txt'
data, TTP, EFL = xyz_arrays(file_name)
centers = center(data)
ADx1, ADy1, ADx2, ADy2, AD_radius = airy_disk(EFL)
plotting_rays(data, centers, count)

database['TTP'].append(TTP)
database['data'].append(data)
database['centers'].append(centers)
count+=1