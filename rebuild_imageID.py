import os
import json
import cv2 as cv

f = open("C:/Users/liminyi/OneDrive/桌面/UC_Berkeley/DETR/coco_annotations/trainval.json", encoding="utf-8")# switch among train.json & val.json & trainval.json
file = json.load(f)
Images = file["images"]
Annotations = file["annotations"]

#produce the list of Image Path
path_list = []
for path in Images:
    each_path = path['file_name']
    image_path = each_path.split('/')[0]

    if image_path not in path_list:
        path_list.append(image_path)

#produce the number list of images according to the path list
tmp_image_number_list = []
for item_path in range(len(path_list)):
    sub_number_list = []

    for tmp_path in Images:
        image_path = tmp_path['file_name'].split('/')[0]

        if image_path == path_list[item_path]:
            image_number = tmp_path['file_name'].split('/')[1].split('.')[0]
            image_id = tmp_path['id']

            if image_number not in sub_number_list:
                sub_sub_number_list = []
                sub_sub_number_list.append(image_id)
                sub_sub_number_list.append(int(image_number))
            sub_number_list.append(sub_sub_number_list)

    tmp_image_number_list.append(sub_number_list)

# print(len(tmp_image_number_list))
print(tmp_image_number_list[2])
print(sorted(tmp_image_number_list[2], key=lambda x: x[1]))