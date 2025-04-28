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

class updateCollegeDialog(QDialog, Ui_updateCollegeDialog):
    def __init__(self, collegeCode, collegeName,parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.oldcollegecode = collegeCode
        self.oldcollegename = collegeName

        self.updcollegeCodeLine.setText(collegeCode)
        self.updcollegeNameLine.setText(collegeName)

        self.updateCollegeButton.clicked.connect(self.validateUpdateCollege)

    def getnewCollege(self):
        newcollegecode = self.updcollegeCodeLine.text().strip().replace(" ", "").upper()
        newcollegename = self.updcollegeNameLine.text().strip().title()

        if not newcollegecode or not newcollegename:
            QMessageBox.warning(self, "Input Error", "All fields must be filled up.")
            return None

        if not newcollegecode.isalnum() or not all(char.isalpha() or char.isspace() for char in newcollegename):
            QMessageBox.warning(self, "Input Error", "Please input a valid college code and name.")
            return None

        if (newcollegecode == self.oldcollegecode and newcollegename == self.oldcollegename):
            return [self.oldcollegecode, self.oldcollegename]
        
        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        cursor.execute("SELECT collegecode FROM COLLEGES WHERE collegecode = %s AND collegecode <> %s",
                       (newcollegecode, self.oldcollegecode))
        result_code = cursor.fetchone()

        if result_code:
            QMessageBox.warning(self, "Input Error", "The college code you are trying to add already exists.")
            cursor.close()
            connection.close()
            return None

        finalcollegename = newcollegename.replace(" ", "").upper()
        cursor.execute("SELECT collegename FROM COLLEGES WHERE UPPER(REPLACE(collegename, ' ', '')) = %s AND collegecode <> %s",
                       (finalcollegename, self.oldcollegecode))
        result_name = cursor.fetchone()

        if result_name:
            QMessageBox.warning(self, "Input Error", "The college name you are trying to enter already exists.")
            cursor.close()
            connection.close()
            return None
        
        cursor.close()
        connection.close()

        return [newcollegecode, newcollegename]
    
    def validateUpdateCollege(self):
        newcollegevalues = self.getnewCollege()
        if newcollegevalues:
            self.accept()