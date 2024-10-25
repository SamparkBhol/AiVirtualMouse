
from HandTrackingModule import HandDetector
import cv2
import numpy as np
import time
import pyautogui

# Disable pyautogui's failsafe
pyautogui.FAILSAFE = False

class AIVirtualMouse:
    def __init__(self):
        self.wCam, self.hCam = 640, 480
        self.frameR = 100  # Frame Reduction
        self.smoothening = 7
        
        # Initialize previous and current locations
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        
        # Get screen size
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)  # Try 0 first, if not working try 1
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)
        
        # Initialize hand detector
        self.detector = HandDetector(maxHands=1)
        
        # FPS variables
        self.pTime = 0
        
    def run(self):
        while True:
            # 1. Capture and process frame
            success, img = self.cap.read()
            if not success:
                print("Failed to grab frame")
                break
                
            # Flip the image horizontally for a later selfie-view display
            img = cv2.flip(img, 1)
            
            # 2. Find hand landmarks
            img = self.detector.findHands(img)
            lmList, bbox = self.detector.findPosition(img)
            
            # 3. Process hand landmarks if detected
            if lmList:
                # Get coordinates of index and middle fingertips
                x1, y1 = lmList[8][1:]  # Index finger
                x2, y2 = lmList[12][1:]  # Middle finger
                
                # 4. Check which fingers are up
                fingers = self.detector.fingersUp()
                
                # Draw active area rectangle
                cv2.rectangle(img, (self.frameR, self.frameR), 
                            (self.wCam - self.frameR, self.hCam - self.frameR),
                            (255, 0, 255), 2)
                
                # 5. Moving Mode - Index finger up, middle finger down
                if fingers[1] == 1 and fingers[2] == 0:
                    # Convert coordinates
                    x3 = np.interp(x1, (self.frameR, self.wCam - self.frameR), (0, self.screen_width))
                    y3 = np.interp(y1, (self.frameR, self.hCam - self.frameR), (0, self.screen_height))
                    
                    # Smooth values
                    self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
                    self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening
                    
                    # Move mouse
                    try:
                        pyautogui.moveTo(self.screen_width - self.clocX, self.clocY)
                    except pyautogui.FailSafeException:
                        pass
                        
                    # Visual feedback
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    self.plocX, self.plocY = self.clocX, self.clocY
                
                # 6. Clicking Mode - Both index and middle fingers up
                if fingers[1] == 1 and fingers[2] == 1:
                    # Find distance between fingers
                    length, img, lineInfo = self.detector.findDistance(8, 12, img)
                    
                    # Click if fingers are close together
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()
                        # Add small delay to prevent multiple clicks
                        time.sleep(0.1)
            
            # 7. Calculate and display FPS
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
            
            # 8. Display the image
            cv2.imshow("AI Virtual Mouse", img)
            
            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    mouse = AIVirtualMouse()
    mouse.run()