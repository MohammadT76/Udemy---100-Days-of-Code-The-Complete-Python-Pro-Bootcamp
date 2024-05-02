import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

##
# MAIN WINDOW LAYOUT
##
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.view = View(self)

        # Button to clear both image and drawing
        self.button = QPushButton('Clear Drawing', self)            
        self.button.clicked.connect(self.handleClearView)

        # 'Load image' button
        self.btnLoad = QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)

        # Save
        self.btnSave = QToolButton(self)
        self.btnSave.setText('Save image')
        self.btnSave.clicked.connect(self.file_save)

        # Save as
        self.btnSaveAs = QToolButton(self)
        self.btnSaveAs.setText('Save as...')
        self.btnSaveAs.clicked.connect(self.file_save_as)

        # Arrange Layout
        self.layout = QVBoxLayout(self)                         
        self.layout.addWidget(self.view)        # Drawing
        self.layout.addWidget(self.button)      # Clear view
        self.layout.addWidget(self.btnLoad)     # Load photo
        self.layout.addWidget(self.btnSave)     # Save
        self.layout.addWidget(self.btnSaveAs)   # Save as...


        self.setGeometry(0, 25, 1365, 700)
        self.setWindowTitle('Processed Slices')
        self.show()

    def file_save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        cv2.imwrite(filename + '.png', self.view.cvImage)

    def file_save(self):
        cv2.imwrite(self.view._filename, self.view.cvImage)

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.view._filename = fileName

    def loadImage(self):
        self.view._empty = False
        # Load Image to pixmap
        self.openFileNameDialog()
        self.view.cvImage = cv2.imread(self.view._filename)
        self.view.height, self.view.width , self.view.bytesPerComponent= self.view.cvImage.shape
        self.view.bytesPerLine = self.view.bytesPerComponent * self.view.width
        cv2.cvtColor(self.view.cvImage, cv2.COLOR_BGR2RGB, self.view.cvImage)
        self.view.mQImage = QImage(self.view.cvImage.data, self.view.width, self.view.height, self.view.bytesPerLine, QImage.Format_RGB888)        
        self.pixmap = QPixmap(self.view.mQImage) 

        # Include pixmap on the drawing scene
        self.view.setScene(QGraphicsScene(self))
        self.view.setSceneRect(QRectF(0,0,self.view.width, self.view.height))   # Scene has same dimension as image so that we can map the segmented area to the cv2 image
        self.view.scene().addPixmap(self.pixmap)
        self.view.fitInView()

    def handleClearView(self):
        self.view.scene().clear()
        self.view.scene().addPixmap(self.pixmap)
        self.view.contour = []
        self.view.fitInView()



##
# DRAWING AND ZOOMING
##
class View(QGraphicsView):
    def __init__(self, parent):

        super().__init__()

        # Attributes
        self._zoom = 0
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self._filename = ""
        # Resettings for Zooming
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)

        self.contour = []                   # Contains points of the contour for cv2 drawing
        self.first = QPointF(0,0)
        self.ii = 0

    """ PAINTING """
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start = event.pos()                                                                               # Get point where we pressed
            self.contour.append(QPointF(self.mapToScene(self._start)))              
            if self.first == QPointF(0,0):                                                           # If it is the first we press, save the point which will be used to close 
                                                                                                     # the shape whenever the right button is pressed
                self.first = QPointF(self.mapToScene(self._start))
                self.ii = 0
            else:                                                                                   # If it is not the first point draw a line joining the point we previously 
                                                                                                    # pressed and the one we have just clicked
                self.scene().addItem(QGraphicsLineItem(QLineF(self.contour[self.ii+1], self.contour[self.ii]))) 
                self.ii += 1


    def mouseReleaseEvent(self, event):
        # RIGHT BUTTON
        if event.button() == Qt.RightButton:
            self.scene().addItem(QGraphicsLineItem(QLineF(self.contour[-1], self.first)))  # close contour
            self.first = QPointF(0,0)
            self.contour.append((self.contour[0]))

            #Drawing CV_IMAGE
            for i in range(len(self.contour) - 1):
                A = ( int( self.contour[i].x() ), int( self.contour[i].y() ) )
                B = ( int( self.contour[i+1].x() ), int( self.contour[i+1].y() ))
                cv2.line(self.cvImage, A, B, (0,0,255), 2)
            cv2.imshow('drawed slice', self.cvImage)
            cv2.waitKey()


    """ ZOOMING """
    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QRectF(0, 0, self.width, self.height)
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:              # event.angleDelta() returns the distance that the wheel is rotated, in eighths of a degree.
                factor = 1.25                           # Zooming in
                self._zoom += 1
            else:
                factor = 0.8                            # Zooming out
                self._zoom -= 1

            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:                                       # Cannot zoom out from the original size
                self._zoom = 0


##
# RUN PROGRAM
##
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_()) 