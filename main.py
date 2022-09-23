import cv2
import numpy as np
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
model = load_model('best.h5')

import random
import os
import easy_pyttsx3 as pt





def crop_image(image, x, y, width, height):
    return image[y:y + height, x:x + width]

def keras_predict(model, image):
    data = np.asarray(image, dtype="int32")

    pred_probab = model.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class
def prediction(pred):
    return(chr(pred+ 65))

cap = cv2.VideoCapture(0)
counter=0
while True:
    ret, frame = cap.read()
    counter=counter+1
    frame_resized=crop_image(frame, 300,300,300,300)
    image_grayscale = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

    image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15, 15), 0)
    resized_img = cv2.resize(image_grayscale_blurred, (28, 28),interpolation = cv2.INTER_AREA)

    im4 = np.resize(resized_img, (28, 28, 1))
    im5 = np.expand_dims(im4, axis=0)
    a=""
    pred_probab, pred_class = keras_predict(model, im5 )
    cv2.rectangle(frame, (400, 300), (600, 600), (0, 255, 0), 3)
    curr = prediction(pred_class)
    cv2.putText(frame, "AI ASL system", (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), lineType=cv2.LINE_AA)
    cv2.putText(frame, "by Murat Ali", (400, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), lineType=cv2.LINE_AA)
    cv2.imshow('Camera',frame)


    print(curr,pred_probab)

    #print(counter)
    if curr=="B" and pred_probab > 0.7:
        pt.say("Hello")
        a="hello"
    if curr=="G" and pred_probab > 0.7:
        pt.say("How are you")
    if curr == "P" and pred_probab > 0.9:
        pt.say("Thank You")
    if curr == "W" and pred_probab > 0.9:
        pt.say("See you")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break
