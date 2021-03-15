from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)
from .model import ContactsModel


class Window(QMainWindow):
    """ Main Window """
    def __init__(self, parent=None):
        """ Initializer. """
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel = ContactsModel()
        self.setupUI()

    def setupUI(self):
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.resizeColumnsToContents
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clearContacts)
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def openAddDialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()
    
    def deleteContact(self):
        row = self.table.currentIndex().row()
        if row <0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.StandardButtons.Yes | QMessageBox.StandardButtons.Cancel,
        )
        if messageBox == QMessageBox.StandardButtons.Yes:
            self.contactsModel.deleteContact(row)

    def clearContacts(self):
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove all your contacts?",
            QMessageBox.StandardButtons.Yes | QMessageBox.StandardButtons.Cancel,
        )

        if messageBox == QMessageBox.StandardButtons.Yes:
            self.contactsModel.clearContacts()

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        self.setupUI()

    def setupUI(self):
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.jobField = QLineEdit()
        self.jobField.setObjectName("Job")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        #Layout
        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Job:", self.jobField)
        layout.addRow("Email:", self.emailField)
        self.layout.addLayout(layout)
        # Buttons
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Orientations.Horizontal)
        self.buttonsBox.setStandardButtons(QDialogButtonBox.StandardButtons.Yes | QDialogButtonBox.StandardButtons.Cancel)
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        self.data = []
        for field in (self.nameField, self.jobField, self.emailField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None
                return

            self.data.append(field.text())
        if not self.data:
            return
        super().accept()

