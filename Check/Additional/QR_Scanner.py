from pyzbar import pyzbar
from Additional.User_Data import UserData
import cv2


class Scanner:
    def __init__(self):
        self.scanned_data = []

    def qr_live(self):
        cam = cv2.VideoCapture(0)
        while True:
            ret, image = cam.read()
            scan_list = pyzbar.decode(image)
            for each_scan in scan_list:
                data = {}
                data["points"] = each_scan.rect
                data["text"] = each_scan.data.decode("utf-8")
                data["type"] = each_scan.type
                self.scanned_data.append(data)
                (x, y, w, h) = data["points"]
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 225), 1)
                text = "{}".format(data["text"])
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if len(scan_list) > 0:
                return data["text"]
            """
            cv2.imshow("Image", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        cam.release()
        """

    def qr_scan(self, file="img.png", img_dir=""):
        img_file = img_dir + "\\" + file
        image = cv2.imread(img_file)

        scan_list = pyzbar.decode(image)
        for each_scan in scan_list:
            data = {}
            data["points"] = each_scan.rect
            data["text"] = each_scan.data.decode("utf-8")
            data["type"] = each_scan.type
            self.scanned_data.append(data)
            (x, y, w, h) = data["points"]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 225), 1)
            text = "{}".format(data["text"])
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Image", image)
        output_file = img_dir + "\\scanned-" + file
        cv2.imwrite(image, output_file)
        cv2.waitKey(0)