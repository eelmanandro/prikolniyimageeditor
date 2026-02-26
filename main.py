from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                              QHBoxLayout, QWidget, QListWidget, QLabel, QFileDialog)
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageFilter
app = QApplication([])


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
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        return image_path
    # def saveAndShowImage(self):
    #     self.saveImage()
    #     image_path = os.path.join(self.dir, self.save_dir, self.filename)
    #     self.showImage(image_path)
    def toGrayscale(self):
        self.image = self.image.convert("L")
        image_path = self.saveImage()
        return image_path


class MainWindow(QMainWindow):
    def __init__(self, workimage: ImageProcessor):
        super().__init__()
        self.resize(700, 500)
        self.setWindowTitle('prikolniyimageeditor')
        self.work_dir = ""
        self.current_image_path = ""
        self.workimage = workimage
        self._last_shown_image_path = None
        self.setupUi()
        self.setupWindowEvents()
    
    def setupUi(self):
        self.lb_image = QLabel('Картинка')
        # Встановлення мінімального розміру, щоб уникнути проблеми зі зменшенням зображення
        self.lb_image.setMinimumSize(1, 1)
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
        self.row.addLayout(self.col1, 20)
        self.row.addLayout(self.col2, 80)
        central_widget = QWidget()
        central_widget.setLayout(self.row)
        self.setCentralWidget(central_widget)

    def setupWindowEvents(self):
        self.lw_files.currentRowChanged.connect(self.showChosenImage)

        self.btn_dir.clicked.connect(self.showFileNamesList)
        self.btn_bw.clicked.connect(self.toGrayscaleImage)

    def chooseWorkdir(self):
        dir = QFileDialog.getExistingDirectory()
        if dir:
            self.work_dir = dir

    def filter_files(self, files: list, extensions: list)-> list:
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

            filenames = self.filter_files(os.listdir(self.work_dir), extensions)
            self.lw_files.clear()
            for filename in filenames:
                self.lw_files.addItem(filename)


    def showImage(self, path):
        self._last_shown_image_path = path
        self.lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = self.lb_image.width(), self.lb_image.height()
        if w == 0 or h == 0:
            w, h = 700, 500
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lb_image.setPixmap(pixmapimage)
        self.lb_image.show()

    def resizeEvent(self, event):
        """Обробка події зміни розміру вікна"""
        super().resizeEvent(event)
        if self._last_shown_image_path:
            self.showImage(self._last_shown_image_path)

    def showChosenImage(self):
        if self.lw_files.currentRow() >= 0:
            filename = self.lw_files.currentItem().text()
            self.workimage.loadImage(self.work_dir, filename)
            self.current_image_path = os.path.join(self.work_dir, filename)
            self.showImage(self.current_image_path)

    def toGrayscaleImage(self):
        self.current_image_path = workimage.toGrayscale()
        self.showImage(self.current_image_path)


if __name__ == "__main__":
    workimage = ImageProcessor()
    win = MainWindow(workimage)

    win.show()
    app.exec_()
