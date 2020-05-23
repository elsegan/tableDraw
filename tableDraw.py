import matplotlib.pyplot as plt
import numpy as np
import cv2

from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import QDateTime, Qt, QTimer,QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox, QComboBox,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QSizePolicy, QDialog, QTableWidget, QTextEdit,
                             QVBoxLayout, QWidget, QFileDialog, QTableWidgetItem)

print("No Problem ImportingLibraries --> Starting the tool -->")

class mainWindow(QDialog):
    def __init__(self,parent=None):
        super(mainWindow,self).__init__(parent)
        scale = 1.4
        self.setFixedSize(1400 * scale,1000 * scale)
        self.setWindowTitle('tableDraw Tool')
        self.guiCols = 4

        self.globalFont = QtGui.QFont('consolas',10)
        self.wStatement = QLabel('I\'ll tell you the number of cuts horizontal, vertical and their width\n \n \n \n ')
        self.wStatement.setFont(self.globalFont)

        self.createGroupPanel()
        self.createGroupPieces()
        self.createGroupCalc()
        self.createGroupSaw()

        # Create image window
        self.wImg = QLabel()

        self.eval()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.wImg,0,0,5,self.guiCols,QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.wStatement,5,0,1,self.guiCols,QtCore.Qt.AlignCenter)
        mainLayout.addWidget(self.gPanel,6,0,2,2)
        mainLayout.addWidget(self.gPieces,6,2,2,2)
        mainLayout.addWidget(self.gSaw,8,0,1,self.guiCols)
        mainLayout.addWidget(self.gCalc,9,0,1,self.guiCols)

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
            self.vizualise()
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
        self.dataOK &= self.testInt(self.depEdit,True)

        # Check conformity of dimensions
        if ((int(self.xEdit.text())) >= int(self.lEdit.text())):
            if ((int(self.yEdit.text())) >= int(self.dEdit.text())):
                self.dataOK &= True
            else:
                self.dataOK &= False
        elif ((int(self.xEdit.text())) >= int(self.dEdit.text())):
            if ((int(self.yEdit.text())) >= int(self.lEdit.text())):
                self.dataOK &= True
            else:
                self.dataOK &= False
        else:
            self.dataOK &= False

    def testInt(self, lineEditWidget,okZero=False):
        # Check that the input can be cast to an int
        # If is can, make it positive, otherwise make it 0
        try:
            deadVar = int(lineEditWidget.text())
            if (deadVar < 0):
                lineEditWidget.setText(str(-deadVar))
            return (deadVar != 0) or (okZero)
        except:
            lineEditWidget.setText(str(0))
            return False

    def calc(self):
        # Preallocate some values so its easier to read
        sawWidth = int(self.sawEdit.text())
        twiddle  = int(self.depEdit.text())
        inputX   = int(self.xEdit.text())
        inputY   = int(self.yEdit.text())

        maxArea  = inputX * inputY # in mm^2
        self.orientation = -1

        tempLength = float(int(self.lEdit.text()) + sawWidth)
        tempDepth  = float(int(self.dEdit.text()) + sawWidth + twiddle)

        rows   = []
        cols   = []
        pieces = []

        # Get the number of non-rotated cuts
        if (inputX >= int(self.lEdit.text())) and (inputY >= int(self.dEdit.text())):
            outX0 = inputX - int(self.lEdit.text())
            outY0 = inputY - int(self.dEdit.text())
            rows.append(1)
            cols.append(1)

            cols[0] += int(outX0 / tempLength)
            rows[0] += int(outY0 / tempDepth)
        else:
            cols.append(0)
            rows.append(0)

        # Get the number of rotated cuts
        if (inputX >= int(self.dEdit.text())) and (inputY >= int(self.lEdit.text())):
            outX1 = inputX - int(self.dEdit.text())
            outY1 = inputY - int(self.lEdit.text())
            rows.append(1)
            cols.append(1)

            cols[1] += int(outX1 / tempDepth)
            rows[1] += int(outY1 / tempLength)
        else:
            cols.append(0)
            rows.append(0)

        # Calculate the number of pieces made
        pieces.append(rows[0] * cols[0])
        pieces.append(rows[1] * cols[1])

        if (pieces[0] >= pieces[1]):
            self.orientation = 0
        elif(pieces[1] > 0):
            self.orientation = 1

        warnArea = False
        if (self.orientation == -1):
            self.wStatement.setText('There was something wrong with the dimensions\n'
                                    + 'It can\'t possibly exist\n \n \n ')
            
        else:
            usedArea = (pieces[self.orientation]
                       * int(self.lEdit.text())
                       * int(self.dEdit.text())) # mm^2

            sawnArea = (pieces[self.orientation]
                        * (  tempLength
                           + tempDepth
                           - sawWidth)
                        * sawWidth)

            wasteArea = maxArea - usedArea # mm^2

            tableArea  = (pieces[self.orientation]
                         * int(self.wEdit.text())
                         * int(self.lEdit.text())
                         * 1e-6)

            if (cols[self.orientation] == 1) and (rows[self.orientation] != 1):
                sawnArea = pieces[self.orientation] * (tempLength - sawWidth) * sawWidth
            elif (cols[self.orientation] != 1) and (rows[self.orientation] == 1):
                sawnArea = pieces[self.orientation] * (tempDepth - sawWidth) * sawWidth
            elif (cols[self.orientation] == 1) and (rows[self.orientation] == 1):
                sawnArea = 0
                print('The amount of sawn waste is too complex to be useful')
                print('So I didn\'t calculate it')

            wasteArea = max(wasteArea, 0)
            sawnArea  = max(sawnArea,0)

            try:
                assert(usedArea  <= maxArea)
                assert(wasteArea <= maxArea)
                assert(sawnArea  <= maxArea)
            except AssertionError:
                print('There was something erroneous about the areas calculated\n'
                      + 'The maxArea was    : ' + str(maxArea) + ' (mm^2)\n'
                      + 'The usedArea was   : ' + str(usedArea) + ' (mm^2)\n'
                      + 'The wasteArea was  : ' + str(wasteArea) + ' (mm^2)\n'
                      + 'The sawnArea was   : ' + str(sawnArea) + ' (mm^2)')

            self.wNumPieces.setText('Pieces : ' + str(pieces[self.orientation]))
            self.wRotated.setText('Rotation : ' + str(self.orientation))
            self.wNumCols.setText('Cuts X : ' + str(rows[self.orientation]))
            self.wNumRows.setText('Cuts Y : ' + str(cols[self.orientation]))
            self.wStatement.setText('Wow, you actually gave good dimensions \^.^/'
                                    + '\nThe wastage is   : ' + str((wasteArea * 100 / maxArea)) + ' %'
                                    + '\nBut sawn area is : ' + str((sawnArea * 100 / maxArea)) + ' %'
                                    + '\nSo real waste is : ' + str((wasteArea - sawnArea) * 100 / maxArea) + ' %'
                                    + '\nThe coverable area is : ' + str(tableArea) + ' m^2')

    def vizualise(self):
        pCols = int(self.xEdit.text())
        pRows = int(self.yEdit.text())
        sawWidth = int(self.sawEdit.text())
        twiddle  = int(self.depEdit.text())

        if (self.orientation == 0):
            cutX = int(self.lEdit.text()) + sawWidth
            cutY = int(self.dEdit.text()) + sawWidth + twiddle
            widX = sawWidth
            widY = sawWidth + twiddle
        elif (self.orientation == 1):
            cutX = int(self.dEdit.text()) + sawWidth + twiddle
            cutY = int(self.lEdit.text()) + sawWidth
            widX = sawWidth + twiddle
            widY = sawWidth
        else:
            return -1

        canvas = np.ones((pRows,pCols,3))

        imgDim = 3

        # Make marks on the columns
        cCols = cutX
        fullCol = np.zeros((pRows,1,imgDim))
        while (cCols <= pCols):
            for i in range(widX):
                try:
                    canvas[:,cCols - i,:] = fullCol[:,0,:]
                except:
                    continue

            cCols += cutX

        # Make marks on the columns
        cRows = cutY
        fullRow = np.zeros((1,pCols,imgDim))
        while (cRows <= pRows):
            for i in range(widY):
                try:
                    canvas[cRows - i,:,:] = fullRow[0,:,:]
                except:
                    continue

            cRows += cutY

        # Mark off the waste area of true wastage
        cCols -= cutX
        cRows -= cutY
        gCols  = np.ones((pRows,1,imgDim)) * 0.5
        gColor = np.array([[185/255.0, 185/255.0, 240/255.0]])
        gRows  = np.ones((1,pCols,imgDim)) * 0.5

        tCols = np.copy(gCols)
        for i in range(pRows):
            gCols[i] = gColor

        for i in range(pCols):
            gRows[:,i] = gColor

        if cCols > 0:
            for cols in range(cCols,pCols):
                try:
                    canvas[:,cols,:] = gCols[:,0,:]
                except:
                    continue
        
        if cRows > 0:
            for rows in range(cRows,pRows):
                try:
                    canvas[rows,:,:] = gRows[0,:,:]
                except:
                    continue

        canvas = canvas[:int(self.yEdit.text()),:int(self.xEdit.text()),:]
        dummyName = 'tempResultant.png'
        cv2.imwrite(dummyName,canvas * 255)
        canvas = cv2.imread(dummyName)

        canvas = self.imageUnskew(canvas)
        
        # Perform image scaling
        maxRows    = 700
        scale      = maxRows / pRows
        scaledRows = maxRows
        scaledCols = int(scale * pCols)

        canvas = cv2.resize(canvas,(scaledCols,scaledRows))
        bpl = imgDim * scaledCols
        
        qImg = QtGui.QImage(canvas,canvas.shape[1],canvas.shape[0],bpl,QtGui.QImage.Format_RGB888).rgbSwapped()
        pMap = QtGui.QPixmap.fromImage(qImg)
        self.wImg.setPixmap(pMap)

    def imageUnskew(self,npArray):
        return npArray

if __name__ == "__main__":
    app = QApplication([])
    gui = mainWindow()
    gui.show()
    app.exec_()
