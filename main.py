import cv2
import sys
from PIL import Image

# Assign values to variables via APP Interface
IMAGE_PATH = "test.jpg"
BIT_AMOUNT = 2  # from 1 to 6
EDGE_PARAMETER = 50  # from 50 to 300
TEXT_MESSAGE = "to jest wiadomosc, ktora zakodujemy" + "~~"
IMAGE_DECODE_PATH = "./temporary_images/encoded_image.png"

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

if __name__ == '__main__':
    create_image_with_zeros(IMAGE_PATH, BIT_AMOUNT)
    create_edge_image(EDGE_PARAMETER)
    encode_message_into_image(TEXT_MESSAGE, BIT_AMOUNT, IMAGE_PATH)
    decode_message_from_image(IMAGE_DECODE_PATH,BIT_AMOUNT,EDGE_PARAMETER)
