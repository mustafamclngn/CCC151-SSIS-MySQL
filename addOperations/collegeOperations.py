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

class addCollegeDialog(QDialog, Ui_addCollegeDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.addCollegeButton.clicked.connect(self.validateCollegeData)

#ADDING COLLEGE DATA
    def addingCollege(self):
        collegeCode = self.collegeCodeLine.text().strip().replace(" ", "").upper()
        collegeName = self.collegeNameLine.text().strip().title()

        if not collegeCode or not collegeName:
            QMessageBox.warning(self, "Input Error", "All fields must be filled up.")
            return

        if not collegeCode.isalnum() or not all(char.isalpha() or char.isspace() for char in collegeName):
            QMessageBox.warning(self, "Input Error", "Please input a valid college code and name.")
            return

        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        # Check if college code already exists
        cursor.execute("SELECT collegecode FROM COLLEGES WHERE collegecode = %s",
                       (collegeCode,))
        resultcocode = cursor.fetchone()

        if resultcocode:
            QMessageBox.warning(self, "Input Error", "The college code you are trying to add already exists.")
            cursor.close()
            connection.close()
            return

        # Check if college name already exists (ignoring spaces and case)
        finalCollegeName = collegeName.replace(" ", "").upper()
        cursor.execute("SELECT collegename FROM COLLEGES WHERE UPPER(REPLACE(collegename, ' ', '')) = %s",
                       (finalCollegeName,))
        resultconame = cursor.fetchone()

        if resultconame:
            QMessageBox.warning(self, "Input Error", "The college name you are trying to enter already exists.")
            cursor.close()
            connection.close()
            return

        # Insert new college if no conflicts
        cursor.execute("INSERT INTO COLLEGES (collegecode, collegename) VALUES (%s, %s)",
                       (collegeCode, collegeName))
        connection.commit()

        cursor.close()
        connection.close()

        return True
        
#WHEN ADD COLLEGE CLICKED
    def validateCollegeData(self):
        newcollegevalues = self.addingCollege()
        if newcollegevalues:
            self.accept()