#!/usr/bin/env python3

import logging
import signal
import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QWidget,
)


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
        pixmap_dst = QPixmap(pixmap_src.width(), pixmap_src.height())

        label_dst = ClickableLabel()
        label_src = ClickableLabel()

        label_dst.setStyleSheet("border: 1px solid black;")
        label_src.setStyleSheet("border: 1px solid black;")

        label_dst.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        label_src.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.layout().addWidget(label_dst)
        layout.layout().addWidget(label_src)

        label_dst.setPixmap(pixmap_dst)
        label_src.setPixmap(pixmap_src)

        label_dst.clicked.connect(self.on_lbl_dst_clicked)

        self.setGeometry(100, 100, 1100, 500)

    def get_pixmap(self, filename):
        pixmap = QPixmap(filename)
        return pixmap.scaled(
            min(pixmap.width(), 500), min(pixmap.height(), 500), Qt.KeepAspectRatio
        )

    def on_lbl_dst_clicked(self, *args):
        print(args)


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
