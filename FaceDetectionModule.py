import cv2
import mediapipe as mp
import time

class FaceDetector():
    def __init__(self, minDetectionCon = 0.5, model_selection = 0):
        self.minDetectionCon = minDetectionCon
        self.model_selection = model_selection

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon,self.model_selection)

    def findFaces(self, img, draw=True, drawColor=(0, 255, 0)):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.faceDetection.process(imgRGB)

        bboxs = []

        if self.result.detections:
            for id, detection in enumerate(self.result.detections):
                # if id == 0:
                #     drawColor = (255, 0, 0)
                # elif id == 1:
                #     drawColor = (0, 255, 0)
                # elif id == 2:
                #     drawColor = (0, 0, 255)
                # elif id == 3:
                #     drawColor = (255, 0, 255)

                # mpDraw.draw_detection(img,detection)
                # print(id, detection)
                # print(detection.score)
                # print(detection.location_data.relative_bounding_box)
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)

                bboxs.append([id, bbox, detection.score])
                if draw:
                    img = self.fancyDraw(img, bbox, drawColor)
                    cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 2, drawColor, 2)

        return img, bboxs

    def fancyDraw(self, img, bbox, drawColor, l=30, t=2, rt=0):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h

        cv2.rectangle(img, bbox, drawColor, rt)
        ### Top Left x,y
        cv2.line(img, (x,y), (x+l,y), drawColor, t)
        cv2.line(img, (x, y), (x, y + l), drawColor, t)
        ### Top Right x1,y
        cv2.line(img, (x1, y), (x1 - l, y), drawColor, t)
        cv2.line(img, (x1, y), (x1, y + l), drawColor, t)
        ### Bottom Left x,y1
        cv2.line(img, (x, y1), (x + l, y1), drawColor, t)
        cv2.line(img, (x, y1), (x, y1 - l), drawColor, t)
        ### Botom Right x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), drawColor, t)
        cv2.line(img, (x1, y1), (x1, y1 - l), drawColor, t)
        return img

def main():
    cap = cv2.VideoCapture("Videos/show1.mp4")
    pTime = 0
    detector = FaceDetector(model_selection=1)
    while True:
        success, img = cap.read()

        img, bboxs = detector.findFaces(img)
        # print(bboxs)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()