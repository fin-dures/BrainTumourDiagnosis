from PIL import Image
import PIL
import tkinter
from tkinter import filedialog

def files_select():

    FILE_TYPES = ["jpg", "jpeg", "bmp", "tiff", "pdf"]
    temp=tkinter.Tk()
    
    filenames=None
    valid = False
    while not valid:
        filenames = tkinter.filedialog.askopenfilenames()
        
        if filenames!=None:
            valid = True
        for file in filenames:
            file_valid = False
            for filetype in FILE_TYPES:
                if filetype in file:
                    file_valid = True
            if not file_valid:
                valid = False

        
    try:
        temp.destroy()
    except:
        pass
        
    
    return filenames

def file_select():
    FILE_TYPES = ["jpg", "jpeg", "bmp", "tiff", "pdf"]
    
    temp=tkinter.Tk()
    filename=None
    valid = False
    while not valid:
        filename = tkinter.filedialog.askopenfilename()
        for filetype in FILE_TYPES:
            if filetype in filename:
                valid = True

    try:
        temp.destroy()
    except:
        pass
        
    return filename

def get_image_vector(file_name, x_res, y_res):
    
    image=Image.open(file_name)
    image=image.resize((x_res, y_res))
    
    rgb_pixels = list(image.getdata())
    pixels=[]

    #some images are already in greyscale format whereas some aren't
    for rgb in rgb_pixels:
        
        if type(rgb) == tuple:
            pixels.append(rgb[0]/10+1)
        else:
            pixels.append(rgb/10)


    return pixels

def get_image_matrix(x_res, y_res):
    image_list=files_select()
    matrix=[]
    for filename in image_list:
        vector=get_image_vector(filename, x_res, y_res)
        matrix.append(vector)

    return matrix

def get_single_image(x_res, y_res):
    image = file_select()
    vector=get_image_vector(image, x_res, y_res)
    return vector

def save_value(value, filepath):
    with open(filepath, "w") as file:

        file.write(str(value))

def save_matrix(matrix, filepath):

    with open(filepath, "w") as file:
        
        for vector in matrix:

            for number in vector:
                file.write(str(number))
                file.write(",")


            file.write("\n")
        

def load_value(filepath):
    with open(filepath, "r") as file:
        return float(file.read())

def load_matrix(filepath):

    matrix=[]

    with open(filepath, "r") as file:
        for line in file:
            split_line = line.split(",")
            split_line.pop()

            split_line = list(map(float, split_line))
            matrix.append(split_line)
            

    return matrix







    

