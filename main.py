import cv2
import numpy as np
import winsound
import openfoodfacts
from pyzbar.pyzbar import decode

global UPC

def beep():
    winsound.Beep(2500, 500)


def searchOpenFoodFacts(barCode):
    product = openfoodfacts.products.get_product(barCode)
    print(product['product']["product_name"])


def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)

        cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        beep()

        return barcodeData



cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    UPC = decoder(frame)

    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
    if UPC is not None:
        try:
            searchOpenFoodFacts(UPC)
        except:
            print("Open Food Facts did not return a result for this item")
            continue
