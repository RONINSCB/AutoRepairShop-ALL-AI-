# Dialog for adding a new OBD II record
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton

class AddOBDIIDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add OBD II Record")
        self.setMinimumWidth(350)
        layout = QVBoxLayout()
        form = QFormLayout()
        self.dtc_input = QLineEdit()
        self.description_input = QTextEdit()
        self.fix_input = QTextEdit()
        form.addRow("DTC Code:", self.dtc_input)
        form.addRow("Description:", self.description_input)
        form.addRow("Fix/Notes:", self.fix_input)
        layout.addLayout(form)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def get_data(self):
        return {
            "dtc": self.dtc_input.text(),
            "description": self.description_input.toPlainText(),
            "fix": self.fix_input.toPlainText(),
        }
