# Dialog for adding a new inventory item
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox

class AddInventoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Inventory Item")
        self.setMinimumWidth(300)
        layout = QVBoxLayout()
        form = QFormLayout()
        self.name_input = QLineEdit()
        self.category_input = QLineEdit()
        self.code_input = QLineEdit()
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 100000)
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 1000000)
        self.price_input.setDecimals(2)
        self.supplier_input = QLineEdit()
        self.location_input = QLineEdit()
        form.addRow("Name:", self.name_input)
        form.addRow("Category:", self.category_input)
        form.addRow("Code:", self.code_input)
        form.addRow("Quantity:", self.quantity_input)
        form.addRow("Price:", self.price_input)
        form.addRow("Supplier:", self.supplier_input)
        form.addRow("Location:", self.location_input)
        layout.addLayout(form)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        layout.addWidget(self.add_btn)
        self.setLayout(layout)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "category": self.category_input.text(),
            "code": self.code_input.text(),
            "quantity": self.quantity_input.value(),
            "price": self.price_input.value(),
            "supplier": self.supplier_input.text(),
            "location": self.location_input.text(),
        }
