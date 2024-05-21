import cv2 as cv
from PIL import ImageGrab, Image
import numpy as np

region = (300, 300, 600, 900)
correct_i = cv.imread('./screenshots/correct"I".png')




def locate_opencv_pil():
    img = ImageGrab.grab(bbox=region)
    img_np = np.array(img)
    img_cv = cv.cvtColor(img_np, cv.COLOR_RGB2BGR)  # Convert PIL to OpenCV format
    res = cv.matchTemplate(img_cv, correct_i, cv.TM_CCORR)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        return True
    else:
        return False

print(locate_opencv_pil())