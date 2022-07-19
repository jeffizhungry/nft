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

# Changes this IMAGES_BASE_URL to yours
IMAGES_BASE_URL = "https://gateway.pinata.cloud/ipfs/QmRVpBZDAin34Hwztw5xwRvyFTwctB5h7QpQHGEaKfNnHq/"
PROJECT_NAME = "NFTPrintingPress"

# -------------------------------------
# Main Function
# -------------------------------------
if __name__ == "__main__":
    # Generate Metadata for each Image

    with open('./metadata/all-traits.json',) as f:
        data = json.load(f)

        def getAttribute(key, value):
            return {
                "trait_type": key,
                "value": value
            }
        for i in data:
            token_id = i['tokenId']
            token = {
                "image": IMAGES_BASE_URL + str(token_id) + '.png',
                "tokenId": token_id,
                "name": PROJECT_NAME + ' ' + str(token_id),
                "attributes": []
            }
            token["attributes"].append(getAttribute("Face", i["Face"]))
            token["attributes"].append(getAttribute("Ears", i["Ears"]))
            token["attributes"].append(getAttribute("Eyes", i["Eyes"]))
            token["attributes"].append(getAttribute("Hair", i["Hair"]))
            token["attributes"].append(getAttribute("Mouth", i["Mouth"]))
            token["attributes"].append(getAttribute("Nose", i["Nose"]))

            with open('./metadata/' + str(token_id) + ".json", 'w') as outfile:
                json.dump(token, outfile, indent=4)
