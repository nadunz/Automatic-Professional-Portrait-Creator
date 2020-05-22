import PIL
from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2 as cv
import colorsys

def imageprocess(y,x,gap,inURL,outURL,file,color):
    imageURL = inURL +"/"+ file
    #get top position
    image= Image.open(imageURL)
    color_original=image.getpixel((2, 2))
    h,s,l = colorsys.rgb_to_hls(color_original[0]/255,color_original[1]/255,color_original[2]/255)
    color_original1=(h*239,s*240,l*240)
    X, Y = image.size
    grey = image.convert("L")
    #give threshhold to image
    thresh_value=180
    bw = grey.point(lambda x: 0 if x<thresh_value else 255, '1')
    i=0
    j=0
    topPositionX1=0
    topPositionX2=0
    topPositionX=0
    topPositionY=0
    top_found=False
    top_found_over=False;
    while i<Y and not top_found :
        while j<X and not top_found_over :
            pixel = bw.getpixel((j, i))
            if pixel==0 and not top_found:
                topPositionX1=j
                topPositionY=i
                top_found=True
            if top_found:
                if pixel==255:
                    topPositionX2=j-1
                    topPositionX=int((topPositionX1+topPositionX2)/2)
                    top_found_over=True;
                    
            j=j+1
        i=i+1
        j=0

    #Get face height and width using openCV
    H = 0;
    W = 0;
    x_f=0; #face position
    y_f=0; #face position
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv.imread(imageURL)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x1,y1,w,h) in faces:
        H=h+(y1-topPositionY)
        W=w
        x_f=x1
        y_f=topPositionY
  
    #resizing
    resize_ratio = (26*y) / (45*H)  #26,27 for FeeLs #33 for Passport
    height = int(resize_ratio*Y)
    width = int(resize_ratio*X)
    image = image.resize((width, height), PIL.Image.ANTIALIAS)

    #crop
    crop_x1=resize_ratio*x_f-((x-int(resize_ratio*W))/2)
    crop_y1=resize_ratio*y_f-((y-int(resize_ratio*H))/3)
    crop_x2=crop_x1+x
    crop_y2=crop_y1+y

    area = (crop_x1, crop_y1, crop_x2, crop_y2)
    croped = image.crop(area)

    #####Color Replacing
    grey = croped.convert("L")
    #give threshhold to image
    #grey.save(outURL +"/grey"+ file)
    thresh_value=180
    bw = grey.point(lambda x: 0 if x<thresh_value else 255, '1')
    #bw.save(outURL +"/bw"+ file)
    #get new top positions after resizings
    i=((y-int(resize_ratio*H))/3)-5
    j=0
    topPositionX1=0
    topPositionX2=0
    topPositionX=0
    topPositionY=0 
    top_found=False
    top_found_over=False;
    while i<y and not top_found :
        while j<x and not top_found_over :
            pixel = bw.getpixel((j, i))
            if pixel==0 and not top_found:
                topPositionX1=j
                topPositionY=i
                top_found=True
            if top_found:
                if pixel==255:
                    topPositionX2=j-1
                    topPositionX=int((topPositionX1+topPositionX2)/2)
                    top_found_over=True;
                    
            j=j+1
        i=i+1
        j=0

    ##start replacing
    #create new colord plain image
    offset=17
    image = Image.new("RGB", (x, y), (int(color[0]),int(color[1]),int(color[2])))
    img=image.load()
    found_border=False
    i=topPositionY-4
    j=0
    old_pixel=grey.getpixel((j, i))
    while i<y :
        while j<topPositionX:
            pixel = grey.getpixel((j, i))
            pixel_im = croped.getpixel((j, i))
            if found_border:
                img[j,i]=pixel_im
            elif abs(pixel-old_pixel)<=offset:
                img[j,i]=(int(color[0]),int(color[1]),int(color[2]))
            elif abs(pixel-old_pixel)>offset and not found_border:
                found_border =True
                img[j,i]=pixel_im
            j=j+1
        i=i+1
        j=0
        found_border=False
    i=topPositionY-4
    j=x-1
    found_border=False
    while i<y :
        while j>=topPositionX:
            pixel = grey.getpixel((j, i))
            pixel_im = croped.getpixel((j, i))
            if found_border:
                img[j,i]=pixel_im
            elif abs(pixel-old_pixel)<=offset:
                img[j,i]=(int(color[0]),int(color[1]),int(color[2]))
            elif abs(pixel-old_pixel)>offset and not found_border:
                found_border =True
                img[j,i]=pixel_im
            j=j-1
        i=i+1
        j=x-1
        found_border=False
    image.save(outURL +"/"+ file)

