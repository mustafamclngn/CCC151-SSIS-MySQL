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

class addStudentDialog(QDialog, Ui_addStudentDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.stunpr()
        self.yearLevelBox.setCurrentIndex(-1)
        self.genderBox.setCurrentIndex(-1)
        self.addStudentButton.clicked.connect(self.validateStudentData)
        self.programBox.setCurrentIndex(-1)

#STUDENTS UNDER THE PROGRAM
    def stunpr(self):
        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        query_code = "SELECT DISTINCT programcode FROM PROGRAMS"
        cursor.execute(query_code)
        stunpr = [choice[0] for choice in cursor.fetchall()]
        self.programBox.clear()
        self.programBox.addItems(sorted(stunpr))

        connection.close()
        cursor.close()

#VALIDATE STUDENT ID NUMBER FROMAT
    def validatestudentID(self, studentID, edit_state=False):
        if not edit_state:
            validstudentID = re.match(r'^2[0-9]{3}-[0-9]{4}$', studentID)
        else:
            validstudentID = re.match(r'^2[0-9]{3}-[0-9]{4}$|^$', studentID)
        return True if validstudentID else False

#ADDING STUDENT DATA
    def addingStudent(self):
        studentID = self.IDNumberLine.text().strip()
        firstName = self.firstNameLine.text().strip().title()
        lastName = self.lastNameLine.text().strip().title()
        yearLevel = self.yearLevelBox.currentText()
        gender = self.genderBox.currentText()
        programCode = self.programBox.currentText()

        if not studentID or not firstName or not lastName or not yearLevel or not gender or not programCode:
            QMessageBox.warning(self, "Input Error", "All fields must be filled up.")
            return
        
        if not self.validatestudentID(studentID):
            QMessageBox.warning(self, "Input Error", "Please input a valid student ID number.")
            return
        
        connection = self.parent().mysqlConnection()
        cursor = connection.cursor()

        # Check if student ID already exists
        cursor.execute("SELECT idnumber FROM STUDENTS WHERE idnumber = %s",
                       (studentID,))
        uniqueID = cursor.fetchone()

        if uniqueID:
            QMessageBox.warning(self, "Input Error", "The student ID you are trying to add already exists.")
            cursor.close()
            connection.close()
            return
        
        cursor.execute("INSERT INTO STUDENTS (idnumber, firstname, lastname, yearlevel, gender, programcode) VALUES (%s, %s, %s, %s, %s, %s)",
                       (studentID, firstName, lastName, yearLevel,gender, programCode))
        connection.commit()

        cursor.close()
        connection.close()

        return True
    
#WHEN ADD STUDENT CLICKED
    def validateStudentData(self):
        newstudentvalues = self.addingStudent()
        if newstudentvalues:
            self.accept()