import cv2                                                                                                        #importing of libraries 
import numpy as np                                                                                                #NumPy is the fundamental package for scientific computing with Python

cap = cv2.VideoCapture('real.avi')                                                                                #To capture a video, you need to create a VideoCapture object. Its argument can be either the device index or the name of a video file

frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))                                                             #cv2.CAP_PROP_FRAME_WIDTH = width of frames in video stream 

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))                                                           #cv2.CAP_PROP_FRAME_HEIGHT = height of frames in video stream 

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')                                                                  #fourcc is 4-character code of codec used to compress the frames

out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))                                                      #save the output in video, parameteres are (flie name, fourcc, fps = framerate of created video stream, frame size(width ,height)


ret, frame1 = cap.read()                                                                                          #reading two frames from cap instance object frame1

ret, frame2 = cap.read()                                                                                          #reading two frames from cap instance object frame2

print(frame1.shape)

while cap.isOpened():                                                                                             #cap.isOpened is to know wheather they have initialised the capture or not

    diff = cv2.absdiff(frame1, frame2)                                                                            #absdiff method means absloute difference for finding the abs diff between frame 1 and frame 2
                        #source, code - to convert BGR to gray scale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)                                                                 #once we have diff we have to convert into gray scale mode , why because we have to find contours that will be easier to find contours in gray scale mode
                            #source, Kernel size (5,5), sigmaX value
    blur = cv2.GaussianBlur(gray, (5,5), 0)                                                                       #The Gaussian filter is a low-pass filter that removes the high-frequency components are reduced  
                              #source,thresh value 20, maxthresh value 255, type  
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)                                                   #threshold method is to compare the pixel with threshol value if the value is small its set to (0) and if not it set to maixmum (255)
                         #source,kernel, iterations
    dilated = cv2.dilate(thresh, None, iterations=3)                                                              #dialate the image to fill all the holes this helps us to find better contours  
                                   #source, mode         , method
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)                               #contours method is joinning all the points along the boundray line , if find both contours and hierarchy 

                                                              #once we have contours we have to apply on original frame 1,  contours , contoursID, color, thickness 
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)       
                                                              #by using Drawcontours we get some noises so we make comment it  


    for contour in contours:                                                                                       #now we make iterate over all contours by making list as contour in contours  

                                                                                                                   #next to save all the coordinates of found contours
        (x, y, w, h) = cv2.boundingRect(contour)                                                                   # x, y coordinates and width and height boundingrect is mainly used for draw an rectangle around the image    

                                                                                                                   #counter area method is if the are of tge contour is less the are we dont need contour
        if cv2.contourArea(contour) < 900:                                                                         #if the area is graater then we get a rectangle on image 
            continue                                                                                               #continue statement is used to skip the rest of the code inside a loop for the current iteration ,Loop does not terminate but continues on with the next iteration. 
                      #source,  point1, point2 ,  color , thickness
        cv2.rectangle(frame1, (x, y), (x+w, y+h), ( 0, 0, 255), 2)                                                 #cv2.rectangle is used to draw a rectangle on image
                     #source         ,text ,               origin ,  font face , font scale , color , thicknes
        cv2.putText(frame1, "Status: {}".format('walking'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)  #cv2.puttext is used put text on the image to notice  

                      #source, frame size 
    image = cv2.resize(frame1, (1280,720))                                                                         #cv2.resize to resize the image of all contours in frame 1  

    out.write(image)

    cv2.imshow("feed", frame1)                                                                                     #cv2.imshow show the all operation performed on the video will be saved in frame 1 and displayed

    frame1 = frame2                                                                                                #assign the value of frame 2 in frame1

    ret, frame2 = cap.read()                                                                                       #inside the frame 2 we reading a new frame in variable frame , reading the two frames and finding the difference between them 

    if cv2.waitKey(40) == 27:                                                                                      #waitKey function which displays the image for specified milliseconds if not it won't display the image    
        break                                                                                                      #breat statement terminates the loop containing in it

cv2.destroyAllWindows()                                                                                            #cv2.destroyallwindows will simply destroy all windows
cap.release()                                                                                                      #to off the camera we use cap.release()
out.release()
