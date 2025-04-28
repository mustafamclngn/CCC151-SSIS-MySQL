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

class MainClass(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.currentTable = self.displayBox.currentIndex()
        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.updateButton.clicked.connect(self.updateButtonClicked)
        self.displayBox.currentIndexChanged.connect(self.loadDatabase)
        self.sortBox.currentIndexChanged.connect(self.sortTable)
        self.refreshButton.clicked.connect(self.loadDatabase)
        self.searchButton.clicked.connect(self.searchTable)

        self.tableShown = None
        self.loadDatabase()

    def mysqlConnection(self):
        return mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "admin",
            database = "SSISREMAKE"
        )

    def loadDatabase(self):
        self.tableShown = self.displayBox.currentText()
        self.clearHeader()

        connection = self.mysqlConnection()
        mycursor = connection.cursor()

        query = f"SELECT * FROM {self.tableShown}"
        mycursor.execute(query)
        rows = mycursor.fetchall()
        columns = [col[0].upper() for col in mycursor.description]

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

        mycursor.close()
        connection.close()

    def clearHeader(self):
        self.comboBoxItems()
        self.tableWidget.clearSelection()
        self.tableWidget.setCurrentItem(None)

        #RESET HIDDEN ROWS
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(row, False)

    def searchTable(self):
        searchColumn = self.searchBox.currentText()
        searchTerm = self.searchLine.text().strip()

        if not searchColumn:
            QMessageBox.warning(self, "Search Error", "Select a data to search.")
            return
        
        if not searchTerm:
            QMessageBox.warning(self, "Search Error", "Input a search term.")
            return

        if searchColumn and searchTerm:
            column_index = self.searchBox.currentIndex()
            found = False
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, column_index)
                if item and searchTerm.lower() in item.text().lower():
                    self.tableWidget.setRowHidden(row, False)
                    found = True
                else:
                    self.tableWidget.setRowHidden(row, True)

            self.tableWidget.setCurrentItem(None)

            if not found:
                QMessageBox.information(self, "No Results", "No matching records found.")

    def sortTable(self):
        sortColumn = self.sortBox.currentText()
        sortOrder = QtCore.Qt.AscendingOrder

        if sortColumn:
            column_index = self.sortBox.currentIndex()
            self.tableWidget.sortItems(column_index, sortOrder)

    def comboBoxItems(self):
        self.sortBox.clear()
        self.searchBox.clear()
        self.searchLine.clear()

        table_headers = {
            "STUDENTS": ['ID NUMBER', 'FIRST NAME', 'LAST NAME', 'YEAR LEVEL', 'GENDER', 'PROGRAM CODE'],
            "PROGRAMS": ['PROGRAM CODE', 'PROGRAM NAME', 'COLLEGE CODE'],
            "COLLEGES": ['COLLEGE CODE', 'COLLEGE NAME']
        }

        if self.tableShown in table_headers:
            headers = table_headers[self.tableShown]
            self.sortBox.addItems(headers)
            self.searchBox.addItems(headers)

        self.sortBox.setCurrentIndex(-1)
        self.searchBox.setCurrentIndex(-1)

    def addButtonClicked(self):
        add_actions = {
            0: self.addStudent,
            1: self.addProgram,
            2: self.addCollege
        }

        action = add_actions.get(self.displayBox.currentIndex())
        if action:
            action()
            
    def deleteButtonClicked(self):
        delete_actions = {
            0: self.deleteStudent,
            1: self.deleteProgram,
            2: self.deleteCollege
        }

        action = delete_actions.get(self.displayBox.currentIndex())
        if action:
            action()
        
    def updateButtonClicked(self):
        update_actions = {
            0: self.updateStudent,
            1: self.updateProgram,
            2: self.updateCollege
        }

        action = update_actions.get(self.displayBox.currentIndex())
        if action:
            action()

# ===============================================================================================================================================================================================================

# UPDATE FUNCTIONS                            

# ===============================================================================================================================================================================================================

    def updateStudent(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a student to update.")
            return
        
        oldstudentID = self.tableWidget.item(selected_row, 0).text()
        oldfirstName = self.tableWidget.item(selected_row, 1).text()
        oldlastName = self.tableWidget.item(selected_row, 2).text()
        oldyearLevel = self.tableWidget.item(selected_row, 3).text()
        oldgender = self.tableWidget.item(selected_row, 4).text()
        oldprogramCode = self.tableWidget.item(selected_row, 5).text()

        updateStudent = updateStudentDialog(oldstudentID, oldfirstName, oldlastName, oldyearLevel, oldgender, oldprogramCode, self)
        if updateStudent.exec_():
            newstudentdata = updateStudent.getnewStudent()

            if not newstudentdata:
                return
            
            newstudentID, newfirstName, newlastName, newyearLevel, newgender, newprogramCode = newstudentdata

            connection = self.mysqlConnection()
            cursor = connection.cursor()

            #  COUNT HOW MANY PROGRAMS ARE AFFECTED
            cursor.execute("SELECT COUNT(*) FROM PROGRAMS WHERE programcode = %s",
                           (oldprogramCode,))
            self.programCount = cursor.fetchone()[0]

            cursor.execute("UPDATE STUDENTS SET firstname = %s, lastname = %s, yearlevel = %s, gender = %s, programcode = %s WHERE idnumber = %s",
                           (newfirstName, newlastName, newyearLevel, newgender, newprogramCode, oldstudentID))
            connection.commit()
            cursor.close()
            connection.close()

            self.loadDatabase()
            self.successUpdateStudent()

    def updateProgram(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a program to update.")
            return
        
        oldprogramcode = self.tableWidget.item(selected_row, 0).text()
        oldprogramname = self.tableWidget.item(selected_row, 1).text()
        oldcollegecode = self.tableWidget.item(selected_row, 2).text()

        updateProgram = UpdateProgramDialog(oldprogramcode, oldprogramname, oldcollegecode, self)
        if updateProgram.exec_():
            newprogramdata = updateProgram.getnewProgram()

            if not newprogramdata:
                return
            
            newprogramcode, newprogramname, newcollegecode = newprogramdata

            connection = self.mysqlConnection()
            cursor = connection.cursor()

            #COUNT HOW MANY STUDENTS ARE AFFECTED
            cursor.execute("SELECT COUNT(*) FROM STUDENTS WHERE programcode = %s",
                           (oldprogramcode,))
            self.programCount = cursor.fetchone()[0]

            cursor.execute("UPDATE PROGRAMS SET programcode = %s, programname = %s, collegecode = %s WHERE programcode = %s",
                           (newprogramcode, newprogramname, newcollegecode, oldprogramcode))
            connection.commit()

            cursor.close()
            connection.close()

            self.loadDatabase()
            self.successUpdateProgram()

    def updateCollege(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a college to update.")
            return

        oldcollegecode = self.tableWidget.item(selected_row, 0).text()
        oldecollegename = self.tableWidget.item(selected_row, 1).text()

        updateCollege = updateCollegeDialog(oldcollegecode, oldecollegename, self)
        if updateCollege.exec_():
            newcollegedata = updateCollege.getnewCollege()

            if not newcollegedata:
                return
            
            newcollegecode,newcollegename = newcollegedata

            connection = self.mysqlConnection()
            cursor = connection.cursor()

            self.programCount = 0

            #COUNT HOW MANY PROGRAMS ARE AFFECTED
            cursor.execute("SELECT COUNT(*) FROM PROGRAMS WHERE collegecode = %s",
                           (oldcollegecode,))
            self.programCount = cursor.fetchone()[0]

            cursor.execute("UPDATE COLLEGES SET collegecode = %s, collegename = %s WHERE collegecode = %s",
                           (newcollegecode, newcollegename, oldcollegecode))
            connection.commit()

            cursor.close()
            connection.close()

            self.loadDatabase()
            self.successUpdateCollege()

# ===============================================================================================================================================================================================================

# ADD OPERATIONS                          

# ===============================================================================================================================================================================================================

    def addStudent(self):
        studentAdd = addStudentDialog(self)
        if studentAdd.exec_():
            self.loadDatabase()
            self.successaddStudent()

    def addProgram(self):
        programAdd = addProgramDialog(self)
        if programAdd.exec_():
            self.loadDatabase()
            self.successaddProgram()

    def addCollege(self):
        collegeAdd = addCollegeDialog(self) 
        if collegeAdd.exec_():
            self.loadDatabase()
            self.successaddCollege()

# ===============================================================================================================================================================================================================

# SUCCES ADD, DELETE AND UPDATE MESSAGES                      

# ===============================================================================================================================================================================================================
    
    def successaddStudent(self):
        QMessageBox.information(self, "Success", "Student added successfully!")

    def successaddProgram(self):
        QMessageBox.information(self, "Success", "Program added successfully!")
    
    def successaddCollege(self):
        QMessageBox.information(self, "Success", "College added successfully!")
    
    def successdeleteStudent(self):
        QMessageBox.information(self, "Success", "Student deleted successfully!")
    
    def successdeleteProgram(self):
        QMessageBox.information(self, "Success", "Program deleted successfully! Students under this program now have NULL programs.")
    
    def successdeleteCollege(self):
        QMessageBox.information(self, "Success", "College deleted successfully! Programs under this college have been deleted.")

    def successUpdateStudent(self):
        QMessageBox.information(self, "Success", "Student updated successfully!")

    def successUpdateProgram(self):
        QMessageBox.information(self, "Success", "Program updated successfully!")

    def successUpdateCollege(self):
        QMessageBox.information(self, "Success", "College updated successfully!")
    
# ===============================================================================================================================================================================================================

# DELETE FUNCTIONS                             

# ===============================================================================================================================================================================================================

    def deleteStudent(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a student to delete.")
            return

        studentID = self.tableWidget.item(selected_row, 0).text()

        confirmation = QMessageBox.question(self,
            "Confirm Deletion",
            f"Are you sure you want to delete the student with ID '{studentID}'?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmation == QMessageBox.No:
            return

        connection = self.mysqlConnection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM STUDENTS WHERE idnumber = %s",
                       (studentID,))
        connection.commit()

        cursor.close()
        connection.close()

        self.loadDatabase()
        self.successdeleteStudent()

    def deleteProgram(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a program to delete.")
            return

        programCode = self.tableWidget.item(selected_row, 0).text()

        confirmation = QMessageBox.question(self,
            "Confirm Deletion",
            f"Are you sure you want to delete the program '{programCode}'? Students under this program will have their program set to NULL.",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmation == QMessageBox.No:
            return

        connection = self.mysqlConnection()
        cursor = connection.cursor()

        #SET PROGRAM CODE TO NULL FOR STUDENTS UNDER THIS PROGRAM
        cursor.execute("UPDATE STUDENTS SET programcode = NULL WHERE programcode = %s",
                       (programCode,))
        connection.commit()

        #DELETE THE PROGRAM
        cursor.execute("DELETE FROM PROGRAMS WHERE programcode = %s",
                       (programCode,))
        connection.commit()

        cursor.close()
        connection.close()

        self.loadDatabase()
        self.successdeleteProgram()

    def deleteCollege(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a college to delete.")
            return

        collegeCode = self.tableWidget.item(selected_row, 0).text()

        confirmation = QMessageBox.question(self,
            "Confirm Deletion",
            f"Are you sure you want to delete the college '{collegeCode}' and all associated programs?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmation == QMessageBox.No:
            return

        connection = self.mysqlConnection()
        cursor = connection.cursor()

        #DELETE PROGRAMS UNDER THIS COLLEGE
        cursor.execute("DELETE FROM PROGRAMS WHERE collegecode = %s",
                       (collegeCode,))
        connection.commit()

        #DELETE THE COLLEGE
        cursor.execute("DELETE FROM COLLEGES WHERE collegecode = %s",
                       (collegeCode,))
        connection.commit()

        cursor.close()
        connection.close()

        self.loadDatabase()
        self.successdeleteCollege()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainClass()
    main.show()
    app.exec_()