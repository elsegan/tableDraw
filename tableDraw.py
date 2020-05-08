
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
        self.wStatement = QLabel('I\'ll tell you the number of cuts horizontal, vertical and their width\n \n \n \n ')
        self.wStatement.setFont(self.globalFont)

        self.createGroupPanel()
        self.createGroupPieces()
        self.createGroupCalc()
        self.createGroupSaw()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.wStatement,0,0,1,self.guiCols)
        mainLayout.addWidget(self.gPanel,1,0,2,2)
        mainLayout.addWidget(self.gPieces,1,2,2,2)
        mainLayout.addWidget(self.gSaw,3,0,1,self.guiCols)
        mainLayout.addWidget(self.gCalc,4,0,1,self.guiCols)

        self.setLayout(mainLayout)
        self.calc()

    def createGroupPanel(self):
        self.gPanel = QGroupBox("Panel Dimensions")
        self.gPanel.setFont(self.globalFont)

        xText = QLabel('Panel X (mm) :')
        xText.setFont(self.globalFont)
        yText = QLabel('Panel Y (mm) :')
        yText.setFont(self.globalFont)
        zText = QLabel('Panel Z (mm) :')
        zText.setFont(self.globalFont)

        self.xEdit = QLineEdit(str(2400))
        self.xEdit.setFont(self.globalFont)
        self.yEdit = QLineEdit(str(1200))
        self.yEdit.setFont(self.globalFont)
        self.zEdit = QLineEdit(str(18))
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

        self.lEdit = QLineEdit(str(60))
        self.lEdit.setFont(self.globalFont)
        self.dEdit = QLineEdit(str(30))
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

        saw = QLabel('Saw Width (mm) :')
        saw.setFont(self.globalFont)
        dep = QLabel('Twiddle   (mm) :')
        dep.setFont(self.globalFont)
        
        self.sawEdit = QLineEdit(str(3))
        self.sawEdit.setFont(self.globalFont)
        self.depEdit = QLineEdit(str(1))
        self.depEdit.setFont(self.globalFont)

        panelLayout = QGridLayout()

        panelLayout.addWidget(saw,0,0)
        panelLayout.addWidget(self.sawEdit,0,1)
        panelLayout.addWidget(dep,0,2)
        panelLayout.addWidget(self.depEdit,0,3)

        self.gSaw.setLayout(panelLayout)

    def createGroupCalc(self):
        self.gCalc = QGroupBox('Calculation Result')
        self.gCalc.setFont(self.globalFont)

        self.wNumCols = QLabel('Cuts X : 0')
        self.wNumCols.setFont(self.globalFont)
        self.wNumRows = QLabel('Cuts Y : 0')
        self.wNumRows.setFont(self.globalFont)
        self.wRotated = QLabel('Rotation : 0')
        self.wRotated.setFont(self.globalFont)
        self.wNumPieces = QLabel('Pieces : 0')
        self.wNumPieces.setFont(self.globalFont)
        self.wCalcButton = QPushButton('Calculate Number of Pieces')
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
        self.checkData()

        if (self.dataOK):
            self.calc()
        else:
            self.wStatement.setText('There was something wrong with your dimensions\n'
                                    + 'It can\'t possibly exist!\n \n \n ')

    def checkData(self):
        self.dataOK = True

        # Check the Panel data
        self.dataOK &= self.testInt(self.xEdit)
        self.dataOK &= self.testInt(self.yEdit)
        self.dataOK &= self.testInt(self.zEdit)

        # Force the z data and Width data to be aligned
        self.wEdit.setText(self.zEdit.text())
        
        # Check the Piece data
        self.dataOK &= self.testInt(self.lEdit)
        self.dataOK &= self.testInt(self.dEdit)
        self.dataOK &= self.testInt(self.wEdit)

        # Check the Saw data
        self.dataOK &= self.testInt(self.sawEdit)
        self.dataOK &= self.testInt(self.depEdit)

    def testInt(self, lineEditWidget):
        # Check that the input can be cast to an int
        # If is can, make it positive, otherwise make it 0
        try:
            deadVar = int(lineEditWidget.text())
            if (deadVar < 0):
                lineEditWidget.setText(str(-deadVar))
            return (deadVar != 0)
        except:
            lineEditWidget.setText(str(0))
            return False

    def calc(self):
        # Preallocate/precalc some values of the dimensions
        sawWidth = int(self.sawEdit.text())
        twiddle  = int(self.depEdit.text())
        tempX    = int(self.xEdit.text()) + sawWidth
        tempY    = int(self.yEdit.text()) + sawWidth

        maxArea = int(self.xEdit.text()) * int(self.yEdit.text())

        self.orientation = -1

        tempPieceLength = int(self.lEdit.text()) + sawWidth
        tempPieceDepth  = int(self.dEdit.text()) + twiddle

        rows   = []
        cols   = []
        pieces = []

        # Get non-rotated cuts
        rows.append(int((tempY + twiddle) / tempPieceDepth))
        cols.append(int(tempX / tempPieceLength))

        # Get rotated cuts
        rows.append(int((tempX + twiddle) / tempPieceDepth))
        cols.append(int(tempY / tempPieceLength))

        # Calc Pieces
        pieces.append(rows[0] * cols [0])
        pieces.append(rows[1] * cols [1])

        if ( pieces[0] > pieces[1] ):
            self.orientation = 0
        elif ( pieces[1] > 0 ):
            self.orientation = 1

        usedArea   = pieces[self.orientation] * int(self.lEdit.text()) * int(self.dEdit.text())
        wasteArea  = (maxArea - usedArea) # mm^2
        wastage    = wasteArea / (maxArea / 100.0)
        wasteArea *= 1e-6 # m^2
        tableArea  = pieces[self.orientation] * int(self.lEdit.text()) * int(self.wEdit.text()) * 1e-6

        cutWasteX  = sawWidth * cols[self.orientation]
        cutWasteY  = sawWidth * rows[self.orientation]
        remX       = int(self.xEdit.text()) - cutWasteX
        remY       = int(self.yEdit.text()) - cutWasteY
        remArea    = remX * remY
        sawArea   = (maxArea - remArea) / (maxArea / 100)

        if ( self.orientation == -1 ):
            self.wStatement.setText('There was something wrong with the dimensions\n'
                                    + 'It can\'t possibly exist\n \n \n ')
        else:
            self.wNumPieces.setText('Pieces : ' + str(pieces[self.orientation]))
            self.wRotated.setText('Rotation : ' + str(self.orientation))
            self.wNumCols.setText('Cuts X : ' + str(rows[self.orientation]))
            self.wNumRows.setText('Cuts Y : ' + str(cols[self.orientation]))
            self.wStatement.setText('Wow, you actually gave good dimensions \^.^/'
                                    + '\nThe wastage is : ' + str(wastage) + ' %'
                                    + '\nBut saw area is :' + str(sawArea) + (' %')
                                    + '\nThe coverable area is : ' + str(tableArea) + ' m^2\n ')

if __name__ == "__main__":
    app = QApplication([])
    gui = mainWindow()
    gui.show()
    app.exec_()
