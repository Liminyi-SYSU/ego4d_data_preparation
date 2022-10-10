import os,time
import json
import cv2

f = open("/rscratch/data/ego4d_data/coco_annotations/temp.json", encoding="utf-8")# switch among train.json & val.json & trainval.json
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
image_id_list = []
for item_path in range(len(path_list)):
    sub_number_list = []
    sub_id_list = []

    for tmp_path in Images:
        image_path = tmp_path['file_name'].split('/')[0]

        if image_path == path_list[item_path]:
            image_number = tmp_path['file_name'].split('/')[1].split('.')[0]
            image_id = tmp_path['id']

            if image_number not in sub_number_list:
                sub_sub_number_list = []
                sub_sub_number_list.append(image_id)
                sub_sub_number_list.append(int(image_number))
                sub_id_list.append(image_id)
            sub_number_list.append(sub_sub_number_list)

    tmp_image_number_list.append(sub_number_list)
    image_id_list.append(sub_id_list)

#produce the temporary annotation list of images
tmp_annotations_list = []
for annotation_name in Annotations:
    sub_annotations_list = []

    each_box = annotation_name['bbox']
    each_id = annotation_name['image_id']
    sub_annotations_list.append(each_id)
    sub_annotations_list.append(each_box)

    tmp_annotations_list.append(sub_annotations_list)

#produce the annotation list of images according to the path list
final_image_annotations_list = []
for item_number in range(len(image_id_list)):
    sub_annotations_list = []

    for item_annotation in image_id_list[item_number]:
        for item_id in range(len(tmp_annotations_list)):
            if tmp_annotations_list[item_id][0] == item_annotation:
                sub_annotations_list.append(tmp_annotations_list[item_id])
    
    final_image_annotations_list.append(sub_annotations_list)


#produce images
total_start_time = time.time()
item = 0
while item < len(path_list):

    image_list = sorted(tmp_image_number_list[item], key=lambda x: x[1])
    annotation_list = final_image_annotations_list[item]
    video_path = '/rscratch/data/ego4d_data/pre_pnr_post_frames/full_scale/'+ path_list[item] + '.mp4'
    vc=cv2.VideoCapture(video_path)
    if vc.isOpened():
        vc.set(cv2.CAP_PROP_POS_FRAMES,image_list[0][1])
        rep,frame=vc.read()
    else:
        rep=False 


    save_root = '/rscratch/data/ego4d_data/' + path_list[item] + '/'
    if not os.path.isdir(save_root):
        os.mkdir(save_root)
        
    j = 0

    sub_start_time = time.time()
    for i in range(len(image_list)):
        vc.set(cv2.CAP_PROP_POS_FRAMES,image_list[i][1])
        rep,frame=vc.read()

        #draw the bbox (use the "while" loop)

        if len(annotation_list) != 1:
            while image_list[i][0] == annotation_list[0][0]:
                NW_Point_x = annotation_list[0][1][0]
                NW_Point_y = annotation_list[0][1][1]
                SE_Point_x = annotation_list[0][1][0] + annotation_list[0][1][2]
                SE_Point_y = annotation_list[0][1][1] + annotation_list[0][1][3]
                
                # p1_Northwest point     p2_Southeast point
                frame = cv2.rectangle(frame, (int(NW_Point_x),int(NW_Point_y)), (int(SE_Point_x),int(SE_Point_y)), (0,255,0) , 2)
                del annotation_list[0]
        else:
            if image_list[i][0] == annotation_list[0][0]:
                NW_Point_x = annotation_list[0][1][0]
                NW_Point_y = annotation_list[0][1][1]
                SE_Point_x = annotation_list[0][1][0] + annotation_list[0][1][2]
                SE_Point_y = annotation_list[0][1][1] + annotation_list[0][1][3]
                
                # p1_Northwest point     p2_Southeast point
                frame = cv2.rectangle(frame, (int(NW_Point_x),int(NW_Point_y)), (int(SE_Point_x),int(SE_Point_y)), (0,255,0) , 2)
                del annotation_list[0]

        cv2.imwrite(save_root + str(image_list[i][1]) +'.jpg',frame)
        print("the %d_%d image has been produced" %(image_list[i][1],j))
        j += 1
    
    vc.release()

    sub_end_time = time.time()
    string = "all images of " + path_list[item] + " has been produced, totally concluding " + str(len(image_list)) +" images"
    print(string)
    print("This path spend %d seconds" %(sub_end_time-sub_start_time))

    item += 1

total_end_time = time.time()
print("all images have been produced, total time is %d seconds" %(total_end_time-total_start_time))