# -*- coding: utf-8 -*-
"""Task2.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15XH-TJzfIpMTnGhLaXcaFKDLPeagC07g
"""

from IPython.lib.pretty import Printable
from skimage import data,metrics # for inbuilt images
from skimage.color import * # for rgb2gray
from skimage.feature import *
import matplotlib.pyplot as plt
import numpy as np
import skimage.io
import math

def convolution(image,kernal):

    #height and width of input image
    height_img=image.shape[0]
    width_img=image.shape[1]

    #height and width of kernal
    height_kernal=kernal.shape[0]
    width_kernal=kernal.shape[1]

    n=height_kernal//2
    m=width_kernal//2

    #padding the image so out of bounds doesn't occur
    padded_img=np.pad(image,pad_width=((n,n),(m,m)),mode='constant',constant_values=0).astype(np.float32) 
    image_new=np.zeros(padded_img.shape)  

    image_final=np.zeros((height_img+2*n,width_img+2*m),np.float32)

    new_height=image_new.shape[0]
    new_width=image_new.shape[1]

    for i in range(n,new_height-n):
        for j in range(m,new_width-m):
            #slicing the required part
            sliced_img=padded_img[i-n:i-n+height_kernal,j-m:j-m+width_kernal]
            sliced_img=sliced_img.flatten()*kernal.flatten()
            image_final[i][j]=sliced_img.sum()
    
    return image_final[n:n+height_img,m:m+width_img]

def BlurOrNot():

    #laplacian matrix
    l_mat=np.zeros((3,3),np.float32)
    l_mat[0][0]=0
    l_mat[0][1]=1
    l_mat[0][2]=0
    l_mat[1][0]=1
    l_mat[1][1]=-4
    l_mat[1][2]=1
    l_mat[2][0]=0
    l_mat[2][1]=1
    l_mat[2][2]=0
    
    mi=1000
    mx=-1
    sum=0
    #calculation of variance of all sample images 
    for i in range (1,11):
        input_img=skimage.io.imread(str(i)+".jpg")
        image=rgb2gray(input_img)
        image=np.asarray(image)
        convo_output=convolution(image,l_mat)
        #calcution of variance of convolved output and laplacian matrix
        convo_variance=np.var(convo_output,dtype=np.float32)
        mi=min(mi,convo_variance)
        mx=max(mx,convo_variance)
        sum=sum+convo_variance

    #calculating the average varinace        
    average_var=sum/10.0

    #taking input file
    file_name=input("please Enter the file name : ")
    st_img=skimage.io.imread(file_name)

    image=rgb2gray(st_img)
    image=np.asarray(image)
    convo_output=convolution(image,l_mat)
    #calculating the variance of input image
    std_variance=np.var(convo_output,dtype=np.float32)

    #calculating the probaility of image to be blur
    output=0
    if std_variance<=mi:
        output=1
    elif std_variance>=mx:
        output=0
    elif std_variance>=mi and std_variance<=average_var:
        output=1-((0.5*(mi-std_variance))/(mi-average_var))   
    elif std_variance>=average_var and std_variance<=mx:
        output=(0.5*(std_variance-mx)/(average_var-mx))  

    print("The probability of image being blurred : ",output)

BlurOrNot()

