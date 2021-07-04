#!/usr/bin/env python3
#SkinDetection.py

# This program runs all 4 skin detection algorithms one after the other
# Run `python3 SkinDetection.py Path/To/Image` to specify
# inital image, removing this command arguements will result in
# the script attempting hard coded locations so errors may arise
# The 

from PIL import Image
import math
import colorsys
import sys

#Explicitly Defined Skin Region Model
def EDSRModel(image_path):
    im = Image.open(image_path)
    pixels = im.load()
    rgb_im = im.convert('RGB')
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r,g,b = rgb_im.getpixel((i,j))
            if r > 95 and g > 40 and b > 20 and  (max(r, g, b) - min(r, g, b)) > 15 and abs(r - g) > 15 and r > g and r > b:
                x = j
                y = i
            else: 
                pixels[i,j] = (0,0,0)

    im.save("Results/Explicitly-Defined-Skin-Region.png")

#Colour Segmentation in Normalization rg Color Model
def NormalizationrgModel(image_path):
    im = Image.open(image_path)
    pixels = im.load()   
    rgb_im = im.convert('RGB')
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r,g,b = rgb_im.getpixel((i,j))
            
            R = 0.0
            G = 0.0
            B = 0.0
            
            if r > 0 or g > 0 or b > 0:
                R = r/float(r+g+b)
                G = g/float(r+g+b)
                B = b/float(r+g+b)
            
            if 0.465 >= R >= 0.36 and 0.363 >= G >= 0.28:
                x = j
                y = i
            else: 
                pixels[i,j] = (0,0,0)

    im.save("Results/Normalizationrg.png")

#Color Segmentation in HSV Color Model 
def HSVModel(image_path):
    im = Image.open(image_path)
    pixels = im.load()   
    rgb_im = im.convert('RGB')
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            r,g,b = rgb_im.getpixel((i,j))
            
            r = r/255.0
            g = g/255.0
            b = b/255.0
            
            h,s,v = colorsys.rgb_to_hsv(r,g,b)
           
            h = h*255
            
            if 50 >= h >= 0 and 0.68 >= s >= 0.2 and 1 >= v >= 0.35:
                x = j
                y = i
            else: 
                pixels[i,j] = (0,0,0)

    im.save("Results/HSV.png")

#Color Segmentation in YCBCR Color Model
def YCBCRModel(image_path):
    im = Image.open(image_path)
    pixels = im.load()   
    ycbcr_im = im.convert('YCbCr')
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            y,Cb,Cr = ycbcr_im.getpixel((i,j))
            
            if 142.5 >= Cb >= 97.5 and 134 >= Cr >= 17:
                pixels[i,j] = (0,0,0)
            else: 
                x = i
                y = j

    im.save("Results/YCBCR.png")

def main():
    args = sys.argv[1:] 

    if len(sys.argv) == 1:
        image_path = "Images/skin.jpg"
    else:
        image_path = args[0]

    EDSRModel(image_path)
    NormalizationrgModel(image_path)
    HSVModel(image_path)
    YCBCRModel(image_path)
    return

if __name__ == "__main__":
    main()
