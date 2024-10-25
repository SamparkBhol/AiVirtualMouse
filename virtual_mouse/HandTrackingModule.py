# hand_tracking.py
import cv2
import mediapipe as mp
import math
import numpy as np

class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        # Initialize mediapipe hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]  # Finger tip landmarks
        self.results = None
        self.lmList = []

    def findHands(self, img, draw=True):
        """Find hands in the image"""
        # Convert BGR to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process the image
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, 
                    handLms,
                    self.mpHands.HAND_CONNECTIONS,
                    self.mpDraw.DrawingSpec(color=(255,0,255), thickness=2, circle_radius=2),
                    self.mpDraw.DrawingSpec(color=(255,255,255), thickness=2)
                )
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """Find position of hand landmarks"""
        self.lmList = []
        xList, yList = [], []
        bbox = []
        
        if self.results.multi_hand_landmarks:
            try:
                myHand = self.results.multi_hand_landmarks[handNo]
                
                for id, lm in enumerate(myHand.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy])
                    xList.append(cx)
                    yList.append(cy)
                    
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                
                # Calculate bounding box
                if xList and yList:
                    xmin, xmax = min(xList), max(xList)
                    ymin, ymax = min(yList), max(yList)
                    bbox = xmin, ymin, xmax, ymax
                    
                    if draw:
                        cv2.rectangle(img, (xmin - 20, ymin - 20),
                                    (xmax + 20, ymax + 20), (0, 255, 0), 2)
            except IndexError:
                pass
                
        return self.lmList, bbox

    def fingersUp(self):
        """Check which fingers are up"""
        fingers = []
        
        if len(self.lmList) >= 21:  # Ensure we have all landmarks
            # Thumb
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        """Find distance between two landmarks"""
        if len(self.lmList) >= max(p1, p2):
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
                cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
                
            length = math.hypot(x2 - x1, y2 - y1)
            return length, img, [x1, y1, x2, y2, cx, cy]
            
        return None, img, None