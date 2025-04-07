from draw import draw_text, overlay_image, get_arial_bold_font
import cv2


# arialFontPath = "./font/Arial Bold.ttf"
# arialFont = ImageFont.truetype(arialFontPath, 16)

# ONTARIO_DRIVERS_LICENSE = DriversLicense()
# ONTARIO_DRIVERS_LICENSE.image_path = "./template/driverslicense/img/ontario.png"

# ONTARIO_DRIVERS_LICENSE.front.text = {
# 	'photo': DriversLicenseText(((34, 72), (197, 287))),
# 	'firstName': DriversLicenseText(((220, 92), (256, 102))),
# 	'lastName': DriversLicenseText(((220, 110), (264, 122))),
# 	'addressLine1': DriversLicenseText(((220, 130), (352, 138))),
# 	'addressLine2': DriversLicenseText(((222, 149), (413, 158))),
# 	'number': DriversLicenseText(((283, 170), (515, 185)), font = ImageFont.truetype(arialFontPath, 24)),
# 	'issued': DriversLicenseText(((279, 193), (358, 203))),
# 	'expires': DriversLicenseText(((472, 196), (551, 207))),
# 	'dd': DriversLicenseText(((281, 216), (364, 228))),
# 	'height': DriversLicenseText(((472, 217), (526, 278))),
# 	'sex': DriversLicenseText(((282, 239), (294, 249))),
# 	'driverClass': DriversLicenseText(((281, 261), (291, 272))),
# 	'rest': DriversLicenseText(((280, 294), (291, 306))),
# 	'dob': DriversLicenseText(((77, 328), (167, 340)))
# }

def draw_ontario(text, photo):
    img = cv2.imread("./template/driverslicense/img/ontario.png", -1)
    overlay_image(img, photo, (34, 72), (197, 287))
    img = draw_text(img, get_arial_bold_font(16), (220, 92), text['first_name'])
    img = draw_text(img, get_arial_bold_font(16), (220, 110), text['last_name'])
    img = draw_text(img, get_arial_bold_font(16), (220, 130), text['address_line1'])
    img = draw_text(img, get_arial_bold_font(16), (222, 149), text['address_line2'])
    img = draw_text(img, get_arial_bold_font(24), (283, 170), text['number'])
    img = draw_text(img, get_arial_bold_font(16), (279, 193), text['issued'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(16), (472, 196), text['expires'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(16), (281, 216), text['dd'])
    img = draw_text(img, get_arial_bold_font(16), (472, 217), text['height'])
    img = draw_text(img, get_arial_bold_font(16), (282, 239), text['sex'])
    img = draw_text(img, get_arial_bold_font(16), (281, 261), text['driver_class'])
    img = draw_text(img, get_arial_bold_font(16), (280, 294), text['rest'])
    img = draw_text(img, get_arial_bold_font(16), (77, 328), text['dob'].strftime("%Y/%m/%d"))

    overlay_image(img, photo, (482, 258), (531, 315))
    img = draw_text(img, get_arial_bold_font(12), (368, 260), text['number'])
    img = draw_text(img, get_arial_bold_font(16), (396, 277), text['dob'].strftime("%Y/%m/%d"))

    return img
