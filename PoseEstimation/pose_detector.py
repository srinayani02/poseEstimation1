import cv2
import mediapipe as mp

class PoseDetector():
    def __init__(self, staticImageMode=False, modelComplexity=1, smoothLandmarks=True,
                 enableSegmentation=False, smoothSegmentation=True, 
                 minDetectionConfidence=0.5, minTrackingConfidence=0.5):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(staticImageMode, modelComplexity, smoothLandmarks,
                                     enableSegmentation, smoothSegmentation,
                                     minDetectionConfidence, minTrackingConfidence)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
