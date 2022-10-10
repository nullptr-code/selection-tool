from distutils.log import error
from turtle import clear
import numpy as np
import cv2
import os
import json

CITY_NAMES = [
    "bejing",
    "changchun",
    "changsha",
    "chengdu",
    "chongqing",
    "dalian",
    "dongguan",
    "foshan",
    "fuzhou",
    "guangzhou",
    "haikou",
    "hangzhou",
    "harbin",
    "hefei",
    "hohhot",
    "jinan",
    "lanzhou",
    "luoyang",
    "nanchang",
    "nanjing",
    "nanning",
    "nigbo",
    "ordos",
    "qingdo",
    "quanzhou",
    "shanghai",
    "shenyang",
    "shenzhen",
    "shijiazhouang",
    "tainjin",
    "taiyuan",
    "tangshan",
    "wuhan",
    "xian",
    "xining",
    "yinchun",
    "zhengzhou",
]

CITY_INDEX = 2

view1_dir = os.path.join("training images", CITY_NAMES[CITY_INDEX], "view1")
masks_dir = os.path.join("training images", CITY_NAMES[CITY_INDEX], "masks")

# print(ord("space"))


def its_overlay_time(image, mask):
    # mask[mask > 0] = 255
    mask[mask < 255] = 0
    mask = np.bitwise_not(mask)

    temp = mask.copy().T
    temp[0] = 0
    temp[1] = 0
    temp = temp.T

    temp = cv2.addWeighted(image, 0.8, temp, 0.2, 1)
    cv2.imshow("test", temp)
    cv2.waitKey(0)


def create_city(data, city_name):
    if city_name in data.keys():
        print(f"{city_name} already exists")
        return
    else:
        data[city_name] = {"selected": [], "rejected": [], "last-seen": ""}


def begin_selection(view1_dir, view2_dir, masks_dir, city_name):

    with open("dataList.json", "r") as f:
        data = f.read()

    data = json.loads(data)

    create_city(data, city_name)

    city_data = data[city_name]
    image_names = sorted(os.listdir(view1_dir))
    mask_names = sorted(os.listdir(view2_dir))

    if city_data["last-seen"] != "":
        last_index = image_names.index(city_data["last-seen"]) + 1
        image_names = image_names[last_index:]
        mask_names = mask_names[last_index:]

    for image_name, mask_name in zip(image_names, mask_names):
        city_data["last-seen"] = image_name

        view1_path, mask_path, view2_path = (
            os.path.join(view1_dir, image_name),
            os.path.join(masks_dir, mask_name),
            os.path.join(view2_dir, image_name),
        )

        view1 = cv2.imread(view1_path)
        view2 = cv2.imread(view2_path)
        # mask = cv2.imread(mask_path) don't need to import masks lol

        img = cv2.hconcat([view1, view2])
        cv2.resize(img, (img.shape[0] * 2, img.shape[1] * 2))
        # return

        cv2.imshow(f"{city_name} - {image_name}", img)
        k = cv2.waitKey(0)

        if k == 27:
            cv2.destroyAllWindows()
            break
        elif k == ord("1"):
            city_data["selected"].append(view1_path)
            print("Selected ----> ", view1_path)
        elif k == ord("2"):
            city_data["selected"].append(view2_path)
            print("Selected ----> ", view2_path)
        elif k == ord("3"):
            city_data["selected"].append(view1_path)
            city_data["selected"].append(view2_path)
            print("Selected ----> ", view2_path)
            print("Selected ----> ", view2_path)
        elif k == ord("0"):
            city_data["rejected"].append(view1_path)
            city_data["rejected"].append(view2_path)
        else:
            print("INVALID USER INPUT")
            cv2.destroyAllWindows()
            return

        cv2.destroyAllWindows()

        print(f"No of Selected: {len(city_data['selected'])}")
        print(f"No of Rejected: {len(city_data['rejected'])}")
        print()

        with open("dataList.json", "w") as f:
            f.write(json.dumps(data))


if __name__ == "__main__":
    print("Select City")

    for i, city in enumerate(CITY_NAMES):
        print(f"{i}. {city}")

    city_index = int(input(">>"))

    view1_dir = os.path.join("training-data", CITY_NAMES[city_index], "view1")
    view2_dir = os.path.join("training-data", CITY_NAMES[city_index], "view2")
    masks_dir = os.path.join("training-data", CITY_NAMES[city_index], "masks")

    begin_selection(view1_dir, view2_dir, masks_dir, CITY_NAMES[city_index])
