import os
import sys
from pdf2image import convert_from_path
import re
from tqdm import tqdm


# Store Pdf with convert_from_path function


CITY_NAMES = [
    "bejing",
    "dalian",
    "dongguan",
    "foshan",
    "guangzhou",
    "harbin",
    "hefei",
    "hohhot",
    "nanchang",
    "nanning",
]

image_dir = os.path.join("training data", CITY_NAMES[2])

walked = os.walk(image_dir)
next(walked)

for root, _, files in walked:
    # print(root, files[:5])
    folders = re.split(r"\\|/", root)[1:]
    new_dir = os.path.join("training images", *folders)
    os.makedirs(new_dir, exist_ok=True)
    for pdf in tqdm(files):
        pdf_path = os.path.join(root, pdf)
        image_path = os.path.join(new_dir, pdf.split(".")[0]) + ".tiff"
        image = convert_from_path(pdf_path)[0]
        image.save(image_path)

        # image.save(os.path.join(new_dir, pdf.split(".")[0]), "TIFF")
# images = convert_from_path("../training data/" + CITY_NAMES[1], 300)

# for i in range(len(images)):
#     # Save pages as images in the pdf
#     images[i].save("page" + str(i) + ".tiff")
