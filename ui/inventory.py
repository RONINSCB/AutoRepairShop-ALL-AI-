# Inventory Tab
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem
from utils.database import Database
from ui.add_inventory_dialog import AddInventoryDialog

class InventoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        layout = QVBoxLayout()
        # Search bar
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.filter_items)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Name", "Category", "Code", "Quantity", "Price", "Supplier", "Location"])
        self.filter_combo.currentIndexChanged.connect(self.filter_items)
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.search_field)
        layout.addLayout(search_layout)
        # Add and Delete buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Item")
        add_button.clicked.connect(self.open_add_item_dialog)
        button_layout.addWidget(add_button)
        delete_button = QPushButton("Delete Item")
        delete_button.clicked.connect(self.delete_selected_item)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        # Table (all columns)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "Code", "Quantity", "Price", "Supplier", "Location"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.ExtendedSelection)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.all_items = []
        self.load_items()

    def delete_selected_item(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows:
            return  # No row selected
        for row in sorted(selected_rows, reverse=True):
            item_id = self.all_items[row][0]
            self.db.delete_inventory_item(item_id)
        self.load_items()

    def load_items(self):
        self.all_items = self.db.get_inventory()
        self.show_items(self.all_items)

    def show_items(self, items):
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            # item: (id, name, category, code, quantity, price, supplier, location)
            self.table.setItem(row, 0, QTableWidgetItem(str(item[1])))
            self.table.setItem(row, 1, QTableWidgetItem(str(item[2])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item[3])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item[4])))
            self.table.setItem(row, 4, QTableWidgetItem(str(item[5])))
            self.table.setItem(row, 5, QTableWidgetItem(str(item[6])))
            self.table.setItem(row, 6, QTableWidgetItem(str(item[7])))

    def filter_items(self):
        text = self.search_field.text().lower()
        filter_by = self.filter_combo.currentText().lower()
        idx = {"name": 1, "category": 2, "code": 3, "quantity": 4, "price": 5, "supplier": 6, "location": 7}[filter_by]
        filtered = [i for i in self.all_items if text in str(i[idx]).lower()]
        self.show_items(filtered)

    def open_add_item_dialog(self):
        dialog = AddInventoryDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.db.add_inventory_item(
                data["name"], data["category"], data["code"],
                data["quantity"], data["price"], data["supplier"], data["location"]
            )
            self.load_items()
