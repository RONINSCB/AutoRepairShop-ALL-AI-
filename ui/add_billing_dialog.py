# Dialog for adding a new billing/invoice record
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, QDateEdit, QDoubleSpinBox
from ui.date_line_edit import DateLineEdit
from PyQt5.QtCore import QDate

class AddBillingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Invoice")
        self.setMinimumWidth(350)
        layout = QVBoxLayout()
        form = QFormLayout()
        self.customer_input = QLineEdit()
        self.date_input = DateLineEdit()
        self.date_input.setInputMask("00/00/0000")
        self.date_input.setPlaceholderText("DD/MM/YYYY")
        self.description_input = QTextEdit()
        self.total_input = QDoubleSpinBox()
        self.total_input.setRange(0, 1000000)
        self.total_input.setDecimals(2)
        self.notes_input = QTextEdit()
        form.addRow("Customer Name:", self.customer_input)
        form.addRow("Date:", self.date_input)
        form.addRow("Description:", self.description_input)
        form.addRow("Total Amount:", self.total_input)
        form.addRow("Notes:", self.notes_input)
        layout.addLayout(form)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def eventFilter(self, obj, event):
        if obj == self.date_input and (event.type() == event.FocusIn or event.type() == event.MouseButtonPress):
            self.date_input.setCursorPosition(0)
        return super().eventFilter(obj, event)

    def get_data(self):
        return {
            "customer_name": self.customer_input.text(),
            "date": self.date_input.text(),
            "description": self.description_input.toPlainText(),
            "total": self.total_input.value(),
            "notes": self.notes_input.toPlainText(),
        }
