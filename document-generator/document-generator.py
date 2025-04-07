import cv2
import random
import os
from tqdm import tqdm
import math
import glob
import itertools
import shutil
from draw import overlay_image, constrain_image, draw_glare, blur_image, rotate_image
from template.idselfie.idselfie import draw_id_selfie, id_selfies

from template.driverslicense.driverslicense import DriversLicense
from template.driverslicense.ontario import draw_ontario
from template.driverslicense.quebec import draw_quebec
from template.driverslicense.britishcolumbia import draw_british_columbia
from template.driverslicense.manitoba import draw_manitoba
from template.driverslicense.prince_edward_island import draw_prince_edward_island
from person import random_drivers_license

# ([a-z]+)([A-Z][a-z]+)
# $1_\l$2

backgrounds = [img for img in glob.glob("./template/backgrounds/*")]
backgrounds.sort()


def random_background():
    return random.choice(backgrounds)


def random_rotation(img):
    return rotate_image(img, random.randint(-20, 20))


provinces = {
    "ontario": draw_ontario,
    "britishcolumbia": draw_british_columbia,
    "quebec": draw_quebec,
    "manitoba": draw_manitoba,
    "prince_edward_island": draw_prince_edward_island,
}


# https://stackoverflow.com/questions/1274405/how-to-create-new-folder
def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python
def clear_dir(path):
    shutil.rmtree(path, ignore_errors=True)


def show_image(path):
    img = cv2.imread(path, -1)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def generate_drivers_licenses(num=100, output_dir="./output/train/"):
    num_photos_per_type = round(num / len(provinces))

    for row in tqdm(itertools.product(provinces.items(), range(0, num_photos_per_type))):
        province = row[0][0]
        draw_func = row[0][1]
        i = row[1]

        background = random_background()
        background_img = cv2.imread(background, 1)
        background_img = constrain_image(background_img, 600, 600)
        background_height, background_width = background_img.shape[:2]

        text = random_drivers_license()
        face_img = cv2.imread(text["face"], -1)

        province_img = blur_image(draw_glare(draw_func(text, face_img)))
        max_province_width = math.floor(random.uniform(0.5, 0.9) * background_width)
        max_province_height = math.floor(random.uniform(0.5, 0.9) * background_height)
        # Rotate before constraining because it affects width and height
        province_img = random_rotation(province_img)
        province_img = constrain_image(province_img, max_province_width, max_province_height)
        province_height, province_width = province_img.shape[:2]

        province_pos = (random.randint(0, background_width - province_width),
                        random.randint(0, background_height - province_height))
        overlay_image(background_img, province_img, province_pos,
                     (province_pos[0] + province_width, province_pos[1] + province_height))

        filename = os.path.join(output_dir, province, str(i) + ".jpg")
        make_dir(os.path.dirname(filename))
        cv2.imwrite(filename, background_img)


def generate_id_selfies(num=100, output_dir="./output/train/"):
    num_photos_per_type = round(num / len(provinces) / len(id_selfies))

    for i in range(0, num_photos_per_type):
        for province, draw_func in provinces.items():
            text = random_driversLicense()
            face_img = cv2.imread(text["face"], -1)
            province_img = draw_func(text, face_img)

            for id_selfie, id_selfieData in id_selfies.items():
                filename = os.path.join(output_dir, province, str(i) + "_" + os.path.basename(id_selfie))
                make_dir(os.path.dirname(filename))
                cv2.imwrite(filename, draw_id_selfie(id_selfie, id_selfieData, province_img))


if __name__ == "__main__":
    # show_image("./template/driverslicense/img/originals/princeedwardisland.jpg")

    clear_dir("./output/train/")
    clear_dir("./output/valid/")

    print("Generating training set")
    generate_drivers_licenses(10, "./output/train/")

    print("Generating validation set")
    generate_drivers_licenses(10, "./output/valid/")

# cv2.imshow("Image", bcImg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
