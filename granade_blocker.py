from pygame import *
from random import*
import os
import cv2
detector = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
cap = cv2.VideoCapture("http://192.168.2.252:8081")
#cap = cv2.VideoCapture(0)

expImg = []
explode = os.listdir("explode")
for i in explode:
    temp = image.load("explode/" + i)
    temp = transform.rotate(temp, 90)
    temp = transform.scale(temp, (160, 300))
    expImg.append(temp)


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
display.init()
display.set_caption("OpenCV Test")
screen = display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
grenade = image.load("grenade.png")
grenade = transform.scale(grenade, (50, 70))

fryingPan = image.load("fryingPan.png")
fryingPan = transform.rotate(fryingPan, 180)



def expSurf(frame, frame1):
    if frame - frame1 >= 11:
        return 0
    else:
        return expImg[frame - frame1]

init()
frame = 0
frame1 = 0
clock= time.Clock()
y = -30
x = randint(0,600)
xe = 0
ye = 0
fpx = 0
fpy = 0
fpw = 0

while True:

    if y >= SCREEN_HEIGHT:
        y = -30
        x = randint(100, 400)
    else:
        y += 20
    clock.tick(30)
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    imgSurf = surfarray.make_surface(img)
    imgSurf = transform.flip(imgSurf, False, True)
    imgSurf = transform.rotate(imgSurf, 270)
    screen.blit(imgSurf, (0, 0))
    screen.blit(grenade, (x, y))
    for (xf, yf, wf, hf) in faces:
        #draw.rect(screen, (200, 200, 200), (xf, yf, wf, hf), 1)
        pass
    try:
        fpx = faces[0][0]
        fpy = faces[0][1]
        fpw = faces[0][2]
    except:
        pass
    fryingPan = transform.scale(fryingPan, (300, 150))
    screen.blit(fryingPan, (fpx - 130, fpy - 100))

    if fpy - 80 <= y <= fpy + 100:
        if fpx <= x and fpx + fpw >= x + 50:
            frame1 = frame
            xe = x
            ye = y
            y = -30
            x = randint(100, 400)


    frame += 1
    if frame - frame1 < 11:
        screen.blit(expSurf(frame, frame1), (fpx, fpy-320))


    display.update()

    #img = surfarray.pixels_green(imgSurf)
    #cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()