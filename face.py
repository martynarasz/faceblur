import sys

import cv2
import os
import datetime
import logging
import time
import errno

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s',
                    filename="detect_log")


class Directory:
    def __init__(self):
        self.today = datetime.datetime.now()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        if self.month <= 9:
            self.month = "0{}".format(self.month)
        if self.day <= 9:
            self.day = "0{}".format(self.day)
        self.id = ["013-420", "013-421", "013-422"]
        self.month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                           "11", "12"]
        self.day_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
                         "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                         "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                         "31"]
        self.update_date()
    def process_directory(self):
        try:
            while True:

                for ids in self.id:
                    self.dir_path = "/var/dav/davserver/lpn_snapshots/%s/%s/%s/%s" % (self.year, self.month,
                                                                                              self.day, ids)
                    # self.dir_path = "C:\\Users\\Delta\\%s\\%s\\%s\\%s" % (self.year, months, days, ids)
                    exists = os.path.exists(self.dir_path)
                    time.sleep(1)
                    if not exists:
                        continue
                    else:
                        print(self.dir_path)
                        os.chdir(self.dir_path)
                        self.files = os.listdir(self.dir_path)
                        os.path.exists(self.dir_path)
                        self.list_of_files = sorted(self.files, key=os.path.getctime)
                        try:
                            for item in self.list_of_files:
                                detection = Detect()
                                detection.detection_rectangle(os.path.join(self.dir_path, item))
                                logging.debug("ostatnia sciezka to %s A ZDJECIE TO %s " % (self.dir_path, item))
                        except AttributeError:
                            logging.error("Directory is not yet created")
                            Directory.__init__(self)
        except OSError:
            logging.error("Directory is not yet created")
            time.sleep(10)
    def update_date(self):
            while True:
                current_day = datetime.datetime.now().day
                current_month = datetime.datetime.now().month
                if current_day != self.day:
                    self.day = current_day
                    self.day = "0{}".format(self.day) if self.day <= 9 else str(self.day)
                    self.process_directory()
                if current_month != self.month:
                    self.month = "0{}".format(self.month) if self.month <= 9 else str(self.month)


# cascades = cv2.CascadeClassifier("C:\\Users\\Delta\\Downloads\\haarcascade_frontalface_default.xml")

cascades = cv2.CascadeClassifier("/usr/src/faceblur-new/haarcascade_frontalface_default.xml")


class Detect:
    def __init__(self):
        logging.debug("Detection begin")

    def detection_rectangle(self, img):
        self.pic = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        face_rect = cascades.detectMultiScale(self.pic, 1.1, 4)
        for (x, y, w, h) in face_rect:
            # cv2.rectangle(self.pic, (x, y), (x+w, y+h), (0, 0, 0), thickness=0)
            rec = self.pic[y:y + h, x:x + w]
            blur = cv2.GaussianBlur(rec, (23, 23), 0)
            self.pic[y:y + h, x:x + w] = blur
            # overvrites a file
            cv2.imwrite(img, self.pic)
            # self.test_display()# testing only

    def test_display(self):
        cv2.imshow('Detected faces', self.pic)
        cv2.waitKey(0)


if __name__ == '__main__':
  dr = Directory()
