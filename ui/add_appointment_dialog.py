# Dialog for adding a new appointment
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, QDateEdit, QTimeEdit, QComboBox
from PyQt5.QtCore import QDate, QTime

class AddAppointmentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Appointment")
        self.setMinimumWidth(350)
        layout = QVBoxLayout()
        form = QFormLayout()
        self.customer_input = QLineEdit()
        from .date_line_edit import DateLineEdit
        self.date_input = DateLineEdit()
        self.date_input.setInputMask("00/00/0000")
        self.date_input.setPlaceholderText("DD/MM/YYYY")
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime())
        self.service_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["Scheduled", "Completed", "Cancelled"])
        self.notes_input = QTextEdit()
        form.addRow("Customer Name:", self.customer_input)
        form.addRow("Date:", self.date_input)
        form.addRow("Time:", self.time_input)
        form.addRow("Service/Reason:", self.service_input)
        form.addRow("Status:", self.status_input)
        form.addRow("Notes:", self.notes_input)
        layout.addLayout(form)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def get_data(self):
        return {
            "customer_name": self.customer_input.text(),
            "date": self.date_input.text(),
            "time": self.time_input.time().toString("HH:mm"),
            "service": self.service_input.text(),
            "status": self.status_input.currentText(),
            "notes": self.notes_input.toPlainText(),
        }
