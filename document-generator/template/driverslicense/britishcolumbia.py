from draw import draw_text, overlay_image, get_arial_bold_font
import cv2


# BRITISH_COLUMBIA_DRIVERS_LICENSE = DriversLicense()
# BRITISH_COLUMBIA_DRIVERS_LICENSE.image_path = "./template/driverslicense/img/britishcolumbia.jpg"

# BRITISH_COLUMBIA_DRIVERS_LICENSE.front.text = {
# 	'photo': DriversLicenseText(((33, 113), (179, 285))),
# 	'firstName': DriversLicenseText(((21, 76), (109, 91))),
# 	'lastName': DriversLicenseText(((21, 97), (136, 111))),
# 	'addressLine1': DriversLicenseText(((179, 258), (429, 271)), font = ImageFont.truetype(arialFontPath, 20)),
# 	'addressLine2': DriversLicenseText(((179, 273), (389, 287)), font = ImageFont.truetype(arialFontPath, 20)),
# 	'number': DriversLicenseText(((431, 89), (538, 108)), font = ImageFont.truetype(arialFontPath, 24)),
# 	'issued': DriversLicenseText(((245, 122), (355, 136))),
# 	'expires': DriversLicenseText(((245, 142), (355, 152))),
# 	'restrictions': DriversLicenseText(((288, 173), (305, 186))),
# 	'driverClass': DriversLicenseText(((226, 194), (223, 206))),
# 	'weight': DriversLicenseText(((207, 216), (267, 228))),
# 	'height': DriversLicenseText(((302, 218), (363, 230))),
# 	'sex': DriversLicenseText(((211, 239), (222, 250))),
# 	'eyes': DriversLicenseText(((304, 239), (339, 251))),
# 	'hair': DriversLicenseText(((405, 239), (442, 251))),
# 	'dob': DriversLicenseText(((418, 118), (534, 131)))
# }

def draw_british_columbia(text, photo):
    img = cv2.imread("./template/driverslicense/img/britishcolumbia.png", -1)
    overlay_image(img, photo, (33, 113), (179, 285))
    img = draw_text(img, get_arial_bold_font(16), (21, 76), text['first_name'])
    img = draw_text(img, get_arial_bold_font(16), (21, 97), text['last_name'])
    img = draw_text(img, get_arial_bold_font(20), (179, 258), text['address_line1'])
    img = draw_text(img, get_arial_bold_font(20), (179, 273), text['address_line2'])
    img = draw_text(img, get_arial_bold_font(24), (431, 89), text['number'])
    img = draw_text(img, get_arial_bold_font(16), (245, 122), text['issued'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(16), (245, 142), text['expires'].strftime("%Y/%m/%d"))
    img = draw_text(img, get_arial_bold_font(16), (288, 173), text['restrictions'])
    img = draw_text(img, get_arial_bold_font(16), (226, 194), text['driver_class'])
    img = draw_text(img, get_arial_bold_font(16), (207, 216), text['weight'])
    img = draw_text(img, get_arial_bold_font(16), (302, 218), text['height'])
    img = draw_text(img, get_arial_bold_font(16), (211, 239), text['sex'])
    img = draw_text(img, get_arial_bold_font(16), (304, 239), text['eyes'])
    img = draw_text(img, get_arial_bold_font(16), (405, 239), text['hair'])
    img = draw_text(img, get_arial_bold_font(16), (418, 118), text['dob'].strftime("%Y/%m/%d"))

    overlay_image(img, photo, (457, 154), (532, 243))

    return img
