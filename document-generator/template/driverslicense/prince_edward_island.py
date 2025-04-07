from draw import draw_text, overlay_image, get_arial_bold_font
import cv2


def draw_prince_edward_island(text, photo):
    img = cv2.imread("./template/driverslicense/img/prince_edward_island.png", -1)
    overlay_image(img, photo, (28, 120), (217, 332))
    img = draw_text(img, get_arial_bold_font(24), (310, 76), text['number'], fill=(43, 38, 154, 255))
    img = draw_text(img, get_arial_bold_font(22), (297, 100), text['expires'].strftime("%Y/%m/%d"), fill=(43, 38, 154, 255))
    img = draw_text(img, get_arial_bold_font(22), (507, 100), text['issued'].strftime("%Y/%m/%d"), fill=(43, 38, 154, 255))
    img = draw_text(img, get_arial_bold_font(18), (267, 136), text['driver_class'])
    img = draw_text(img, get_arial_bold_font(18), (367, 136), text['end'])
    img = draw_text(img, get_arial_bold_font(18), (346, 156), text['rest'])
    img = draw_text(img, get_arial_bold_font(24), (347, 176), text['dob'].strftime("%Y/%m/%d"), fill=(43, 38, 154, 255))
    img = draw_text(img, get_arial_bold_font(18), (594, 182), text['sex'])
    img = draw_text(img, get_arial_bold_font(18), (347, 200), text['eyes'])
    img = draw_text(img, get_arial_bold_font(18), (547, 200), text['height'])
    img = draw_text(img, get_arial_bold_font(18), (462, 220), text['first_license'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(22), (258, 236), text['first_name'])
    img = draw_text(img, get_arial_bold_font(22), (255, 260), text['last_name'])
    img = draw_text(img, get_arial_bold_font(18), (256, 300), text['address_line1'])
    img = draw_text(img, get_arial_bold_font(18), (256, 318), text['address_line2'])
    img = draw_text(img, get_arial_bold_font(18), (256, 338), text['address_line2'])
    img = draw_text(img, get_arial_bold_font(16), (289, 360), text['dd'])

    overlay_image(img, photo, (552, 272), (609, 377))
    img = draw_text(img, get_arial_bold_font(16), (520, 360), text['dob'].strftime("%Y/%m/%d"))

    return img
















