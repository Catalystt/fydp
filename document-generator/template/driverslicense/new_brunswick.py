from draw import draw_text, overlay_image, get_arial_bold_font
import cv2


def draw_new_brunswick(text, photo):
    img = cv2.imread("./template/driverslicense/img/new_brunswick.png", -1)
    overlay_image(img, photo, (539, 111), (735, 350))
    img = draw_text(img, get_arial_bold_font(24), (119, 99), text['number'])
    img = draw_text(img, get_arial_bold_font(16), (119, 126), text['issued'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(16), (356, 121), text['dob'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(16), (119, 148), text['expires'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(16), (53, 171), text['first_name'])
    img = draw_text(img, get_arial_bold_font(16), (53, 197), text['last_name'])
    img = draw_text(img, get_arial_bold_font(20), (53, 249), text['address_line1'])
    img = draw_text(img, get_arial_bold_font(20), (53, 275), text['address_line2'])
    img = draw_text(img, get_arial_bold_font(16), (267, 332), text['sex'])
    img = draw_text(img, get_arial_bold_font(16), (267, 358), text['height'])
    img = draw_text(img, get_arial_bold_font(16), (267, 384), text['eyes'])
    img = draw_text(img, get_arial_bold_font(16), (230, 432), text['dd'])

    overlay_image(img, photo, (46, 337), (119, 429))
    img = draw_text(img, get_arial_bold_font(16), (35, 433), text['dob'].strftime("%Y/%m/%d"))

    return img
