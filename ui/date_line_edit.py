from PyQt5.QtWidgets import QLineEdit

class DateLineEdit(QLineEdit):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setCursorPosition(0)
