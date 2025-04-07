from draw import draw_text, overlay_image, get_arial_bold_font
import cv2


def draw_manitoba(text, photo):
    img = cv2.imread("./template/driverslicense/img/manitoba.png", -1)
    overlay_image(img, photo, (46, 140), (334, 479))
    img = draw_text(img, get_arial_bold_font(30), (374, 110), text['first_name'])
    img = draw_text(img, get_arial_bold_font(30), (373, 142), text['last_name'])
    img = draw_text(img, get_arial_bold_font(30), (373, 209), text['address_line1'])
    img = draw_text(img, get_arial_bold_font(30), (376, 246), text['address_line2'])
    img = draw_text(img, get_arial_bold_font(40), (456, 278), text['number'])
    img = draw_text(img, get_arial_bold_font(30), (351, 342), text['issued'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(30), (515, 342), text['expires'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(30), (351, 400), text['restrictions'])
    img = draw_text(img, get_arial_bold_font(30), (517, 400), text['driver_class'])
    img = draw_text(img, get_arial_bold_font(30), (817, 400), text['end'])
    img = draw_text(img, get_arial_bold_font(30), (351, 460), text['eyes'])
    img = draw_text(img, get_arial_bold_font(30), (517, 460), text['restrictions'])
    img = draw_text(img, get_arial_bold_font(30), (351, 519), text['sex'])
    img = draw_text(img, get_arial_bold_font(30), (517, 519), text['height'])
    img = draw_text(img, get_arial_bold_font(30), (158, 581), text['dob'].strftime("%Y/%m/%d"))

    overlay_image(img, photo, (865, 465), (951, 563))
    img = draw_text(img, get_arial_bold_font(24), (678, 476), text['number'], fill=(97, 97, 97, 255))
    img = draw_text(img, get_arial_bold_font(24), (678, 502), text['dob'].strftime("%Y/%m/%d"), fill=(97, 97, 97, 255))

    return img
