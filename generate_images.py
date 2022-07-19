from PIL import Image
from IPython.display import display
import random
import json
import os

# -------------------------------------
# Config
# -------------------------------------

# Number of random unique images we want to generate
TOTAL_IMAGES = 100

OUTPUT_PATH = "./images"
METADATA_PATH = "./metadata"
METADATA_FILE_NAME = METADATA_PATH + '/all-traits.json'


# -------------------------------------
# Define traits and the chance that they will occur
# -------------------------------------
face = ["White", "Black"]
face_weights = [60, 40]

ears = ["No Earring", "Left Earring", "Right Earring", "Two Earrings"]
ears_weights = [25, 30, 44, 1]

eyes = ["Regular", "Small", "Rayban", "Hipster", "Focused"]
eyes_weights = [70, 10, 5, 1, 14]

hair = ['Up Hair', 'Down Hair', 'Mohawk', 'Red Mohawk', 'Orange Hair', 'Bubble Hair', 'Emo Hair',
        'Thin Hair',
        'Bald',
        'Blonde Hair',
        'Caret Hair',
        'Pony Tails']
hair_weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 2]

mouth = ['Black Lipstick', 'Red Lipstick', 'Big Smile',
         'Smile', 'Teeth Smile', 'Purple Lipstick']
mouth_weights = [10, 10, 50, 10, 15, 5]

nose = ['Nose', 'Nose Ring']
nose_weights = [90, 10]

# -------------------------------------
# Map traits to files
# -------------------------------------
face_files = {
    "White": "face1",
    "Black": "face2"
}

ears_files = {
    "No Earring": "ears1",
    "Left Earring": "ears2",
    "Right Earring": "ears3",
    "Two Earrings": "ears4"
}

eyes_files = {
    "Regular": "eyes1",
    "Small": "eyes2",
    "Rayban": "eyes3",
    "Hipster": "eyes4",
    "Focused": "eyes5"
}

hair_files = {
    "Up Hair": "hair1",
    "Down Hair": "hair2",
    "Mohawk": "hair3",
    "Red Mohawk": "hair4",
    "Orange Hair": "hair5",
    "Bubble Hair": "hair6",
    "Emo Hair": "hair7",
    "Thin Hair": "hair8",
    "Bald": "hair9",
    "Blonde Hair": "hair10",
    "Caret Hair": "hair11",
    "Pony Tails": "hair12"
}

mouth_files = {
    "Black Lipstick": "m1",
    "Red Lipstick": "m2",
    "Big Smile": "m3",
    "Smile": "m4",
    "Teeth Smile": "m5",
    "Purple Lipstick": "m6"
}

nose_files = {
    "Nose": "n1",
    "Nose Ring": "n2"
}

all_parts = ["Face", "Ears", "Eyes", "Hair", "Mouth", "Nose"]

# -------------------------------------
# Helper Functions
# -------------------------------------


def create_new_image(all_images):
    """
    A recursive function to generate unique image combinations
    """

    new_image = {}

    # For each trait category, select a random trait based on the weightings
    new_image["Face"] = random.choices(face, face_weights)[0]
    new_image["Ears"] = random.choices(ears, ears_weights)[0]
    new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image["Hair"] = random.choices(hair, hair_weights)[0]
    new_image["Mouth"] = random.choices(mouth, mouth_weights)[0]
    new_image["Nose"] = random.choices(nose, nose_weights)[0]
    new_image["tokenId"] = random.randint(1, 1000000000)

    # Dedupe images
    if new_image in all_images:
        return create_new_image(all_images)
    else:
        return new_image


def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


def count_traits(all_images):
    traits = {}
    for image in all_images:
        for part in all_parts:
            key = part + "." + image[part]
            if key in traits:
                traits[key] = traits[key] + 1
            else:
                traits[key] = 1

    sorted_traits = []
    for trait in traits:
        sorted_traits.append(trait)
    sorted_traits.sort()

    for trait in sorted_traits:
        count = traits[trait]
        print("{}: {}".format(trait, count))


# -------------------------------------
# Main Function
# -------------------------------------
if __name__ == "__main__":
    all_images = []

    # Generate the unique combinations based on trait weightings
    for i in range(TOTAL_IMAGES):

        new_trait_image = create_new_image(all_images)

        all_images.append(new_trait_image)

    # print("Are all images unique?", all_images_unique(all_images))
    # count_traits(all_images)

    # Generate Images
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    for item in all_images:

        im1 = Image.open(f'./substrapunks/scripts/face_parts/face/{face_files[item["Face"]]}.png').convert('RGBA')
        im2 = Image.open(f'./substrapunks/scripts/face_parts/eyes/{eyes_files[item["Eyes"]]}.png').convert('RGBA')
        im3 = Image.open(f'./substrapunks/scripts/face_parts/ears/{ears_files[item["Ears"]]}.png').convert('RGBA')
        im4 = Image.open(f'./substrapunks/scripts/face_parts/hair/{hair_files[item["Hair"]]}.png').convert('RGBA')
        im5 = Image.open(f'./substrapunks/scripts/face_parts/mouth/{mouth_files[item["Mouth"]]}.png').convert('RGBA')
        im6 = Image.open(f'./substrapunks/scripts/face_parts/nose/{nose_files[item["Nose"]]}.png').convert('RGBA')

        # Create each composite
        com1 = Image.alpha_composite(im1, im2)
        com2 = Image.alpha_composite(com1, im3)
        com3 = Image.alpha_composite(com2, im4)
        com4 = Image.alpha_composite(com3, im5)
        com5 = Image.alpha_composite(com4, im6)

        # Convert to RGB
        rgb_im = com5.convert('RGB')
        file_name = str(item["tokenId"]) + ".png"
        rgb_im.save(OUTPUT_PATH + "/" + file_name)

    # Generate Metadata
    os.makedirs(METADATA_PATH, exist_ok=True)

    with open(METADATA_FILE_NAME, 'w') as outfile:
        json.dump(all_images, outfile, indent=4)
