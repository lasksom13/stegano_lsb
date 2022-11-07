import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import cv2
import sys

# Assign values to variables via APP Interface

BIT_AMOUNT = 2  # from 1 to 6
EDGE_PARAMETER = 50  # from 50 to 300
IMAGE_DECODE_PATH = "./temporary_images/encoded_image.png"

app = tk.Tk()
app.geometry("1200x800")  # Size of the window 
app.title('HidingInfo')
my_font1=('times', 14, 'bold')

l1 = tk.Label(app,text='Add image to encode',width=50,font=my_font1)
l1.grid(row=1,column=1)
#l1.place(height=150, width=2500)

b1 = tk.Button(app, text='Upload image', 
   width=20,command = lambda:upload_file(col=1))
b1.grid(row=3,column=1) 

l2 = tk.Label(app,text="Insert text to hide",width=30,font=my_font1)
l2.grid(row=1, column=2)
inputTxt = tk.Text(app, height=8, width=40)
inputTxt.grid(row=2, column=2)

b3 = tk.Button(app, text='Encode image', 
   width=20,command = lambda:encode_file())
b3.grid(row=3, column=2)

b4 = tk.Button(app, text='Decode image', 
   width=20,command = lambda:decode_file())
b4.grid(row=4, column=2)

def upload_file(col):
    f_types = [('Jpg Files', '*.jpg'),
    ('PNG Files','*.png')]   # type of files to select
    filename = tk.filedialog.askopenfilename(multiple=True,filetypes=f_types)
    row=2 # start from row 3 
    for f in filename:
        print("its f: ", f)
        img=Image.open(f) # read the image file
        img=img.resize((400,270)) # new width & height
        img=ImageTk.PhotoImage(img)
        e1 =tk.Label(app)
        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection
        global IMAGE_PATH
        IMAGE_PATH = f
        return IMAGE_PATH

def encode_file():
    #encoding
    TEXT_MESSAGE = inputTxt.get("1.0",'end-1c') + "~~"
    print("To wiadomosc do zakodowania:", TEXT_MESSAGE)
    print("przekazana ścieżka: ",IMAGE_PATH)
    create_image_with_zeros(IMAGE_PATH, BIT_AMOUNT)
    create_edge_image(EDGE_PARAMETER)
    encode_message_into_image(TEXT_MESSAGE, BIT_AMOUNT, IMAGE_PATH)
    l3 = tk.Label(app,text='Edge image',width=50,font=my_font1)  
    l3.grid(row=6,column=1)
    img=Image.open("./temporary_images/edge_image.png")
    img=img.resize((400,270)) # new width & height
    img=ImageTk.PhotoImage(img)
    e1 =tk.Label(app)
    e1.grid(row=7,column=1)
    e1.image = img
    e1['image']=img # garbage collection
        
    l4 = tk.Label(app,text='Encoded image',width=50,font=my_font1)  
    l4.grid(row=6,column=2)
    img=Image.open("./temporary_images/encoded_image.png")
    img=img.resize((400,270)) # new width & height
    img=ImageTk.PhotoImage(img)
    e2 =tk.Label(app)
    e2.grid(row=7,column=2)
    e2.image = img
    e2['image']=img # garbage collection

def decode_file():
    #decoding
    decode_message_from_image(IMAGE_DECODE_PATH,BIT_AMOUNT,EDGE_PARAMETER)
    l4 = tk.Label(app,text='Decoded image',width=30,font=my_font1)  
    l4.grid(row=6,column=4)

def create_image_with_zeros(IMAGE_PATH: str, BIT_AMOUNT: int):
    im_original = Image.open(IMAGE_PATH)
    pix_original = im_original.load()

    for x in range(im_original.size[0]):
        for y in range(im_original.size[1]):
            color_a = pix_original[x,y][0]
            color_b = pix_original[x,y][1]
            color_c = pix_original[x,y][2]
            for bit in range(BIT_AMOUNT):
                color_a = (color_a & ~(1 << bit)) | (0 << bit)
                color_b = (color_b & ~(1 << bit)) | (0 << bit)
                color_c = (color_c & ~(1 << bit)) | (0 << bit)
            temp_list = [color_a, color_b, color_c]
            pix_original[x,y] = tuple(temp_list)

    im_original.save("./temporary_images/original_zero.png")
    return

def create_edge_image(EDGE_PARAMETER: int):
    im = cv2.imread("./temporary_images/original_zero.png")
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(im, EDGE_PARAMETER, 300)
    (thresh, BW_image) = cv2.threshold(edges, 125, 255, cv2.THRESH_BINARY)
    (thresh, BW_image2) = cv2.threshold(BW_image, 125, 255, cv2.THRESH_BINARY_INV)
    BW_image_format = Image.fromarray(BW_image2)
    BW_image_format.save("./temporary_images/edge_image.png")
    return

def encode_message_into_image(TEXT_MESSAGE: str, BIT_AMOUNT: int ,IMAGE_PATH: str):
    text_bin = (''.join(format(ord(x), '07b') for x in TEXT_MESSAGE))
    print(text_bin)

    # original image <- encode messsage on it
    im_org = Image.open(IMAGE_PATH)
    pix_org = im_org.load()

    # edge image <- based on this image choose pixels
    im = Image.open("./temporary_images/edge_image.png")
    pix = im.load()

    counter = 0
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if pix[x,y] == 0:
                counter += 1

    if len(text_bin) > counter:
        print("Message is too long")
        sys.exit(1)

    counter = 0
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if pix[x,y] == 0:
                list = [pix_org[x,y][0], pix_org[x,y][1], pix_org[x,y][2]]
                for color in range(3):
                    color_x = pix_org[x,y][color]
                    for bit in range(BIT_AMOUNT):
                        color_x = (color_x & ~(1 << bit)) | (int(text_bin[counter]) << bit)
                        counter += 1
                        list[color] = color_x
                        pix_org[x,y] = tuple(list)
                        if counter == len(text_bin):
                            im_org.save("./temporary_images/encoded_image.png")
                            return

# COPY PASTE FOR DECODE PROCESS
def decode_message_from_image(IMAGE_DECODE_PATH: str, BIT_AMOUNT, EDGE_PARAMETER):
    # STEP 1
    im_original = Image.open(IMAGE_DECODE_PATH)
    pix_original = im_original.load()
    for x in range(im_original.size[0]):
        for y in range(im_original.size[1]):
            color_a = pix_original[x, y][0]
            color_b = pix_original[x, y][1]
            color_c = pix_original[x, y][2]
            for bit in range(BIT_AMOUNT):
                color_a = (color_a & ~(1 << bit)) | (0 << bit)
                color_b = (color_b & ~(1 << bit)) | (0 << bit)
                color_c = (color_c & ~(1 << bit)) | (0 << bit)
            temp_list = [color_a, color_b, color_c]
            pix_original[x, y] = tuple(temp_list)
    im_original.save("./temporary_images_decode/decode_zero.png")

    # STEP 2
    im = cv2.imread("./temporary_images_decode/decode_zero.png")
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(im, EDGE_PARAMETER, 300)
    (thresh, BW_image) = cv2.threshold(edges, 125, 255, cv2.THRESH_BINARY)
    (thresh, BW_image2) = cv2.threshold(BW_image, 125, 255, cv2.THRESH_BINARY_INV)
    BW_image_format = Image.fromarray(BW_image2)
    BW_image_format.save("./temporary_images_decode/edge_decode_image.png")

    # STEP 3
    end_char = "~~"
    end_char = (''.join(format(ord(x), '07b') for x in end_char))
    text_bin = "0" * 14
    # original image <- encode messsage on it
    im_org = Image.open(IMAGE_DECODE_PATH)
    pix_org = im_org.load()
    # edge image <- based on this image choose pixels
    im = Image.open("./temporary_images_decode/edge_decode_image.png")
    pix = im.load()

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if pix[x, y] == 0:
                for color in range(3):
                    color_x = pix_org[x, y][color]
                    for bit in range(BIT_AMOUNT):
                        char = str( (color_x >> bit) & 1 )
                        text_bin += char
                        if text_bin[-14:] == end_char:
                            text_bin = text_bin[14:-14]
                            print(text_bin)
                            text_decoded = ""
                            for char in range(0,len(text_bin),7):
                                text_decoded += chr(int("0b" + text_bin[char:char+7],2))
                            print(text_decoded)
                            return
'''
if __name__ == '__main__':
    create_image_with_zeros(IMAGE_PATH, BIT_AMOUNT)
    create_edge_image(EDGE_PARAMETER)
    encode_message_into_image(TEXT_MESSAGE, BIT_AMOUNT, IMAGE_PATH)
    decode_message_from_image(IMAGE_DECODE_PATH,BIT_AMOUNT,EDGE_PARAMETER)
'''

app.mainloop()  # Keep the window open