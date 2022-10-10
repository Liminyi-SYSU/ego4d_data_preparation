# Ego4d_data_preparation
Capturing frames and drawing bounding-boxes from given videos

The DATA-FOLDER should be built like
```
    ${DATA_FOLDER}
    |-- coco_annotations
    |-- |-- trainval.json
    |   |-- train.json
    |   |-- val.json
    |-- pre_pnr_post_frames
        |-- video_id
        |   |-- frame_number.jpg
        |   |-- ...
        |-- ...
    ```

All videos are stored at the path(/rscratch/data/ego4d_data/pre_pnr_post_frames/full_scale)
