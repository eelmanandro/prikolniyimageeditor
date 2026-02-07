from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                              QHBoxLayout, QWidget, QListWidget, QLabel, QFileDialog)
import os
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

btn_dir.clicked.connect(showFileNamesList)




win.show()
app.exec_()
