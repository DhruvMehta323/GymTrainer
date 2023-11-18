import cv2 as cv
import numpy as np
import mediapipe as mp
import time

import Pose as pm
exercise = input("Choose an exercise (bicep curls, tricep curls, bench press, leg press): ").lower()
if exercise=='bicep curls':
    Path='videos/bicepCurls.mp4'
if exercise=='tricep curls':
    Path='videos/tricepCurls.mp4'
if exercise=='bench press':
    Path='videos/benchPress.mp4'
if exercise=='leg press':
    Path='videos/legPress.mp4'
#You can change your path

capture=cv.VideoCapture(Path)
detector=pm.poseDetector()

count=0
dir=0
prevTime=0

while True:
    success,img=capture.read()
    img=cv.resize(img,(720,480))
    img=detector.findPose(img,False)
    lmList=detector.findPosition(img,False)
    #print(lmList)
    if len(lmList)!=0:
        if exercise == 'bicep curls':
            angle=detector.findAngle(img,12,14,16)
            percent=np.interp(angle,(65,165),(0,100))
            bar=np.interp(angle,(65,165),(360,60))
            if percent==100:
                if dir==0:
                    count+=0.5
                    dir=1
            if percent==0:
                if dir==1:
                    count+=0.5
                    dir=0
            
            cv.rectangle(img,(600,60),(650,360),(0,100,200),3)
            cv.rectangle(img,(600,int(bar)),(650,360),(0,255,0),cv.FILLED)
            cv.putText(img,f'{int(percent)}%',(600,50),cv.FONT_HERSHEY_COMPLEX,1,(0,100,200),2)
            cv.rectangle(img,(15,10),(150,40),(0,0,0),cv.FILLED)
            cv.putText(img,f'Count:{str(int(count))}',(20,35),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        
        elif exercise == 'tricep curls':
            angle=detector.findAngle(img,12,14,16)
            percent=np.interp(angle,(65,165),(0,100))
            bar=np.interp(angle,(65,165),(360,60))
            if percent==100:
                if dir==1:
                    count+=0.5
                    dir=0
            if percent==0:
                if dir==0:
                    count+=0.5
                    dir=1
            
            cv.rectangle(img,(600,60),(650,360),(0,100,200),3)
            cv.rectangle(img,(600,int(bar)),(650,360),(0,255,0),cv.FILLED)
            cv.putText(img,f'{int(percent)}%',(600,50),cv.FONT_HERSHEY_COMPLEX,1,(0,100,200),2)
            
            cv.rectangle(img,(15,10),(150,40),(0,0,0),cv.FILLED)
            cv.putText(img,f'Count:{str(int(count))}',(20,35),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        
        elif exercise == 'bench press':
            angle=detector.findAngle(img,11,13,15)
            angle=detector.findAngle(img,12,14,16)
            percent=np.interp(angle,(180,350),(0,100))
            bar=np.interp(angle,(180,350),(360,60))
            if percent==100:
                if dir==0:
                    count+=0.5
                    dir=1
            if percent==0:
                if dir==1:
                    count+=0.5
                    dir=0
            
            cv.rectangle(img,(600,60),(650,360),(0,100,200),3)
            cv.rectangle(img,(600,int(bar)),(650,360),(0,255,0),cv.FILLED)
            cv.putText(img,f'{int(percent)}%',(600,50),cv.FONT_HERSHEY_COMPLEX,1,(0,100,200),2)
            
            cv.rectangle(img,(15,10),(150,40),(0,0,0),cv.FILLED)
            cv.putText(img,f'Count:{str(int(count))}',(20,35),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),2)    
        
        elif exercise == 'leg press':
            angle=detector.findAngle(img,24,26,28)
            angle2=detector.findAngle(img,23,25,27)
            percent=np.interp(angle,(230,270),(0,100))
            bar=np.interp(angle,(230,270),(60,360))
            if percent==100:
                if dir==0:
                    count+=0.5
                    dir=1
            if percent==0:
                if dir==1:
                    count+=0.5
                    dir=0
            
            cv.rectangle(img,(600,60),(650,360),(0,100,200),3)
            cv.rectangle(img,(600,int(bar)),(650,360),(0,255,0),cv.FILLED)
            cv.putText(img,f'{int(100)-int(percent)}%',(600,50),cv.FONT_HERSHEY_COMPLEX,1,(0,100,200),2)
            
            cv.rectangle(img,(15,10),(150,40),(0,0,0),cv.FILLED)
            cv.putText(img,f'Count:{str(int(count))}',(20,35),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        
        

    cv.imshow("Video",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
capture.release()
cv.destroyAllWindows()

