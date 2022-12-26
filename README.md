# faceblur
Usage: bluring faces in a photos

packages
apt-get install python-opencv
apt-get install opencv-data

For using this program type in command line
python face.py

Program search for a list of photos in directory which is named by current year -> month -> day
next sorting it by the creation time and checks every 10 secons for new files.
If there is no new file then loggingINFO shows the message: There is no new file in the direcotry
If camera tooks a new photo and sent it to the directory then program starts a method for face analysing.
logging shows a message: Detection begin..
If any face appear in a photo then program blur it and overwritews a file.

Program search only for last new file because 10 seconds is an optimal time for camera to took a photo, there is no need to search all the files repeatedly.

Program once executed can run all the time.





