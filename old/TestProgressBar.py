import sys
from PyQt5.QtCore    import pyqtProperty, QSize, Qt, QRectF, QTimer
from PyQt5.QtGui     import QColor, QPainter, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSlider, \
    QApplication


class PercentProgressBar(QWidget):
    MinValue    =   0
    MaxValue    = 100
    Value       =   0
    BorderWidth =   8
    Clockwise       = True   # �� ������� ������� ��� ������ ������� �������
    ShowPercent     = True   # ���������� �� �������
    ShowFreeArea    = False  # ���������� ������ ���������
    ShowSmallCircle = False  # �������� ��������� ���� � �������
    TextColor       = QColor(255, 255, 255)  # ���� ������
    BorderColor     = QColor(24, 189, 155)   # ���� ������������ �����
    BackgroundColor = QColor(70, 70, 70)     # ���� ����

    def __init__(self, *args, value=0, minValue=0, maxValue=100,
                 borderWidth=8, clockwise=True, showPercent=True,
                 showFreeArea=False, showSmallCircle=False,
                 textColor=QColor(255, 255, 255),
                 borderColor=QColor(24, 189, 155),
                 backgroundColor=QColor(70, 70, 70), **kwargs):
        super(PercentProgressBar, self).__init__(*args, **kwargs)
        
        self.Value    = value
        self.MinValue = minValue
        self.MaxValue = maxValue
        self.BorderWidth     = borderWidth
        self.Clockwise       = clockwise
        self.ShowPercent     = showPercent
        self.ShowFreeArea    = showFreeArea
        self.ShowSmallCircle = showSmallCircle
        self.TextColor       = textColor
        self.BorderColor     = borderColor
        self.BackgroundColor = backgroundColor

    def setRange(self, minValue: int, maxValue: int):
        if minValue >= maxValue:  
            return
        self.MinValue = minValue
        self.MaxValue = maxValue
        self.update()                

    def paintEvent(self, event):
        super(PercentProgressBar, self).paintEvent(event)
        width = self.width()
        height = self.height()
        side = min(width, height)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing)
        # ������������ ����� - ������� �����
        painter.translate(width / 2, height / 2)
        # 100x100 ���������������
        painter.scale(side / 100.0, side / 100.0)
        self._drawCircle(painter, 50)
        # ��������� ����
        self._drawArc(painter, 50 - self.BorderWidth / 2)
        # ����� 
        self._drawText(painter, 50)

    def _drawCircle(self, painter: QPainter, radius: int):
        radius = radius - self.BorderWidth
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.BackgroundColor)
        painter.drawEllipse(QRectF(-radius, -radius, radius * 2, radius * 2))
        painter.restore()                 

    def _drawArc(self, painter: QPainter, radius: int):
        # ��������� ����
        painter.save()
        painter.setBrush(Qt.NoBrush)
        # �������� �����
        pen = painter.pen()
        pen.setWidthF(self.BorderWidth)
        pen.setCapStyle(Qt.RoundCap)

        arcLength = 360.0 / (self.MaxValue - self.MinValue) * self.Value
        rect = QRectF(-radius, -radius, radius * 2, radius * 2)

        if not self.Clockwise:
            # ������ ������� �������
            arcLength = -arcLength

        # ��������� ���������� ���������
        if self.ShowFreeArea:
            acolor = self.BorderColor.toRgb()
            acolor.setAlphaF(0.2)
            pen.setColor(acolor)
            painter.setPen(pen)
            painter.drawArc(rect, (0 - arcLength) *
                            16, -(360 - arcLength) * 16)

        # ��������� ������� ���������
        pen.setColor(self.BorderColor)
        painter.setPen(pen)
        painter.drawArc(rect, 0, -arcLength * 16)

        # ��������� ��������� ���� ����� ����� ���������
        if self.ShowSmallCircle:
            offset = radius - self.BorderWidth + 1
            radius = self.BorderWidth / 2 - 1
            painter.rotate(-90)
            circleRect = QRectF(-radius, radius + offset,
                                radius * 2, radius * 2)
            painter.rotate(arcLength)
            painter.drawEllipse(circleRect)

        painter.restore()

    def _drawText(self, painter: QPainter, radius: int):
        painter.save()
        painter.setPen(self.TextColor)
        painter.setFont(QFont('Arial', 25))
        strValue = '{}%'.format(int(self.Value / (self.MaxValue - self.MinValue)
                                    * 100)) if self.ShowPercent else str(self.Value)
        painter.drawText(QRectF(-radius, -radius, radius * 2,
                                radius * 2), Qt.AlignCenter, strValue)
        painter.restore()

    @pyqtProperty(int)             
    def minValue(self) -> int:             
        return self.MinValue       

    @minValue.setter                    
    def minValue(self, minValue: int):
        if self.MinValue != minValue:
            self.MinValue = minValue
            self.update()
            
    @pyqtProperty(int)
    def maxValue(self) -> int:
        return self.MaxValue

    @maxValue.setter
    def maxValue(self, maxValue: int):
        if self.MaxValue != maxValue:
            self.MaxValue = maxValue
            self.update()

    @pyqtProperty(int)
    def value(self) -> int:
        return self.Value

    @value.setter
    def value(self, value: int):
        if self.Value != value:
            self.Value = value
            self.update()

    @pyqtProperty(float)
    def borderWidth(self) -> float:
        return self.BorderWidth

    @borderWidth.setter
    def borderWidth(self, borderWidth: float):
        if self.BorderWidth != borderWidth:
            self.BorderWidth = borderWidth
            self.update()

    @pyqtProperty(bool)
    def clockwise(self) -> bool:
        return self.Clockwise

    @clockwise.setter
    def clockwise(self, clockwise: bool):
        if self.Clockwise != clockwise:
            self.Clockwise = clockwise
            self.update()

    @pyqtProperty(bool)
    def showPercent(self) -> bool:
        return self.ShowPercent

    @showPercent.setter
    def showPercent(self, showPercent: bool):
        if self.ShowPercent != showPercent:
            self.ShowPercent = showPercent
            self.update()

    @pyqtProperty(bool)
    def showFreeArea(self) -> bool:
        return self.ShowFreeArea

    @showFreeArea.setter
    def showFreeArea(self, showFreeArea: bool):
        if self.ShowFreeArea != showFreeArea:
            self.ShowFreeArea = showFreeArea
            self.update()

    @pyqtProperty(bool)
    def showSmallCircle(self) -> bool:
        return self.ShowSmallCircle

    @showSmallCircle.setter
    def showSmallCircle(self, showSmallCircle: bool):
        if self.ShowSmallCircle != showSmallCircle:
            self.ShowSmallCircle = showSmallCircle
            self.update()

    @pyqtProperty(QColor)
    def textColor(self) -> QColor:
        return self.TextColor

    @textColor.setter
    def textColor(self, textColor: QColor):
        if self.TextColor != textColor:
            self.TextColor = textColor
            self.update()

    @pyqtProperty(QColor)
    def borderColor(self) -> QColor:
        return self.BorderColor

    @borderColor.setter
    def borderColor(self, borderColor: QColor):
        if self.BorderColor != borderColor:
            self.BorderColor = borderColor
            self.update()

    @pyqtProperty(QColor)
    def backgroundColor(self) -> QColor:
        return self.BackgroundColor

    @backgroundColor.setter
    def backgroundColor(self, backgroundColor: QColor):
        if self.BackgroundColor != backgroundColor:
            self.BackgroundColor = backgroundColor
            self.update()

    def setValue(self, value):
        self.value = value

    def sizeHint(self) -> QSize:
        return QSize(100, 100)

 
class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        
        layout = QHBoxLayout(self)
        self._value   = 0
        self._widgets = []
        self._timer   = QTimer(self, timeout=self.updateValue)

        self._widgets.append(PercentProgressBar(self))
        layout.addWidget(self._widgets[0])

        self._widgets.append(PercentProgressBar(self, clockwise=False))
        layout.addWidget(self._widgets[1])

        self._widgets.append(PercentProgressBar(self, showPercent=False))
        layout.addWidget(self._widgets[2])

        self._widgets.append(PercentProgressBar(self, showFreeArea=True))
        layout.addWidget(self._widgets[3])

        self._widgets.append(PercentProgressBar(self, showSmallCircle=True))
        layout.addWidget(self._widgets[4])

        self._widgets.append(PercentProgressBar(self, styleSheet="""
            qproperty-textColor: rgb(255, 0, 0);
            qproperty-borderColor: rgb(0, 255, 0);
            qproperty-backgroundColor: rgb(0, 0, 255);
        """))
        layout.addWidget(self._widgets[5])

        rWidget = QWidget(self)
        layout.addWidget(rWidget)
        
        vlayout = QVBoxLayout(rWidget)
        self.staticPercentProgressBar = PercentProgressBar(self)
        self.staticPercentProgressBar.showFreeArea = True
        self.staticPercentProgressBar.ShowSmallCircle = True
        vlayout.addWidget(self.staticPercentProgressBar)
        vlayout.addWidget(QSlider(self, minimum=0, maximum=100, 
                                  orientation=Qt.Horizontal,
                                  valueChanged=self.staticPercentProgressBar.setValue))
        self._timer.start(100)

    def updateValue(self):
        for w in self._widgets:
            w.value = self._value
        self._value += 1
        if self._value > 100:
            self._value = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
