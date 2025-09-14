import sys
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class SplashPage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback

        layout = QVBoxLayout(self)
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        # Load your HTML splash file
        self.browser.load(QUrl.fromLocalFile(
            r"C:\Users\Kunal\OneDrive\Desktop\programs\SIH2025\DEC\ui\splash.html"
        ))

        self.setLayout(layout)

    # ✅ Only run timer when SplashPage is shown
    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(6000, self.finish)

    def finish(self):
        self.switch_callback("login")


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    def test_switch(page):
        print("Switching to:", page)

    win = SplashPage(test_switch)
    win.show()
    sys.exit(app.exec_())
