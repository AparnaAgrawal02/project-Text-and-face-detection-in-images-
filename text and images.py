#!/usr/bin/env python
# coding: utf-8

# # The Project #
# 1. This is a project with minimal scaffolding. Expect to use the the discussion forums to gain insights! It’s not cheating to ask others for opinions or perspectives!
# 2. Be inquisitive, try out new things.
# 3. Use the previous modules for insights into how to complete the functions! You'll have to combine Pillow, OpenCV, and Pytesseract
# 4. There are hints provided in Coursera, feel free to explore the hints if needed. Each hint provide progressively more details on how to solve the issue. This project is intended to be comprehensive and difficult if you do it without the hints.
# 
# ### The Assignment ###
# Take a [ZIP file](https://en.wikipedia.org/wiki/Zip_(file_format)) of images and process them, using a [library built into python](https://docs.python.org/3/library/zipfile.html) that you need to learn how to use. A ZIP file takes several different files and compresses them, thus saving space, into one single file. The files in the ZIP file we provide are newspaper images (like you saw in week 3). Your task is to write python code which allows one to search through the images looking for the occurrences of keywords and faces. E.g. if you search for "pizza" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions "pizza". This will test your ability to learn a new ([library](https://docs.python.org/3/library/zipfile.html)), your ability to use OpenCV to detect faces, your ability to use tesseract to do optical character recognition, and your ability to use PIL to composite images together into contact sheets.
# 
# Each page of the newspapers is saved as a single PNG image in a file called [images.zip](./readonly/images.zip). These newspapers are in english, and contain a variety of stories, advertisements and images. Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use [small_img.zip](./readonly/small_img.zip) for testing.
# 
# Here's an example of the output expected. Using the [small_img.zip](./readonly/small_img.zip) file, if I search for the string "Christopher" I should see the following image:
# ![Christopher Search](./readonly/small_project.png)
# If I were to use the [images.zip](./readonly/images.zip) file and search for "Mark" I should see the following image (note that there are times when there are no faces on a page, but a word is found!):
# ![Mark Search](./readonly/large_project.png)
# 
# Note: That big file can take some time to process - for me it took nearly ten minutes! Use the small one for testing.

# In[12]:


import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np



import zipfile
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np
from PIL import ImageDraw
# loading the face detection classifier
face_cascade = cv.CascadeClassifier(
    'readonly/haarcascade_frontalface_default.xml')
images = "readonly/images.zip"


def get_images_from_zipfile(t):
    img_dict={}
    with zipfile.ZipFile(t) as myzip:
        for file in myzip.infolist():
            with myzip.open(file.filename) as myfile:
                img = Image.open(myfile).convert("RGB")
                img_dict[file.filename] = img
    return img_dict  


def detect_faces(image):
    CV_image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
    return face_cascade.detectMultiScale(CV_image, scaleFactor=1.3, minNeighbors=5)


def create_contact_sheet(img_lst):
    first_img = img_lst[0]
    img_num = len(img_lst)
    return Image.new(first_img.mode, (first_img.width*5, first_img.height*(img_num//5+1)))
def add_to_contact_sheet(img_lst, contact_sheet, x, y): 
    for img in img_lst:        
        contact_sheet.paste(img, (x,y))
        x += 100        
        if x == 500:            
            x = 0            
            y = 100
    return contact_sheet
name = input("Enter name to search for: ").lower().capitalize()
ret = get_images_from_zipfile(images)
for k, v in img_dict.items():
    text = pytesseract.image_to_string(v)
    if name in text:
        print("Results found in file {}".format(k))
        faces_rect = detect_faces(v)
        if len(faces_rect) == 0:
            print("\n")
            print("But there were no faces in that file!")
            continue
        img_list = []
        for (x, y, w, h) in faces_rect:
            cropped_img = v.crop((x,y,x+w,y+h))
            cropped_img.thumbnail((100,100))
            img_list.append(cropped_img)
        m = 0
        n = 0
        contact_sheet = create_contact_sheet(img_list)
        contact_sheet = add_to_contact_sheet(img_list, contact_sheet, m, n)
        display(contact_sheet)    


# In[ ]:




