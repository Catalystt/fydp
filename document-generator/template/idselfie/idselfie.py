import cv2
import os
from draw import overlay_image, constrain_image, rotate_image, draw_glare, blur_image


class IDSelfie:
    def __init__(self, document_bounding_box=((0, 0), (0, 0)), document_rotation=0, face_bounding_box=((0, 0), (0, 0))):
        self.document_bounding_box = document_bounding_box
        self.document_rotation = document_rotation
        self.face_bounding_box = face_bounding_box


id_selfies = {
    "./template/idselfie/0.png": IDSelfie(((803, 438), (1067, 615)), -1),
    "./template/idselfie/1.png": IDSelfie(((133, 191), (660, 542))),
    "./template/idselfie/2.png": IDSelfie(((663, 515), (1038, 789)), -12),
}


# Save all selfies as png's constrained to a max width and height
def format_id_selfies():
    for id_selfie in id_selfies:
        selfie_img = cv2.imread(id_selfie)
        selfie_img = constrain_image(selfie_img, 1280, 1280, 1280, 1280)

        # Save as a png file
        base = os.path.splitext(id_selfie)[0]
        new_filename = base + ".png"

        cv2.imwrite(new_filename, selfie_img)


# format_id_selfies()

def draw_id_selfie(id_selfie, value, drivers_license_img):
    selfie_img = cv2.imread(id_selfie)

    rot_img = draw_glare(drivers_license_img)
    rot_img = rotate_image(rot_img, value.document_rotation)
    rot_img = blur_image(rot_img)
    overlay_image(selfie_img, rot_img, value.document_bounding_box[0], value.document_bounding_box[1])

    return selfie_img
