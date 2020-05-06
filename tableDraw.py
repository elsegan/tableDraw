
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
        self.guiCols = 4

        self.globalFont = QtGui.QFont('consolas',10)
        self.wStatement = QLabel('I\'ll tell you the number of cuts horizontal, vertical and their width')
        self.wStatement.setFont(self.globalFont)

        self.createGroupPanel()
        self.createGroupPieces()
        self.createGroupCalc()
        self.createGroupSaw()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.wStatement,0,0,4,self.guiCols)
        mainLayout.addWidget(self.gPanel,4,0,2,2)
        mainLayout.addWidget(self.gPieces,4,2,2,2)
        mainLayout.addWidget(self.gSaw,6,0,1,self.guiCols)
        mainLayout.addWidget(self.gCalc,7,0,1,self.guiCols)

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
        wText = QLabel('Piece Width  (mm) :')
        wText.setFont(self.globalFont)

        self.lEdit = QLineEdit(str(0))
        self.lEdit.setFont(self.globalFont)
        self.dEdit = QLineEdit(str(0))
        self.dEdit.setFont(self.globalFont)
        self.wEdit = QLineEdit(self.zEdit.text())
        self.wEdit.setFont(self.globalFont)
        self.wEdit.setReadOnly(True)

        panelLayout = QGridLayout()
        panelLayout.addWidget(lText,0,0)
        panelLayout.addWidget(self.lEdit,0,1)
        panelLayout.addWidget(dText,1,0)
        panelLayout.addWidget(self.dEdit,1,1)
        panelLayout.addWidget(wText,2,0)
        panelLayout.addWidget(self.wEdit,2,1)

        self.gPieces.setLayout(panelLayout)

    def createGroupSaw(self):
        self.gSaw = QGroupBox('Saw Parameters')
        self.gSaw.setFont(self.globalFont)

        wSaw = QLabel('Saw Width (mm) :')
        wSaw.setFont(self.globalFont)
        wDep = QLabel('Twiddle   (mm) :')
        wDep.setFont(self.globalFont)
        
        self.wSawEdit = QLineEdit(str(0))
        self.wSawEdit.setFont(self.globalFont)
        self.wDepEdit = QLineEdit(str(0))
        self.wDepEdit.setFont(self.globalFont)

        panelLayout = QGridLayout()

        panelLayout.addWidget(wSaw,0,0)
        panelLayout.addWidget(self.wSawEdit,0,1)
        panelLayout.addWidget(wDep,0,2)
        panelLayout.addWidget(self.wDepEdit,0,3)

        self.gSaw.setLayout(panelLayout)

    def createGroupCalc(self):
        self.gCalc = QGroupBox('Calculation Result')
        self.gCalc.setFont(self.globalFont)

        self.wNumCols = QLabel('Cuts X : 0')
        self.wNumCols.setFont(self.globalFont)
        self.wNumRows = QLabel('Cuts Y : 0')
        self.wNumRows.setFont(self.globalFont)
        self.wRotated = QLabel('No Rotation')
        self.wRotated.setFont(self.globalFont)
        self.wNumPieces = QLabel('Pieces : 0')
        self.wNumPieces.setFont(self.globalFont)
        self.wCalcButton = QPushButton('Calculate Result')
        self.wCalcButton.setFont(self.globalFont)
        self.wCalcButton.clicked.connect(lambda: self.eval())

        panelLayout = QGridLayout()

        panelLayout.addWidget(self.wNumCols,0,0)
        panelLayout.addWidget(self.wNumRows,0,1)
        panelLayout.addWidget(self.wRotated,0,2)
        panelLayout.addWidget(self.wNumPieces,0,3)
        panelLayout.addWidget(self.wCalcButton,1,0,1,self.guiCols)

        self.gCalc.setLayout(panelLayout)

    def eval(self):
        print('Calculate Result Button was Pressed')

if __name__ == "__main__":
    app = QApplication([])
    gui = mainWindow()
    gui.show()
    app.exec_()
