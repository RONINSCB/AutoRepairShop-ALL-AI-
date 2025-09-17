# Dialog for adding a new customer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton

class AddCustomerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Customer")
        self.setMinimumWidth(300)
        layout = QVBoxLayout()
        form = QFormLayout()
        self.name_input = QLineEdit()
        self.surname_input = QLineEdit()
        self.plate_input = QLineEdit()
        self.chassis_input = QLineEdit()
        form.addRow("Name:", self.name_input)
        form.addRow("Surname:", self.surname_input)
        form.addRow("Plate Number:", self.plate_input)
        form.addRow("Chassis Number:", self.chassis_input)
        layout.addLayout(form)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "surname": self.surname_input.text(),
            "plate": self.plate_input.text(),
            "chassis": self.chassis_input.text(),
        }
