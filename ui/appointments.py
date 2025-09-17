# Appointments Tab
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem
from utils.database import Database
from ui.add_appointment_dialog import AddAppointmentDialog

class AppointmentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        layout = QVBoxLayout()
        # Search bar
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.filter_appointments)
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Customer Name", "Date", "Time", "Service", "Status", "Notes"])
        self.filter_combo.currentIndexChanged.connect(self.filter_appointments)
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.search_field)
        layout.addLayout(search_layout)
        # Add and Delete buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Appointment")
        add_button.clicked.connect(self.open_add_appointment_dialog)
        button_layout.addWidget(add_button)
        delete_button = QPushButton("Delete Appointment")
        delete_button.clicked.connect(self.delete_selected_appointment)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        # Table (all columns)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Customer Name", "Date", "Time", "Service", "Status", "Notes"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.ExtendedSelection)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.all_appointments = []
        self.load_appointments()

    def delete_selected_appointment(self):
        selected_rows = set(idx.row() for idx in self.table.selectedIndexes())
        if not selected_rows:
            return  # No row selected
        for row in sorted(selected_rows, reverse=True):
            appointment_id = self.all_appointments[row][0]
            self.db.delete_appointment(appointment_id)
        self.load_appointments()

    def load_appointments(self):
        self.all_appointments = self.db.get_appointments()
        self.show_appointments(self.all_appointments)

    def show_appointments(self, appointments):
        self.table.setRowCount(len(appointments))
        for row, appointment in enumerate(appointments):
            # appointment: (id, customer_name, date, time, service, status, notes)
            self.table.setItem(row, 0, QTableWidgetItem(str(appointment[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(appointment[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(appointment[2])))
            self.table.setItem(row, 3, QTableWidgetItem(str(appointment[3])))
            self.table.setItem(row, 4, QTableWidgetItem(str(appointment[4])))
            self.table.setItem(row, 5, QTableWidgetItem(str(appointment[5])))
            self.table.setItem(row, 6, QTableWidgetItem(str(appointment[6])))

    def filter_appointments(self):
        text = self.search_field.text().lower()
        filter_by = self.filter_combo.currentText().lower()
        idx = {"id": 0, "customer name": 1, "date": 2, "time": 3, "service": 4, "status": 5, "notes": 6}.get(filter_by, 1)
        filtered = [i for i in self.all_appointments if text in str(i[idx]).lower()]
        self.show_appointments(filtered)

    def open_add_appointment_dialog(self):
        dialog = AddAppointmentDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            self.db.add_appointment(data["customer_name"], data["date"], data["time"], data["service"], data["status"], data["notes"])
            self.load_appointments()
