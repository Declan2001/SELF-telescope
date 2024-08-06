import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def all(dad_folder, son_folder):
    base_path = "C:\\Users\\decla\\Documents\\DECLAN\\Jeff_Kuhn_Hawaii\\FiberOptics\\"
    ref_path = dad_folder + son_folder
    mystery_path = dad_folder + "mystery\\"

    # setting up initials
    if dad_folder == "amscope\\":
        mystery_files = ["z-31.0-m.jpg", "z-31.5-m.jpg", "z-34.5-m.jpg", "z-37.0-m.jpg", "z-39.0-m.jpg"]
    elif dad_folder == "psm\\":
        mystery_files = ["z-31.0-m.png", "z-31.5-m.png", "z-34.5-m.png", "z-37.0-m.png", "z-39.0-m.png"]
    else:
        print(f"No folder data for dad_folder name: {dad_folder}")
        return
    
    if son_folder == "7-10-24\\":
        starting_num = 29.5                     
        num_of_pics = 22
        dif = 0                     # this is zero because mysterty pics taken same day 
    elif son_folder == "7-5-24\\":    
        starting_num = 33                     
        num_of_pics = 20
        dif = 3                     # this is the recalibration number (done by eye) [7-5-24: 37.5, 7-10-24:34.5]
    else:
        print(f"No folder data for son_folder name: {son_folder}")
        return

    # statisitcal analysis 
    def calc_mse(pix_arr1, pix_arr2):
        return np.mean((pix_arr1 - pix_arr2)**2)
    def calc_least_squares(pix_arr1, pix_arr2):
        return np.sum((pix_arr1 - pix_arr2)**2)

    # open image and make np array
    def image2array(folder, file):
        image = Image.open(base_path + folder + file)
        pixels = np.array(image)
        return pixels

    def search_ref_img(image):
        # Finding which image matches the closest
        for i in range(len(reference_images)):
            ref = reference_images[i]
            if image.shape != ref.shape:
                print("Sizes do not match")
                print("Mystery size: ", image.shape, "Reference Image index and shape: ", i, reference_images[i].shape)
            if i == 0:
                stat_method = calc_least_squares(ref, image)
                which_ref = i
            else:
                new_stat_method = calc_least_squares(ref, image)
                if new_stat_method < stat_method:
                    stat_method = new_stat_method
                    which_ref = i
        return which_ref, stat_method

    # Plotting param according to statistical analysis
    def plot_mse_param(image):
        mse_list = [calc_mse(ref,image) if image.shape == ref.shape else print("Sizes do not match") for ref in reference_images]
        counter = [i*0.5+starting_num for i in range(len(mse_list))]
        return mse_list, counter
    def plot_least_squares_param(image):
        least_squares_list = [calc_least_squares(ref,image) if image.shape == ref.shape else print("Sizes do not match") for ref in reference_images]
        counter = [i*0.5+starting_num for i in range(len(least_squares_list))]
        return least_squares_list, counter

    # Convert title into a int to do math and cut then back to a string
    def stringify(image_name, dif):
        if "m" not in image_name:
            return float(image_name[2:6])
        else:
            return float(image_name[2:6]) + dif

    # setup reference images
    reference_images = []
    ref_img_name = []
    for i in range(0, num_of_pics):
        num = starting_num + i*0.5
        if dad_folder == "amscope\\":
            file = f"z-{num}.jpg"
        elif dad_folder == "psm\\":
            file = f"z-{num}.png"
        reference_images.append(image2array(ref_path, file))
        ref_img_name.append(file)

    # Image with unknown coordinates
    mystery = [image2array(mystery_path, file) for file in mystery_files]

    # Display the image using matplotlib

    cols = 2  # Number of columns you want in your subplot grid
    rows = (len(mystery) + cols - 1) // cols  # Calculate the number of rows needed
    fig, axs = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    count = 0
    #print(f"Reference Path: {ref_path}")
    for pic in mystery:
        fig.suptitle(f'{ref_path}')
        which_index, least_squares_value = search_ref_img(pic)
        # print("Mystery:", stringify(mystery_files[count], dif), "   Best matched reference image:", stringify(ref_img_name[which_index]), "   Mean Square Error", mse_value)
        # mse_list, index2 = plot_mse_param(pic)
        least_squares_list, index = plot_least_squares_param(pic)

        row_idx = count // cols
        col_idx = count % cols

        #axs[row_idx, col_idx].scatter(index, mse_list)
        axs[row_idx, col_idx].scatter(index, least_squares_list)
        #axs[row_idx, col_idx].scatter(which_index+starting_num, mse_value, color='red', marker='o')
        axs[row_idx, col_idx].scatter(index[which_index], least_squares_value, color='red', marker='o')
        axs[row_idx, col_idx].axvline(stringify(mystery_files[count], dif), color='blue', linestyle = "--")
        axs[row_idx, col_idx].set_title(f'Plot {count + 1}: {stringify(mystery_files[count], dif)}')
        axs[row_idx, col_idx].set_xlabel('Ref Image')
        axs[row_idx, col_idx].set_ylabel('Least Squares')  
        axs[row_idx, col_idx].legend(['Calculated Least Squares', 'Best Calculated Value', 'Correct Mystery Number'])
        count += 1  

    # Hide any unused subplots
    for ax in axs.flat[count:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)  # Add more space between rows
    plt.savefig(base_path + f"{dad_folder[:-1]}" + "-" + f"{son_folder[:-1]}")
    return

all("amscope\\", "7-5-24\\")
all("amscope\\", "7-10-24\\")
all("psm\\", "7-5-24\\")
all("psm\\", "7-10-24\\")



"""
Notes:
recalibration number (done by eye) [7-5-24: 37.5, 7-10-24:34.5]
mysterty pics taken 7-10-24

Why MSE was chosen: 
Simplicity: MSE is straightforward to compute and understand.
Effectiveness: MSE measures the average squared difference between corresponding pixel values of two images, making it effective for identifying overall similarity.
Common Use: Widely used in image processing and machine learning for evaluating the quality of reconstructed images.

Conclusion:
Amscope has a lot of potential to be reliable
PSM does not seem to be reliable due to it being a circle output
"""

# least squares fit or mse
    # difference is at the end do you sum or do you take the mean

# make graph
# look for objective lens - in box or around in general
# write-up 
    # pics of setup
    # graph
    # procedure
    # no more psm

# Least squares
# a_i = (sum_of_pixels(f_i * mystery_function))/sum(f_i**2)
#     if mystery_func = f_i get one