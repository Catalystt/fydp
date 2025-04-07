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

def draw_quebec(text, photo):
    img = cv2.imread("./template/driverslicense/img/quebec.png", -1)
    overlay_image(img, photo, (41, 132), (336, 529))
    img = draw_text(img, get_arial_bold_font(48), (407, 121), text['number'])
    img = draw_text(img, get_arial_bold_font(32), (409, 174), text['first_name'])
    img = draw_text(img, get_arial_bold_font(32), (405, 204), text['last_name'])
    img = draw_text(img, get_arial_bold_font(32), (733, 233), text['dob'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(32), (409, 270), text['address_line1'])
    img = draw_text(img, get_arial_bold_font(32), (406, 302), text['address_line2'])
    img = draw_text(img, get_arial_bold_font(32), (405, 328), text['address_line3'])
    img = draw_text(img, get_arial_bold_font(32), (539, 392), text['driver_class'])
    img = draw_text(img, get_arial_bold_font(32), (847, 361), text['sex'])
    img = draw_text(img, get_arial_bold_font(32), (912, 423), text['height'])
    img = draw_text(img, get_arial_bold_font(32), (846, 455), text['eyes'])
    img = draw_text(img, get_arial_bold_font(32), (497, 418), text['conditions'])
    img = draw_text(img, get_arial_bold_font(32), (609, 481), text['reference_number'])
    img = draw_text(img, get_arial_bold_font(32), (520, 528), text['issued'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(32), (803, 528), text['expires'].strftime("%Y/%m/%d"))

    return img
