import sys
from PySide6 import QtWidgets, QtWebEngineWidgets


def create_pdf(html, file_name):
    app = QtWidgets.QApplication(sys.argv)
    loader = QtWebEngineWidgets.QWebEngineView()
    loader.setZoomFactor(1)

    loader.page().pdfPrintingFinished.connect(loader.close)             # <---
    loader.setHtml(html)

    def emit_pdf(finished):
        loader.page().printToPdf(file_name)

    loader.loadFinished.connect(emit_pdf)
    app.exec()
    return True