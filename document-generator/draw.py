import numpy as np
import random
import cv2
import math
from PIL import ImageFont, ImageDraw, Image

random.seed()


def is_transparent(img):
    return len(img.shape) > 2 and img.shape[2] == 4


def get_arial_bold_font(size):
    font_path = "./font/Arial Bold.ttf"
    font = ImageFont.truetype(font_path, size)
    return font


def constrain_image(img, max_width, max_height, min_width=0, min_height=0):
    img_width = img.shape[1]
    img_height = img.shape[0]

    ratio = min(max_width / img_width, max_height / img_height)

    scaled_image = cv2.resize(img, (0, 0), fx=ratio, fy=ratio)
    return scaled_image


# Blend the 3 color channels of the images using the alpha transparency of the overlay image
# https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv
def overlay_image(l_img, s_img, pos1=(0, 0), pos2=(0, 0)):
    scaled_overlay_image = cv2.resize(s_img, (pos2[0] - pos1[0], pos2[1] - pos1[1]))

    x_offset = pos1[0]
    y_offset = pos1[1]

    y1, y2 = y_offset, y_offset + scaled_overlay_image.shape[0]
    x1, x2 = x_offset, x_offset + scaled_overlay_image.shape[1]

    # Alpha transparency of overlay image
    alpha_s = 1.0

    # Not all images have an alpha layer
    if is_transparent(scaled_overlay_image):
        alpha_s = scaled_overlay_image[:, :, 3] / 255.0

    # Alpha transparency of background image
    alpha_l = 1.0 - alpha_s

    # Color channels
    for c in range(0, 3):
        l_img[y1:y2, x1:x2, c] = (alpha_s * scaled_overlay_image[:, :, c] + alpha_l * l_img[y1:y2, x1:x2, c])

    return l_img


# https://stackoverflow.com/questions/37191008/load-truetype-font-to-opencv
def draw_text(img, font, position=(0, 0), text="", fill=(0, 0, 0, 255)):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=fill)

    return np.array(img_pil)


# https://stackoverflow.com/questions/43846306/how-to-produce-glare-on-an-image-with-opencv
def draw_glare(img):
    original_img_transparency = img[:, :, 3].copy()
    num_glare_spots = random.randint(0, 4)
    for i in range(0, num_glare_spots):
        img_width, img_height = img.shape[:2]
        x = random.randint(0, img_width)
        y = random.randint(0, img_height)
        radius = random.randint(20, 80)
        alpha = random.random()
        overlay = img.copy()
        overlay = cv2.circle(overlay, (x, y), radius, (255, 255, 255), -1)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    # Restore the image's original transparency, otherwise there would be holes if overlayed over another image
    img[:, :, 3] = original_img_transparency

    return img


def blur_image(img):
    sigma_x = random.uniform(0.5, 1.5)

    return cv2.GaussianBlur(img, (0, 0), sigma_x)


# https://stackoverflow.com/questions/22041699/rotate-an-image-without-cropping-in-opencv-in-c
def rotate_image(img, angle):
    height, width = img.shape[:2]
    image_center = (width / 2, height / 2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1)

    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    bound_w = int((height * abs(sin)) + (width * abs(cos)))
    bound_h = int((height * abs(cos)) + (width * abs(sin)))

    rotation_mat[0, 2] += ((bound_w / 2) - image_center[0])
    rotation_mat[1, 2] += ((bound_h / 2) - image_center[1])

    rotated_mat = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))

    return rotated_mat
