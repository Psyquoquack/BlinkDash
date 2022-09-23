import cv2
import cvzone     
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
import keyboard
from time import sleep

#Mettre en place toutes les variables

cap = cv2.VideoCapture(0) 

i=0
ratio=0
#VarSetup=0
text=""

detector = FaceMeshDetector(maxFaces=1)

leftEyeLandmarks = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]

plotY = LivePlot(640, 360, [200,500], invert=True)

BLACK = (255,255,255)
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 1.1
font_color = BLACK
font_thickness = 2
x,y = 20,30

while True:
    # Recuperer la cam
    retval, frame = cap.read()

    # Exit si pas de cam
    if not retval:
        break

    # Avoir les mesh de la tete     
    frame, faces = detector.findFaceMesh(frame, draw=False)

    if faces:
        #if VarSetup > 20:
        #    text="CLOSE EYE"

        face = faces[0]
        # Appliquer le visu
        for i in leftEyeLandmarks:
            cv2.circle(frame, face[i], 5, (255,0,255), cv2.FILLED)

        # Les points clé
        topEyelid = face[159]
        bottomEyelid = face[23]
        leftCorner = face[130]
        rightCorner = face[243]
        
        # distance verical
        lengthVer,_ = detector.findDistance(topEyelid, bottomEyelid)

        # horizontal
        lengthHor,_ = detector.findDistance(leftCorner, rightCorner)

        # Lgne Vertical
        cv2.line(frame, topEyelid, bottomEyelid, (0, 200, 0), 3)

        # ligne horizontale
        cv2.line(frame, leftCorner, rightCorner, (0, 200, 0), 3)

        # Ratio ( distance etc...)
        ratio = int((lengthVer/lengthHor) * 1000)

        # appuyer bonton si en dessous de ratio
        if ratio < 345: #and text != "CLOSE EYE":
            keyboard.press("space")
            keyboard.release("space")
            text='CLOSE'
        else:
            text='OPEN'
            #if text != "CLOSE EYE":
            #    text='OPEN'
            #else:
#
#                VarSetup= VarSetup+1
        
        # Appliquer tout les filtre
        imgPlot = plotY.update(ratio)
        frame = cv2.resize(frame, (640, 420))
        imgPlotText = cv2.putText(imgPlot, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
        frameStack = cvzone.stackImages([frame,imgPlotText], 1, 1)
        i=0

    else:
        # Cree les fenétre
        if i==0:
            imgPlot = plotY.update(ratio)
            i=1
        #Afficher pas de tete detecter si pas de tete
        frame = cv2.resize(frame, (640, 420))
        imgPlotText = cv2.putText(imgPlot, "NO FACE DETECTED", (x,y), font, font_size, (0,0,255), font_thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, "NO FACE DETECTED", (x,y), font, font_size, (0,0,255), font_thickness, cv2.LINE_AA)
        frameStack = cvzone.stackImages([frame,imgPlotText], 1, 1)

    # OUvrir
    cv2.imshow("BlinkDash1.0", frameStack)
 
    #cooldown
    key = cv2.waitKey(1)

    # escp 
    if key == 27:
        break 
    #sleep(1)

cap.release()
cv2.destroyAllWindows()
