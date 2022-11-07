# https://data-flair.training/blogs/python-image-steganography-project/
# https://www.google.com/search?q=python+image+steganography+project&sxsrf=ALiCzsZn0DUcjQ9_ul00KNQ3G2flQMzcLQ%3A1665404875507&ei=yw9EY_vDHu3zqwG-uaOgCQ&oq=python+image+steganography+&gs_lcp=Cgdnd3Mtd2l6EAMYATIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46BggjECcQEzoECAAQQzoLCAAQgAQQsQMQgwE6BAgjECc6CggAELEDEIMBEEM6CwguEIAEELEDEIMBOgUIABCABEoECE0YAUoECEEYAEoECEYYAFAAWP0SYP8daABwAXgAgAFhiAGsA5IBATWYAQCgAQHAAQE&sclient=gws-wiz

import cv2
import numpy as np
from PIL import Image

i=0
msg = "Short secret message"
data = ''.join(format(ord(x), 'b') for x in msg)
print((data[:8]))

img = cv2.imread('test1.jpg') 
cv2.imshow('Original', img)
cv2.waitKey(0)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

with Image.open("test1.jpg") as img:
    width, height = img.size
    print(width, height)
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y)))
            for n in range(0,3):
                if(i < len(data)):
                    pixel[n] = pixel[n] & ~1 | int(data[i])
                    i+=1
            img.putpixel((x,y), tuple(pixel))
    img.save("source_secret.png", "PNG")

cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
cv2.waitKey(0)

cv2.destroyAllWindows()