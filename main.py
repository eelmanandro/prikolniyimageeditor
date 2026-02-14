from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                              QHBoxLayout, QWidget, QListWidget, QLabel, QFileDialog)
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageFilter
app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('prikolniyimageeditor')

lb_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()
btn_left = QPushButton('Вліво')
btn_right = QPushButton('Вправо')
btn_flip = QPushButton('Дзеркало')
btn_sharp = QPushButton('Різкість')
btn_bw = QPushButton('Ч/Б')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

workDir = ''
def chooseWorkdir():
    global workDir
    dir = QFileDialog.getExistingDirectory()
    if dir:
        workDir = dir

def filter(files: list, extensions: list)-> list:
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFileNamesList():
    extensions = [ '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.svg' ]
    chooseWorkdir()
    if workDir:

        filenames = filter(os.listdir(workDir), extensions)
        lw_files.clear()
        for filename in filenames:
            lw_files.addItem(filename)

class ImageProcessor():
    def __init__ (self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modified/'
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def saveAndShowImage(self):
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    def toGrayscale(self):
        self.image = self.image.convert("L")
        self.saveAndShowImage()


workimage = ImageProcessor()
def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workDir, filename)
        image_path = os.path.join(workDir, filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)

btn_dir.clicked.connect(showFileNamesList)
btn_bw.clicked.connect(workimage.toGrayscale)



win.show()
app.exec_()
