from PIL import ImageFont

arialFontPath = "./font/Arial Bold.ttf"
arialFont = ImageFont.truetype(arialFontPath, 16)

# Top-left and bottom-right of bounding box
RECT_ZERO = ((0, 0), (0, 0))


class DriversLicenseBack:
    barcode = ""

    barcodePos = RECT_ZERO


class DriversLicenseFront:
    firstName = ""
    lastName = ""
    addressLine1 = ""
    addressLine2 = ""
    number = ""
    issued = ""
    expires = ""
    dd = ""
    height = ""
    sex = ""
    licenseClass = ""
    rest = ""
    dob = ""

    photoPos = RECT_ZERO
    firstNamePos = RECT_ZERO
    lastNamePos = RECT_ZERO
    addressLine1Pos = RECT_ZERO
    addressLine2Pos = RECT_ZERO
    numberPos = RECT_ZERO
    issuedPos = RECT_ZERO
    expiresPos = RECT_ZERO
    ddPos = RECT_ZERO
    heightPos = RECT_ZERO
    sexPos = RECT_ZERO
    classPos = RECT_ZERO
    restPos = RECT_ZERO
    dobPos = RECT_ZERO

    def __init__(self):
        self.text = {}


class DriversLicense:
    def __init__(self):
        self.image_path = ""
        self.front = DriversLicenseFront()
        self.back = DriversLicenseBack()


class DriversLicenseText:
    boundingBox = ((0, 0), (0, 0))
    text = ""
    font = None
    fontColor = ""

    def __init__(self, boundingBox, text="", font=arialFont, fontColor="#000000"):
        self.boundingBox = boundingBox
        self.text = text
        self.font = font
        self.fontColor = fontColor
