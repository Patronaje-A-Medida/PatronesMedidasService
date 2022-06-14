import mediapipe as mp
import cv2
import numpy as np


mp_pose = mp.solutions.pose
BG_COLOR = (0,0,0)

def process_body_person(image) -> any:
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        image_no_bg = image.copy()
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        image_no_bg = np.where(condition, image_no_bg, bg_image)
        image_no_bg[image_no_bg!=0]=255
        image_no_bg = cv2.cvtColor(image_no_bg, cv2.COLOR_RGB2GRAY)
        return image_no_bg