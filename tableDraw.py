
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QDateTime, Qt, QTimer,QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QComboBox,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QSizePolicy, QDialog, QTableWidget, QTextEdit,
                             QVBoxLayout, QWidget, QFileDialog, QTableWidgetItem)

print("No Problem ImportingLibraries --> Starting the tool -->")

class mainWindow(QDialog):
    def __init__(self,parent=None):
        super(mainWindow,self).__init__(parent)
        self.setFixedSize(1200,1200)
        self.setWindowTitle('tableDraw Tool')

        self.globalFont = QtGui.QFont('consolas',10)
        self.wStatement = QLabel('I\'ll tell you the number of cuts horizontal, vertical and their width')
        self.wStatement.setFont(self.globalFont)

        self.createGroupPanel()
        self.createGroupPieces()
        self.createGroupCalc()

        self.guiCols = 4
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.wStatement,0,0,4,self.guiCols)
        mainLayout.addWidget(self.gPanel,4,0,1,2)
        mainLayout.addWidget(self.gPieces,4,2,1,2)
        mainLayout.addWidget(self.gCalc,5,0,1,self.guiCols)

        self.setLayout(mainLayout)

    def createGroupPanel(self):
        self.gPanel = QGroupBox("Panel Dimensions")
        self.gPanel.setFont(self.globalFont)

        xText = QLabel('Panel X (mm) :')
        xText.setFont(self.globalFont)
        yText = QLabel('Panel Y (mm) :')
        yText.setFont(self.globalFont)
        zText = QLabel('Panel Z (mm) :')
        zText.setFont(self.globalFont)

        self.xEdit = QLineEdit(str(0))
        self.xEdit.setFont(self.globalFont)
        self.yEdit = QLineEdit(str(0))
        self.yEdit.setFont(self.globalFont)
        self.zEdit = QLineEdit(str(0))
        self.zEdit.setFont(self.globalFont)

        panelLayout = QGridLayout()
        panelLayout.addWidget(xText,0,0)
        panelLayout.addWidget(self.xEdit,0,1)
        panelLayout.addWidget(yText,1,0)
        panelLayout.addWidget(self.yEdit,1,1)
        panelLayout.addWidget(zText,2,0)
        panelLayout.addWidget(self.zEdit,2,1)

        self.gPanel.setLayout(panelLayout)

    def createGroupPieces(self):
        self.gPieces = QGroupBox("Piece Dimensions")
        self.gPieces.setFont(self.globalFont)

        lText = QLabel('Piece Length (mm) :')
        lText.setFont(self.globalFont)
        dText = QLabel('Piece Depth  (mm) :')
        dText.setFont(self.globalFont)
        wText = QLabel('Panel Width  (mm) :')
        wText.setFont(self.globalFont)

        self.lEdit = QLineEdit(str(0))
        self.lEdit.setFont(self.globalFont)
        self.dEdit = QLineEdit(str(0))
        self.dEdit.setFont(self.globalFont)
        self.wEdit = QLabel(self.zEdit.text())
        self.wEdit.setFont(self.globalFont)

        panelLayout = QGridLayout()
        panelLayout.addWidget(lText,0,0)
        panelLayout.addWidget(self.lEdit,0,1)
        panelLayout.addWidget(dText,1,0)
        panelLayout.addWidget(self.dEdit,1,1)
        panelLayout.addWidget(wText,2,0)
        panelLayout.addWidget(self.wEdit,2,1)

        self.gPieces.setLayout(panelLayout)

    def createGroupCalc(self):
        self.gCalc = QGroupBox('Calculation Result')
        self.gCalc.setFont(self.globalFont)

        self.numCols = QLabel('Cuts X : 0')
        self.numCols.setFont(self.globalFont)
        self.numRows = QLabel('Cuts Y : 0')
        self.numRows.setFont(self.globalFont)
        self.rotated = QLabel('No Rotation')
        self.rotated.setFont(self.globalFont)
        self.numPieces = QLabel('Pieces : 0')
        self.numPieces.setFont(self.globalFont)

        panelLayout = QGridLayout()

        panelLayout.addWidget(self.numCols,0,0)
        panelLayout.addWidget(self.numRows,0,1)
        panelLayout.addWidget(self.rotated,0,2)
        panelLayout.addWidget(self.numPieces,0,3)

        self.gCalc.setLayout(panelLayout)


if __name__ == "__main__":
    app = QApplication([])
    gui = mainWindow()
    gui.show()
    app.exec_()
