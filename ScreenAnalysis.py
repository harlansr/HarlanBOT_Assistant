import cv2
import time
import numpy as np
import time
from PIL import ImageGrab
import FaceDetectionModule as fdm

import requests
import webbrowser


class ScreenAnalysis:
    def __init__(self, timeout=120, crop=True, crop_space=100, search=True, showAuto=True):
        self.timeout = timeout
        self.crop = crop
        self.crop_space = crop_space
        self.search = search
        self.showAuto = showAuto

    def checkFace(self):
        result = self._checkScreenFaceRun()
        if result:
            print("-- FIND FACE --")
        else:
            print("-- FACE NOT FOUND --")
        return result


    def _checkScreenFace(self):
        screen = np.array(ImageGrab.grab())
        # img = cv2.imread("lenna.png")
        screenBGR = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        detector = fdm.FaceDetector(model_selection=3)
        img, bboxs = detector.findFaces(screenBGR, draw=False)

        return img, bboxs

    def _checkScreenFaceRun(self, show=1):
        done = False
        countScan = self.timeout


        while not done:
            img, bboxs = self._checkScreenFace()
            if len(bboxs) != 0 or countScan<=0:
                done = True
                # print(bboxs)
            countScan-=1

        if len(bboxs) != 0:
            c_bbox = bboxs[0]
            # print(c_bbox[2][0])

            if self.crop:
                if len(bboxs) > 1:
                    for f_bbxx in bboxs:
                        if f_bbxx[2][0]>c_bbox[2][0]:
                            c_bbox = f_bbxx
                bbox = c_bbox[1]
                x, y, w, h = bbox
                x1, y1 = x + w, y + h
                img = img[y-self.crop_space:y1 + self.crop_space, x-self.crop_space:x1 + self.crop_space]

            if self.showAuto:
                if show>0:
                    cv2.imshow("Image", img)
                    cv2.waitKey(1)
                    time.sleep(show)
            else:
                cv2.imshow("Image", img)
                cv2.waitKey(0)

            if self.search:
                filePath = 'image/screen-face.jpg'
                cv2.imwrite(filePath, img)
                searchUrl = 'http://www.google.com/searchbyimage/upload'
                multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
                response = requests.post(searchUrl, files=multipart, allow_redirects=False)
                fetchUrl = response.headers['Location']
                webbrowser.open(fetchUrl)

            return True
        else:
            return False

