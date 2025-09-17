# Customers Tab
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QComboBox
from utils.database import Database
from ui.add_customer_dialog import AddCustomerDialog

class CustomersTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        layout = QVBoxLayout()
        # Search bar
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.filter_customers)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Name", "Surname", "Plate", "Chassis"])
        self.filter_combo.currentIndexChanged.connect(self.filter_customers)
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.search_field)
        layout.addLayout(search_layout)
        # Add and Delete buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Customer")
        add_button.clicked.connect(self.open_add_customer_dialog)
        button_layout.addWidget(add_button)
        delete_button = QPushButton("Delete Customer")
        delete_button.clicked.connect(self.delete_selected_customer)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Surname", "Plate", "Chassis"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.ExtendedSelection)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.all_customers = []
        self.load_customers()

    def delete_selected_customer(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows:
            return  # No row selected
        # Sort in reverse to avoid index shifting
        for row in sorted(selected_rows, reverse=True):
            customer_id = self.all_customers[row][0]
            self.db.delete_customer(customer_id)
        self.load_customers()

    def load_customers(self):
        self.all_customers = self.db.get_customers()
        self.show_customers(self.all_customers)

    def show_customers(self, customers):
        self.table.setRowCount(len(customers))
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(customer[1]))
            self.table.setItem(row, 1, QTableWidgetItem(customer[2]))
            self.table.setItem(row, 2, QTableWidgetItem(customer[3]))
            self.table.setItem(row, 3, QTableWidgetItem(customer[4]))

    def filter_customers(self):
        text = self.search_field.text().lower()
        filter_by = self.filter_combo.currentText().lower()
        idx = {"name": 1, "surname": 2, "plate": 3, "chassis": 4}[filter_by]
        filtered = [c for c in self.all_customers if text in c[idx].lower()]
        self.show_customers(filtered)

    def open_add_customer_dialog(self):
        dialog = AddCustomerDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.db.add_customer(data["name"], data["surname"], data["plate"], data["chassis"])
            self.load_customers()
