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

class addProgramDialog(QDialog, Ui_addProgramDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.pruncol()
        self.prcollegecodeBox.setCurrentIndex(-1)
        self.addProgramButton.clicked.connect(self.validateProgramData)

#PROGRAMS UNDER THE COLLEGE
    def pruncol(self):
        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT collegecode FROM COLLEGES")
        pruncol = [choice[0] for choice in cursor.fetchall()]
        self.prcollegecodeBox.clear()
        self.prcollegecodeBox.addItems(sorted(pruncol))

        connection.close()
        cursor.close()

#ADDING PROGRAM DATA
    def addingProgram(self):
        programCode = self.programCodeLine.text().strip().replace(" ", "").upper()
        programName = self.programNameLine.text().strip().title()
        collegeCode = self.prcollegecodeBox.currentText()

        if not programCode or not programName or not collegeCode:
            QMessageBox.warning(self, "Input Error", "All fields must be filled up.")
            return

        if not programCode.isalnum() or not all(char.isalpha() or char.isspace() for char in programName):
            QMessageBox.warning(self, "Input Error", "Please input a valid program code and name.")
            return

        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        # Check if program code already exists
        cursor.execute("SELECT programcode FROM PROGRAMS WHERE programcode = %s",
                       (programCode,))
        uniqueprcode = cursor.fetchone()

        if uniqueprcode:
            QMessageBox.warning(self, "Input Error", "The program code you are trying to add already exists.")
            cursor.close()
            connection.close()
            return

        # Check if program name already exists (ignoring spaces and case)
        finalprogramName = programName.replace(" ", "").upper()
        cursor.execute("SELECT programname FROM PROGRAMS WHERE UPPER(REPLACE(programname, ' ', '')) = %s",
                       (finalprogramName,))
        uniqueprname = cursor.fetchone()

        if uniqueprname:
            QMessageBox.warning(self, "Input Error", "The program name you are trying to enter already exists.")
            cursor.close()
            connection.close()
            return

        # Insert new program if no conflicts
        cursor.execute("INSERT INTO PROGRAMS (programcode, programname, collegecode) VALUES (%s, %s, %s)",
                       (programCode, programName, collegeCode))
        connection.commit()

        cursor.close()
        connection.close()

        return True
    
#WHEN ADD PROGRAM CLICKED
    def validateProgramData(self):
        newprogramvalues = self.addingProgram()
        if newprogramvalues:
            self.accept()