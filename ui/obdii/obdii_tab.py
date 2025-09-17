from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem
from utils.database import Database
from ui.obdii.add_obdii_dialog import AddOBDIIDialog

class OBDIITab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        layout = QVBoxLayout()
        # Search bar
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.filter_records)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["DTC"])
        self.filter_combo.currentIndexChanged.connect(self.filter_records)
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.search_field)
        layout.addLayout(search_layout)
        # Add and Delete buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add OBD II Record")
        add_button.clicked.connect(self.open_add_obdii_dialog)
        button_layout.addWidget(add_button)
        delete_button = QPushButton("Delete OBD II Record")
        delete_button.clicked.connect(self.delete_selected_obdii_record)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["DTC", "Description", "Fix/Notes"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.ExtendedSelection)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.all_records = []
        self.load_records()

    def delete_selected_obdii_record(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows:
            return  # No row selected
        for row in sorted(selected_rows, reverse=True):
            record_id = self.all_records[row][0]
            self.db.delete_obdii_record(record_id)
        self.load_records()

    def load_records(self):
        self.all_records = self.db.get_obdii_records()
        self.show_records(self.all_records)

    def show_records(self, records):
        self.table.setRowCount(len(records))
        for row, rec in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(rec[1])))
            self.table.setItem(row, 1, QTableWidgetItem(str(rec[2])))
            self.table.setItem(row, 2, QTableWidgetItem(str(rec[3])))

    def filter_records(self):
        text = self.search_field.text().lower()
        # Only filter by DTC (index 1 in record tuple)
        filtered = [r for r in self.all_records if text in str(r[1]).lower()]
        self.show_records(filtered)

    def open_add_obdii_dialog(self):
        dialog = AddOBDIIDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.db.add_obdii_record(data["dtc"], data["description"], data["fix"])
            self.load_records()
