import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image, ImageDraw, ImageFont

detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")

model_width = 448
model_height = 448
detection_threshold = 0.4

class_names = ('person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
                'train', 'truck', 'boat', 'traffic light', 'fire', 'hydrant',
                'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
                'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
                'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                'kite', 'baseball bat', 'baseball glove', 'skateboard',
                'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                'keyboard', 'cell phone', 'microwave oven', 'toaster', 'sink',
                'refrigerator', 'book', 'clock', 'vase', 'scissors',
                'teddy bear', 'hair drier', 'toothbrush')


def load_image(image_file_name):
    image = Image.open(image_file_name)
    image = image.resize((model_width, model_height))
    (im_width, im_height) = image.size
    image_arr = np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
    image_arr = image_arr[np.newaxis, ...]
    image.close()
    return image_arr


def detect_objects(img):
    image_tensor = load_image(img)
    boxes, scores, classes, num_detections = detector(image_tensor)
    detection_mask = scores > detection_threshold
    boxes_list = boxes[detection_mask].numpy().tolist()
    labels = [class_names[int(n - 1)] for n in classes[detection_mask].numpy()]

    # Processing Image
    with Image.open(img) as im:
        width, height = im.size
        ratio_width = width / model_width
        ratio_height = height / model_height
        draw = ImageDraw.Draw(im)
        fnt = ImageFont.truetype("consola.ttf", 20)
        for box in boxes_list:
            label = labels[boxes_list.index(box)]
            draw.rectangle([box[1] * ratio_width, box[0] * ratio_height, box[3] * ratio_width, box[2] * ratio_height],
                           fill=None, outline='red', width=2)
            draw.text((box[1] * ratio_width + 3, box[0] * ratio_height), label, font=fnt, fill='red', stroke_width=0)

        # write to stdout
        # im.save(sys.stdout, "PNG")
    return im

