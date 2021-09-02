import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

# img = cv2.imread("vehicles-will-soon-come-fitted-with-number-plates8-1522648047.jpg")
cap = cv2.VideoCapture(0)
ret, img = cap.read()
cv2.imwrite("C:/Users/laxma/Documents/task_08_Node/public/css/my.jpg", img)
photo = cv2.imread("C:/Users/laxma/Documents/task_08_Node/public/css/my.jpg")
cv2.imshow("Clicked Picture", photo)
cv2.waitKey()
cv2.destroyAllWindows()
cap.release()
img = cv2.resize(img, (600,400) )
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(gray,cv2.COLOR_BGR2RGB))

bfilter = cv2.bilateralFilter(gray, 13, 15, 15) #noise reduction
edged = cv2.Canny(bfilter, 30, 200)#edge detection
plt.imshow(cv2.cvtColor(edged,cv2.COLOR_BGR2RGB))

contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

location=None
for con in contours:

    peri = cv2.arcLength(con, True)
    approx = cv2.approxPolyDP(con, 10, True)

    if len(approx) == 4:
        location = approx
        break

#location

mask = np.zeros(gray.shape,np.uint8)
new_image = cv2.drawContours(mask,[location],0,255,-1,)
new_image = cv2.bitwise_and(img,img,mask=mask)

plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
cropped = gray[topx:bottomx+1, topy:bottomy+1]

plt.imshow(cv2.cvtColor(cropped,cv2.COLOR_BGR2RGB))

import easyocr
reader = easyocr.Reader(["en"])
result = reader.readtext(cropped)

result = result[0][1]


import requests
import xmltodict
import json

def user_details(number):

  r = requests.get(f"http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={number}&username=<username>")
  data = xmltodict.parse(r.content)
  jdata = json.dumps(data)
  df = json.loads(jdata)
  df1 = json.loads(df['Vehicle']['vehicleJson'])

  return [df1["Description"],
          df1["RegistrationYear"],
          df1["EngineSize"]["CurrentTextValue"],
          df1["NumberOfSeats"]["CurrentTextValue"],
          df1["VechileIdentificationNumber"],
          df1["EngineNumber"],
          df1["FuelType"]["CurrentTextValue"],
          df1["RegistrationDate"],
          df1["Location"]]
result1 = user_details(result)
print(result)


print(result1)
