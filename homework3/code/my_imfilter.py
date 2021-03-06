# -*- coding: utf-8 -*-
"""my_imfilter.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12iBCp6Mmnwu4ZJyKfJttsFuAwp2RZ51U
"""

# -*- coding: utf-8 -*-
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from scipy import misc
import cv2

def cross_correlation_2d(img,kernel):
	img_size = img.shape
	kernel_size = kernel.shape
	pad_h = kernel_size[0] // 2
	pad_w = kernel_size[1] // 2
	pad_img = np.pad(img,[(pad_h,pad_h),(pad_w,pad_w)],mode="constant",constant_values=0)
	pad_img_size = pad_img.shape
	output = np.zeros(img_size)
	for i in range(pad_h,pad_img_size[0]-pad_h):
		for j in range(pad_w,pad_img_size[1]-pad_w):
			temp = []
			for k in range(kernel_size[0]):
				for z in range(kernel_size[1]):
					temp.append(kernel[k][z] * pad_img[i-pad_h+k][j-pad_w+z])
			output[i-pad_h][j-pad_w] = sum(temp)
	return output

def isGray(img):
	if (len(img.shape) < 3):
		return True
	return False

def convolve_2d(img,kernel):	
	flipped_kernel = np.zeros(kernel.shape)
	for i in range(0,flipped_kernel.shape[0]):
		for j in range(0,flipped_kernel.shape[1]):
			flipped_kernel[i][j] = kernel[flipped_kernel.shape[0]-i-1][flipped_kernel.shape[1]-j-1]
	if (isGray(img)):
		return cross_correlation_2d(img,flipped_kernel)
	else:
		output = np.zeros(img.shape)
		output[:,:,0] = cross_correlation_2d(img[:,:,0],flipped_kernel)
		output[:,:,1] = cross_correlation_2d(img[:,:,1],flipped_kernel)
		output[:,:,2] = cross_correlation_2d(img[:,:,2],flipped_kernel)
		return output

def gaussian_blur_kernel_2d(sigma,size,size_y=None):
	if(size % 2 == 1):
		if not size_y:
			size_y = size
		x, y = np.mgrid[-size:size+1, -size_y:size_y+1]
		g = np.exp(-((x**2/float(size)+y**2/float(size_y))/(2 * sigma **2)))
		return g / g.sum()
	else:
		raise ValueError("The size of gaussian kernel must be odd integer number.")

def low_pass(img,sigma,size=5):
	g_kernel = gaussian_blur_kernel_2d(sigma,size)
	output = convolve_2d(img,g_kernel)
	return output

def high_pass(img,sigma,size=5):
	lowpass = low_pass(img,sigma,size)
	output = 3*(img - lowpass)
	return output