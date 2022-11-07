import cv2
import numpy as np

# Read the original image
img = cv2.imread('test1.jpg') 
# Display original image
cv2.imshow('Original', img)
cv2.waitKey(0)

b_org = np.asarray(img, dtype="int32")
print('original image bits ', b_org[0])
print(type(b_org))

# Convert to graycsale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 

# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection

b_sob = np.array(sobelxy)
print('sobel image bits ', b_sob[0])

msg = """
A hidden message is information that is not immediately noticeable, 
and that must be discovered or uncovered and interpreted before it can be known. 
"""

print(len(b_sob))
print(len(b_org))

#cv2.imshow('Sobel XY encoded', img_np)
#cv2.waitKey(0)

#cv2.imshow('Sobel XY encoded img blur', img_blur)
#cv2.waitKey(0)


# Display Sobel Edge Detection Images
#cv2.imshow('Sobel X', sobelx)
#cv2.waitKey(0)
#cv2.imshow('Sobel Y', sobely)
#cv2.waitKey(0)
#cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
#cv2.waitKey(0)

# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
# Display Canny Edge Detection Image
#cv2.imshow('Canny Edge Detection', edges)
#cv2.waitKey(0)

cv2.destroyAllWindows()