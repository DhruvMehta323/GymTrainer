import cv2 as cv
import mediapipe as mp
import time
import math
class poseDetector():
    def __init__(self, mode=False,smooth=True, detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        # self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        smooth_landmarks=True,
        static_image_mode=False
    )

    def findPose(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    img, self.results.pose_landmarks,
                    self.mpPose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mpDraw.DrawingSpec(
                        color=(0, 0, 255), thickness=2, circle_radius=2
                    ),
                    connection_drawing_spec=self.mpDraw.DrawingSpec(
                        color=(0, 255, 0), thickness=2
                    )
                )

        return img
    
    def findPosition(self,img,draw=True):
        self.lmList=[]
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                cx=int((lm.x)*w)
                cy=int((lm.y)*h)
                
                self.lmList.append([id,cx,cy])
                #print(lmList)
                if draw:
                    cv.circle(img,(cx,cy),10,(255,0,0),cv.FILLED)
        
        return self.lmList

    def findAngle(self,img,p1,p2,p3,draw=True):#p1,p2,p3 are index values of points
        #Get Landmarks
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        x3,y3=self.lmList[p3][1:]
        
        #Calc Angle
        angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        if angle<0:
            angle+=360
        #print(angle)
        #Draw
        if draw:
            cv.line(img,(x1,y1),(x2,y2),(255,255,255),5)
            cv.line(img,(x3,y3),(x2,y2),(255,255,255),5)
            cv.circle(img,(x1,y1),10,(0,0,255),cv.FILLED)
            cv.circle(img,(x2,y2),10,(0,0,255),cv.FILLED)
            cv.circle(img,(x3,y3),10,(0,0,255),cv.FILLED)
            cv.circle(img,(x1,y1),15,(0,0,255),2)
            cv.circle(img,(x2,y2),15,(0,0,255),2)
            cv.circle(img,(x3,y3),15,(0,0,255),2)
            cv.putText(img,str(int(angle)),(x2-35,y2+35),cv.FONT_HERSHEY_PLAIN,1,(100,0,100),2)
    
        return angle        
        

    
    
    
def main():
    video_path = 'videos/pose5.mp4'
    capture = cv.VideoCapture(video_path)

    prevTime = 0
    detector = poseDetector(detectionCon=0.5, trackingCon=0.5)
    
    while True:
        success, img = capture.read()

        # Check if the frame is empty
        if not success or img is None:
            break

        img = cv.resize(img, (600, 600))
        
        detector.findPose(img)
        lmList=detector.findPosition(img,draw=False)
        print(lmList[14])#right elbow
        cv.circle(img,(lmList[14][1],lmList[14][2]),10,(255,0,0),cv.FILLED)   
        
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime
        cv.putText(img, str(int(fps)), (10, 30), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        cv.imshow("Video", img)
        key = cv.waitKey(1)
        
        

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
