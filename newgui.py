# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import image, vidcode
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
from utils import label_map_util
from utils import visualization_utils as vis_util

video,sess,detection_boxes,detection_scores,detection_classes,num_detections,image_tensor,category_index = vidcode.vid()
class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(563, 579)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imgButton = QtWidgets.QPushButton(self.centralwidget)
        self.imgButton.setGeometry(QtCore.QRect(10, 380, 181, 51))
        self.imgButton.setObjectName("imgButton")
        self.camButton = QtWidgets.QPushButton(self.centralwidget)
        self.camButton.setGeometry(QtCore.QRect(200, 380, 171, 51))
        self.camButton.setObjectName("camButton")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(200, 450, 171, 51))
        self.exitButton.setObjectName("exitButton")
        self.vidButton = QtWidgets.QPushButton(self.centralwidget)
        self.vidButton.setGeometry(QtCore.QRect(380, 380, 171, 51))
        self.vidButton.setObjectName("vidButton")
        self.display = QtWidgets.QLabel(self.centralwidget)
        self.display.setGeometry(QtCore.QRect(10, 10, 541, 361))
        self.display.setText("")
        self.display.setPixmap(QtGui.QPixmap("squeezedet.png"))
        self.display.setScaledContents(True)
        self.display.setObjectName("display")
        self.txt = QtWidgets.QLabel(self.centralwidget)
        self.txt.setGeometry(QtCore.QRect(200, 500, 171, 51))
        self.txt.setText("Hello World!")
        self.txt.setScaledContents(True)
        self.txt.setObjectName("text")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 563, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.imgButton.clicked.connect(self.imagedet)
        self.vidButton.clicked.connect(self.viddet)
        self.camButton.clicked.connect(self.camdet)
        self.exitButton.clicked.connect(self.exitdet)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.imgButton.setText(_translate("MainWindow", "Image"))
        self.camButton.setText(_translate("MainWindow", "Camera"))
        self.vidButton.setText(_translate("MainWindow", "Video"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))

    def exitdet(self):
        result = cv2.imread('261.jpeg')
        result = QtGui.QImage(result, result.shape[1],result.shape[0], result.shape[1] * 3,QtGui.QImage.Format_RGB888).rgbSwapped()
        self.display.setPixmap(QtGui.QPixmap(result))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Esc:
            self.test_method()

    def test_method(self):
        self.txt.setText("Esc key pressed")

    def imagedet(self):
        result = image.img()
        #cv2.imshow('Object detector', result)
        result = QtGui.QImage(result, result.shape[1],result.shape[0], result.shape[1] * 3,QtGui.QImage.Format_RGB888).rgbSwapped()
        #pix = QtGui.QPixmap(image)
        self.display.setPixmap(QtGui.QPixmap(result))
        self.txt.setText("Result key pressed")
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    def viddet(self):
        #video,sess,detection_boxes,detection_scores,detection_classes,num_detections,image_tensor,category_index = vidcode.vid()

        while(video.isOpened()):

            ret, frame = video.read()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_expanded = np.expand_dims(frame_rgb, axis=0)
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=0.60)

            cv2.imshow('Object detector', frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            #pix = QPixmap.fromImage(img)
            #pix = pix.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.display.setPixmap(QtGui.QPixmap(img))


            if cv2.waitKey(1) == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()


    def camdet(self):
        #video,sess,detection_boxes,detection_scores,detection_classes,num_detections,category_index = vidcode.vid()
        video = cv2.VideoCapture(0)
        ret = video.set(3,1280)
        ret = video.set(4,720)

        while(video.isOpened()):

            ret, frame = video.read()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_expanded = np.expand_dims(frame_rgb, axis=0)
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=0.60)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            #pix = QPixmap.fromImage(img)
            #pix = pix.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.display.setPixmap(QtGui.QPixmap(img))


            if cv2.waitKey(1) == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()










if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
