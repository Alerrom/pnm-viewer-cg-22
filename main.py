import sys

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QComboBox
from matplotlib import pyplot as plt

import pnm as p


class ImageConverter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.img = p.pnmImage()
        self.layout = QtWidgets.QGridLayout(self)

        openBtn = QtWidgets.QPushButton('Open')
        self.layout.addWidget(openBtn, 1, 0)
        openBtn.clicked.connect(self.openFile)

        self.saveBtn = QtWidgets.QPushButton('Save')
        self.layout.addWidget(self.saveBtn, 2, 0)
        self.saveBtn.clicked.connect(self.saveFile)
        self.saveBtn.setEnabled(False)

        self.original = QtWidgets.QLabel()
        self.layout.addWidget(self.original, 4, 0, 1, 2)
        self.original.adjustSize()


    def openFile(self):
        path, filter = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select image', '')
        message = self.img.open(path, self.nameSpace)

        if self.nameSpace == "RGB":
            pixmap = QPixmap(path)
        else:
            self.img.save("buffer\subbuffer.pnm", self.img.bufferRGB, 1)
            pixmap = QPixmap("buffer\subbuffer.pnm")

        if (not pixmap.isNull()) and message == "Success":
            self.original.setPixmap(pixmap)
            self.saveBtn.setEnabled(True)
            self.combo.setEnabled(True)
            self.activated = True
        if message != "Success":
            QMessageBox.about(self, "Exception", message)
        if pixmap.isNull():
            QMessageBox.about(self, "Exception", "The File is damaged")

    def saveFile(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select path save', '')
        text, ok = QtWidgets.QInputDialog.getText(self, 'File Name', 'Enter file name:')
        if ok:
            if self.canal != "All":
                self.img.save(path + "/" + text + ".pnm", self.img.colorChannel, 0)
            elif self.nameSpace == "RGB":
                self.img.save(path + "/" + text + ".pnm", self.img.bufferRGB, 1)
            else:
                self.img.save(path + "/" + text + ".pnm", self.img.colorModel, 1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageConverter()
    window.show()
    sys.exit(app.exec())
                                                
