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

class UpdateProgramDialog(QDialog, Ui_updateProgramDialog):
    def __init__(self, programCode, programName, collegeCode, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.populatecollegebox()

        self.oldprogramcode = programCode
        self.oldprogramname = programName
        self.oldcollegecode = collegeCode

        self.updprogramCodeLine.setText(programCode)
        self.updprogramNameLine.setText(programName)
        self.updprcollegecodeBox.setCurrentText(collegeCode)

        self.updateProgramButton.clicked.connect(self.validateUpdateProgram)

    def populatecollegebox(self):
        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        query_code = "SELECT DISTINCT collegecode FROM COLLEGES"
        cursor.execute(query_code)
        collegeCodes = [choice[0] for choice in cursor.fetchall()]
        self.updprcollegecodeBox.clear()
        self.updprcollegecodeBox.addItems(sorted(collegeCodes))

        connection.close()
        cursor.close()

    def getnewProgram(self):
        newprogramcode = self.updprogramCodeLine.text().strip().replace(" ", "").upper()
        newprogramname = self.updprogramNameLine.text().strip().title()
        newcollegecode = self.updprcollegecodeBox.currentText()

        if not newprogramcode or not newprogramname or not newcollegecode:
            QMessageBox.warning(self, "Input Error", "All fields must be filled up.")
            return None

        if not newprogramcode.isalnum() or not all(char.isalpha() or char.isspace() for char in newprogramname):
            QMessageBox.warning(self, "Input Error", "Please input a valid program code and name.")
            return None

        if (newprogramcode == self.oldprogramcode and newprogramname == self.oldprogramname and newcollegecode == self.oldcollegecode):
            return [self.oldprogramcode, self.oldprogramname, self.oldcollegecode]

        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        cursor.execute("SELECT programcode FROM PROGRAMS WHERE programcode = %s AND programcode <> %s",
                       (newprogramcode, self.oldprogramcode))
        result_code = cursor.fetchone()

        if result_code:
            QMessageBox.warning(self, "Input Error", "The program code you are trying to add already exists.")
            cursor.close()
            connection.close()
            return None

        finalprogramname = newprogramname.replace(" ", "").upper()
        cursor.execute("SELECT programname FROM PROGRAMS WHERE UPPER(REPLACE(programname, ' ', '')) = %s AND programcode <> %s",
                       (finalprogramname, self.oldprogramcode))
        result_name = cursor.fetchone()

        if result_name:
            QMessageBox.warning(self, "Input Error", "The program name you are trying to enter already exists.")
            cursor.close()
            connection.close()
            return None
        
        cursor.close()
        connection.close()

        return [newprogramcode, newprogramname, newcollegecode]
    
    def validateUpdateProgram(self):
        newprogramvalues = self.getnewProgram()
        if newprogramvalues:
            self.accept()