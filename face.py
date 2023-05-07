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
        self.year = today.year
        self.month = today.month
        self.day = today.day
        self.hour = today.hour
        self.id = ["013-420", "013-421", "013-422"]

        try:
            self.dir_path = "/home/skbb/Pictures/%s/%s/%s/%s" % (self.year, self.month, self.day, self.id[2])
            os.path.exists(self.dir_path)
            self.go_to_dir = os.chdir(self.dir_path)
            self.files = os.listdir(self.dir_path)
            os.path.exists(self.dir_path)
            self.list_of_files = sorted(self.files, key=os.path.getctime)
            # print(self.list_of_files)
        except OSError:
            logging.error("Directory is not yet created")

        while True:
            try:
                self.item = self.list_of_files[-1]
                assert self.item == self.list_of_files[-1]
                self.scan = self.new_files_check()
            except AttributeError:
                logging.error("Directory is not yet created")
                time.sleep(10)
                Directory.__init__(self)


    def new_files_check(self):
        # self.dir_path = "/var/dav/davserver/lpn_snapshots/%s/%s/%s/%s" % (self.year, self.month, self.day, self.id[0])
        self.dir_path = "/home/skbb/Pictures/%s/%s/%s/%s" % (self.year, self.month, self.day, self.id[2])
        self.go_to_dir = os.chdir(self.dir_path)
        self.files = os.listdir(self.dir_path)
        self.list_of_files = sorted(self.files, key=os.path.getmtime)
        # print(self.list_of_files)
        string = str(self.list_of_files[-1])
        if self.item != string:
           self.detection = Detect()
           self.scanning = self.detection.detection_rectangle(self.list_of_files[-1])
        else:
            logging.debug('There is no new file for detection')
        time.sleep(10)


cascades = cv2.CascadeClassifier("/home/skbb/Downloads/test/haarcascade_frontalface_default.xml")
# cascades = cv2.CascadeClassifier("/usr/src/faceblur/haarcascade_frontalface_default.xml")


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
