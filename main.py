from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                              QHBoxLayout, QWidget, QListWidget, QLabel, QFileDialog)
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageFilter
app = QApplication([])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__( )
        self.resize(700, 500)
        self.setWindowTitle('prikolniyimageeditor')
        self.work_dir = ""
        self.setupUi()
    def setupUi(self):
        self.lb_image = QLabel('Картинка')
        self.btn_dir = QPushButton('Папка')
        self.lw_files = QListWidget()
        self.btn_left = QPushButton('Вліво')
        self.btn_right = QPushButton('Вправо')
        self.btn_flip = QPushButton('Дзеркало')
        self.btn_sharp = QPushButton('Різкість')
        self.btn_bw = QPushButton('Ч/Б')

        self.row = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        self.col1.addWidget(self.btn_dir)
        self.col1.addWidget(self.lw_files)
        self.col2.addWidget(self.lb_image, 95)
        self.row_tools = QHBoxLayout()
        self.row_tools.addWidget(self.btn_left)
        self.row_tools.addWidget(self.btn_right)
        self.row_tools.addWidget(self.btn_flip)
        self.row_tools.addWidget(self.btn_sharp)
        self.row_tools.addWidget(self.btn_bw)
        self.col2.addLayout(self.row_tools)
        self.row.addLayout(self.col2, 80)
        self.row.addLayout(self.col1, 20)
        self.setLayout(self.row)

    def chooseWorkdir(self):
        dir = QFileDialog.getExistingDirectory()
        if dir:
            self.work_dir = dir

    def filter(self, files: list, extensions: list)-> list:
        result = []
        for filename in files:
            for ext in extensions:
                if filename.endswith(ext):
                    result.append(filename)
        return result

    def showFileNamesList(self):
        extensions = [ '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.svg' ]
        self.chooseWorkdir()
        if self.work_dir:

            filenames = filter(os.listdir(self.work_dir), extensions)
            self.lw_files.clear()
            for filename in filenames:
                self.lw_files.addItem(filename)

class ImageProcessor():
    def __init__ (self, window: MainWindow):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modified/'
        self.window = window
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        self.window.lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = self.window.lb_image.width(), self.window.lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        self.window.lb_image.setPixmap(pixmapimage)
        self.window.lb_image.show()
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

win = MainWindow()
workimage = ImageProcessor(win)
def showChosenImage():
    if win.lw_files.currentRow() >= 0:
        filename = win.lw_files.currentItem().text()
        workimage.loadImage(win.work_dir, filename)
        image_path = os.path.join(win.work_dir, filename)
        workimage.showImage(image_path)

win.lw_files.currentRowChanged.connect(showChosenImage)

win.btn_dir.clicked.connect(win.showFileNamesList)
win.btn_bw.clicked.connect(workimage.toGrayscale)



win.show()
app.exec_()
