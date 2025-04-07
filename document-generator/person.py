from datetime import date, timedelta
import glob
import string
import random


def random_drivers_license():
    drivers_license = {
        'face': random_face(),
        'first_name': random_first_name(),
        'last_name': random_last_name(),
        'address_line1': random_address_line_1(),
        'address_line2': random_address_line_2(),
        'address_line3': random_address_line_3(),
        'number': random_license_number(),
        'issued': random_issued(),
        'expires': random_expires(),
        'dd': "12",
        'height': "4'5",
        'sex': random_sex(),
        'end': "N",  # End/Endoss.
        'driver_class': "C",
        'rest': "A",
        'restrictions': "21",
        'weight': "51.0 kg",
        'eyes': random_eyes(),
        'hair': random_hair(),
        'dob': random_dob(),
        'conditions': random_conditions(),
        'reference_number': random_reference_number(),
        'first_license': random_first_license(),
    }

    return drivers_license


faces = [img for img in glob.glob("./template/face/*")]
faces.sort()


def random_alphabetical(min_length, max_length):
    random_length = random.randint(min_length, max_length)

    # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    # Only uppercase for licenses
    return ''.join(random.choices(string.ascii_uppercase, k=random_length))


def random_numeric(min_length, max_length):
    random_length = random.randint(min_length, max_length)
    return ''.join(random.choices(string.digits, k=random_length))


def random_date(start, end):
    # Generate a random datetime between start and end
    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def random_address_line_1():
    return (random_numeric(1, 4) + " " + random.choice(
        ["University", "Westmount", "Keats Way", "Bishop", "King", "Queen"]) + " " + random.choice(
        ["Dr, Rd, Ave"])).upper()


def random_address_line_2():
    return random.choice(["SLC", "Basement", "Unit " + random_numeric(1, 4)]).upper()


def random_address_line_3():
    return "(QC) " + str(random_numeric(6, 6))


def random_sex():
    return random.choice(["M", "F", "N/A"])


def random_eyes():
    return random.choice(["BLU", "BLK", "BRN", "GRN", "RED", "GRY"])


def random_license_number():
    return 'L' + random_numeric(4, 4) + '-' + random_numeric(5, 5) + '-' + random_numeric(5, 5)


def random_reference_number():
    return random_alphabetical(3, 20)


def random_first_name():
    return random_alphabetical(3, 20)


def random_last_name():
    return random_alphabetical(3, 20)


def random_issued():
    return random_date(date(date.today().year - 10, 1, 1), date.today())


def random_expires():
    return random_date(date.today(), date(date.today().year + 20, 1, 1))


def random_conditions():
    return random.choice(["CLEAR", "AUCUND", "ANY"])


def random_dob():
    return random_date(date(1900, 1, 1), date(date.today().year - 18, 1, 1))


def random_hair():
    return random.choice(["BLU", "BLK", "BRN", "BLD", "RED", "GRY"])


def random_face():
    return random.choice(faces)


def random_first_license():
    return random_date(date(1950, 1, 1), date(date.today().year - 18, 1, 1))
