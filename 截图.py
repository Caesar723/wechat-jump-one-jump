import pyautogui
import cv2
import numpy as np
import math
import pynput
import time

def catch():
    img = pyautogui.screenshot(region=[2080,300,780,1000]) # x,y,w,h
    img.save('screenshot.png')
    img = cv2.imread('screenshot.png')
    #cv2.imshow('h',img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
def clear(img):

    img = img
    recode=img[0][0]
    print(np.float32([1.009,1.009,1.009]))
    for i in range(0,len(img)):
        for a in range(0,len(img[0])):

            if all(recode/img[i,a]<np.float32([1.03,1.03,1.03])) and all(recode/img[i,a]>np.float32([0.97,0.97,0.97])):
                img[i,a]=recode


            else:
                recode=img[i,a]
    return img

def show():
    global body,top,Core
    first=[0,0]
    last=[0,0]
    close = 0
    open1=False
    getarr=[]
    img=cv2.imread("screenshot.jpeg")
    #img=clear(img)
    get=cv2.imread("screenshot.jpeg",0)
    b, g, r = cv2.split(img)
    get = cv2.GaussianBlur(get, (3, 3), 0)
    canny = cv2.Canny(b,80, 40)

    new=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    low=np.int32([90,25,45])
    up=np.int32([135,125,130])
    new=cv2.inRange(new,low,up)

    for d in range(0,len(canny)):
        for e in range(0,len(canny[0])):

            if canny[d][e]==255:
                wdf=[e,d+30]
                close=1

                break
        if close==1:
            break
    top=[wdf[0],wdf[1]-30]
    print(top,"top")##最顶
    #cv2.imshow('w',canny)#231,130
    #cv2.waitKey()
    bodyArr=[]
    for f in range(0,len(canny)-380):
        recodeBody=0
        bodyCounter=0
        for g in range(0,int(len(canny[0])/2)):

            if wdf[0]>int(len(canny[0])/2):
                if new[f,g]==255:
                    body=[g,f-30]
                    recodeBody += body[0]
                    bodyCounter += 1


            else:
                if new[f,g+int(len(canny[0])/2)]==255:
                    body=[g+int(len(canny[0])/2),f-30]
                    recodeBody+=body[0]
                    bodyCounter+=1

        if bodyCounter>0:
            bodyArr.append(recodeBody/bodyCounter)


    body[0]=int(bodyArr[len(bodyArr)-1])
    print(body,"body")##棋子位置
    mask = np.zeros([len(canny) + 2, len(canny[0]) + 2], np.uint8)
    cv2.floodFill(img, mask,(wdf[0],wdf[1]), (255, 0, 255), (11, 11, 11), (10, 10, 10), cv2.FLOODFILL_FIXED_RANGE)
    kx=np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=np.float32)
    ky=np.ones((3,3))/9
    e=cv2.filter2D(b,cv2.CV_64F,kx)
    e2=cv2.filter2D(img,-1,ky)
    for h in range(0,len(img)):
        for j in range(0,len(img[0])):
            if all(img[h,j]==[255,0,255]) and open1==False:
                first=[j,h]
                open1=True
                print(first)#紫色最上
            elif all(img[h,j]==[255,0,255]) and open1==True:
                last=[j,h]
    print(last)#紫色最下
    Core=getCore(first,last)
    print(Core,"core")
    cv2.circle(img,(Core[0],Core[1]),1,(0,255,0),10)
    cv2.circle(img, (body[0], body[1]), 1, (0, 0, 255), 10)
    cv2.imshow('k',img)
    cv2.namedWindow('m',0)
    cv2.moveWindow('m',390,0)
    cv2.imshow('m',canny)

def getCore(first,last):
    x=int((first[0]+last[0])/2)
    y=int((first[1]+last[1])/2)
    return [x,y]
def measure(body,top,Core):
    diff=(top[0]-body[0])*1.1474
    if diff<0:
        diff=-diff
    diff2=math.sqrt((body[0]-Core[0])*(body[0]-Core[0])+(body[1]-Core[1])*(body[1]-Core[1]))
    print(diff,diff2)
    if (diff-diff2)>30 or (diff-diff2)<-30:
        tim=diff/467.36
        print(tim)
        return tim
    else:
        tim=diff2/467.36
    print(tim)
    return tim
def mouse(tim):
    ctr=pynput.mouse.Controller()
    ctr.position=(1300,100)
    ctr.press(pynput.mouse.Button.left)
    time.sleep(tim-0.04)
    ctr.release(pynput.mouse.Button.left)


#while True:
    #catch()
show()
cv2.waitKey(0)
    #mouse(measure(body,top,Core))
a=measure(body,top,Core)
    #time.sleep(2)


