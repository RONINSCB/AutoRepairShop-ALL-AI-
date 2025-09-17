# Main window for the Automobile Repair Shop App
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from ui.customers import CustomersTab
from ui.inventory import InventoryTab
from ui.billing import BillingTab
from ui.appointments import AppointmentsTab
from ui.obdii.obdii_tab import OBDIITab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automobile Repair Shop Management")
        self.setGeometry(100, 100, 1000, 700)
        self.tabs = QTabWidget()
        # Keep references to each tab for communication
        self.customers_tab = CustomersTab()
        self.inventory_tab = InventoryTab()
        self.billing_tab = BillingTab()
        self.appointments_tab = AppointmentsTab()
        self.obdii_tab = OBDIITab()
        self.tabs.addTab(self.customers_tab, "Customers")
        self.tabs.addTab(self.inventory_tab, "Inventory")
        self.tabs.addTab(self.billing_tab, "Billing")
        self.tabs.addTab(self.appointments_tab, "Appointments")
        self.tabs.addTab(self.obdii_tab, "OBD II")
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
