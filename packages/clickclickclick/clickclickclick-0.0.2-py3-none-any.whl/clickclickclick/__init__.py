#!/usr/bin/env python3

import logging
import signal
import sys

import numpy as np
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QWidget,
)
from scipy.interpolate import LinearNDInterpolator


class ClickableLabel(QLabel):
    clicked = pyqtSignal(int, int)

    def mousePressEvent(self, event):
        self.clicked.emit(event.pos().x(), event.pos().y())


class ClickPick(QMainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi(os.path.join(APP_DIR, 'picks.ui'), self)
        layout = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        pixmap_src = self.get_pixmap(sys.argv[1])
        self.pixmap_dst = QPixmap(pixmap_src.width(), pixmap_src.height())

        self.image = pixmap_src.toImage()
        self.pixels = []
        self.colors = []
        self.grids = np.mgrid[0 : self.pixmap_dst.width() : 1, 0 : self.pixmap_dst.height() : 1]

        self.label_dst = ClickableLabel()

        self.label_dst.setStyleSheet("border: 1px solid black;")

        self.label_dst.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.layout().addWidget(self.label_dst)

        self.label_dst.setPixmap(self.pixmap_dst)

        self.label_dst.clicked.connect(self.on_lbl_dst_clicked)

        if False:
            label_src = ClickableLabel()
            label_src.setStyleSheet("border: 1px solid black;")
            label_src.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label_src.setPixmap(pixmap_src)
            layout.layout().addWidget(label_src)
            self.setGeometry(100, 100, 1100, 500)
        else:

            self.setGeometry(100, 100, 600, 500)

    def get_pixmap(self, filename):
        return (pixmap := QPixmap(filename)).scaled(
            min(pixmap.width(), 500), min(pixmap.height(), 500), Qt.KeepAspectRatio
        )

    def on_lbl_dst_clicked(self, x, y):

        color = QColor(self.image.pixel(x, y))

        self.pixels.append((x, y))
        self.colors.append(color)

        painter = QPainter(self.pixmap_dst)
        if len(self.pixels) > 2:

            i_r = LinearNDInterpolator(self.pixels, [c.red() for c in self.colors], fill_value=0)
            i_g = LinearNDInterpolator(self.pixels, [c.green() for c in self.colors], fill_value=0)
            i_b = LinearNDInterpolator(self.pixels, [c.blue() for c in self.colors], fill_value=0)

            interpolated_r = i_r(*self.grids)
            interpolated_g = i_g(*self.grids)
            interpolated_b = i_b(*self.grids)

            painter.setBrush(Qt.NoBrush)
            for x in range(self.pixmap_dst.width()):
                for y in range(self.pixmap_dst.height()):
                    color = QColor(
                        int(interpolated_r[x, y]),
                        int(interpolated_g[x, y]),
                        int(interpolated_b[x, y]),
                    )
                    painter.setPen(color)
                    painter.drawPoint(x, y)
        else:
            painter.setPen(Qt.NoPen)
            for (x, y), color in zip(self.pixels, self.colors):
                painter.setBrush(color)
                painter.drawEllipse(x - 10, y - 10, 20, 20)

        painter.end()

        self.label_dst.setPixmap(self.pixmap_dst)

    def handle_signal(self, *args):
        raise SystemExit(0)


def main():
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)

    window = ClickPick()

    for s in (signal.SIGABRT, signal.SIGINT, signal.SIGSEGV, signal.SIGTERM):
        signal.signal(s, lambda signal, frame: window.handle_signal(signal))

    timer = QTimer()
    timer.start(200)
    timer.timeout.connect(lambda: None)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
