# Billing Tab
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem
from utils.database import Database
from ui.add_billing_dialog import AddBillingDialog

class BillingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        layout = QVBoxLayout()
        # Search bar
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.filter_invoices)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Invoice No", "Customer Name", "Date", "Description", "Total", "Notes"])
        self.filter_combo.currentIndexChanged.connect(self.filter_invoices)
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.search_field)
        layout.addLayout(search_layout)
        # Add and Delete buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Invoice")
        add_button.clicked.connect(self.open_add_invoice_dialog)
        button_layout.addWidget(add_button)
        delete_button = QPushButton("Delete Invoice")
        delete_button.clicked.connect(self.delete_selected_invoice)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        # Table (all columns)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Invoice No", "Customer Name", "Date", "Description", "Total", "Notes"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.ExtendedSelection)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.all_invoices = []
        self.load_invoices()

    def delete_selected_invoice(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows:
            return  # No row selected
        for row in sorted(selected_rows, reverse=True):
            billing_id = self.all_invoices[row][0]
            self.db.delete_billing(billing_id)
        self.load_invoices()

    def load_invoices(self):
        self.all_invoices = self.db.get_billing()
        self.show_invoices(self.all_invoices)

    def show_invoices(self, invoices):
        self.table.setRowCount(len(invoices))
        for row, invoice in enumerate(invoices):
            # invoice: (id, customer_name, date, description, total, notes)
            self.table.setItem(row, 0, QTableWidgetItem(str(invoice[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(invoice[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(invoice[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(invoice[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(invoice[4])))
            self.table.setItem(row, 5, QTableWidgetItem(str(invoice[5])))

    def filter_invoices(self):
        text = self.search_field.text().lower()
        filter_by = self.filter_combo.currentText().lower()
        idx = {"invoice no": 0, "customer name": 1, "date": 2, "description": 3, "total": 4, "notes": 5}[filter_by]
        filtered = [i for i in self.all_invoices if text in str(i[idx]).lower()]
        self.show_invoices(filtered)

    def open_add_invoice_dialog(self):
        dialog = AddBillingDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.db.add_billing(data["customer_name"], data["date"], data["description"], data["total"], data["notes"])
            self.load_invoices()
