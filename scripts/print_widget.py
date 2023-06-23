import sys
from PyQt5.QtWidgets import QApplication, QTextBrowser


if __name__ == '__main__':
    app = QApplication(sys.argv)

    browser = QTextBrowser()
    browser.setHtml('<h1>Example Title</h1><p>This is an example of a QTextBrowser.</p>')

    browser.show()

    sys.exit(app.exec_())
