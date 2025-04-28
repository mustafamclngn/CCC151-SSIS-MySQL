import sys
import re
import mysql.connector

from ui_Dialogs.UI_main import Ui_mainWindow

from ui_Dialogs.addCollegeDialog import Ui_addCollegeDialog
from ui_Dialogs.addProgramDialog import Ui_addProgramDialog
from ui_Dialogs.addStudentDialog import Ui_addStudentDialog
from ui_Dialogs.updateCollegeDialog import Ui_updateCollegeDialog
from ui_Dialogs.UpdateProgramDialog import Ui_updateProgramDialog
from ui_Dialogs.updateStudentDialog import Ui_updateStudentDialog

from addOperations.collegeOperations import *
from addOperations.programOperations import *
from addOperations.studentOperations import *
from editOperations.editCollegeOperations import *
from editOperations.editProgramOperations import *
from editOperations.editStudentOperations import *

from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class updateStudentDialog(QDialog, Ui_updateStudentDialog):
    def __init__(self, idnumber, firstname, lastname, yearlevel, gender, programcode, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.populateprogrambox()
        self.populateyearlevelbox()
        self.populategenderbox()

        self.updIDNumberLine.setText(idnumber)
        self.updfirstNameLine.setText(firstname)
        self.updlastNameLine.setText(lastname)
        self.updyearLevelBox.setCurrentText(yearlevel)
        self.updgenderBox.setCurrentText(gender)
        self.updprogramBox.setCurrentText(programcode)

        self.updateStudentButton.clicked.connect(self.validateUpdateStudent)
    
    def getnewStudent(self):
        newidnumber = self.updIDNumberLine.text().strip()
        newfirstname = self.updfirstNameLine.text().strip()
        newlastname = self.updlastNameLine.text().strip()
        newyearlevel = self.updyearLevelBox.currentText().strip()
        newgender = self.updgenderBox.currentText().strip()
        newprogramcode = self.updprogramBox.currentText().strip()

        if not newidnumber or not newfirstname or not newlastname or not newyearlevel or not newgender or not newprogramcode:
            QMessageBox.warning(self, "Validation Error", "All fields must be filled out.")
            return

        if not re.match(r'^2[0-9]{3}-[0-9]{4}$', newidnumber):
            QMessageBox.warning(self, "Validation Error", "Input a valid student ID number.")
            return

        if not re.match(r'^[A-Za-z\s]+$', newfirstname):
            QMessageBox.warning(self, "Validation Error", "First Name must contain only letters and spaces.")
            return

        if not re.match(r'^[A-Za-z\s]+$', newlastname):
            QMessageBox.warning(self, "Validation Error", "Last Name must contain only letters and spaces.")
            return

        return [self.updIDNumberLine.text(),self.updfirstNameLine.text(), self.updlastNameLine.text(), self.updyearLevelBox.currentText(), self.updgenderBox.currentText(), self.updprogramBox.currentText(),]

    def populateprogrambox(self):
        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT programcode FROM PROGRAMS")
        programCodes = [choice[0] for choice in cursor.fetchall()]
        self.updprogramBox.clear()
        self.updprogramBox.addItems(sorted(programCodes))

        connection.close()
    def populateyearlevelbox(self):
        # Populate year level combo box with predefined values
        self.updyearLevelBox.clear()
        self.updyearLevelBox.addItems(["1", "2", "3", "4"])

    def populategenderbox(self):
        # Populate gender combo box with predefined values
        self.updgenderBox.clear()
        self.updgenderBox.addItems(["M","F"])

    def validateUpdateStudent(self):
        newstudentvalues = self.getnewStudent()
        if newstudentvalues:
            self.accept()