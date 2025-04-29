from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_updateCollegeDialog(object):
    def setupUi(self, updateCollegeDialog):
        updateCollegeDialog.setObjectName("updateCollegeDialog")
        updateCollegeDialog.resize(448, 369)
        self.updatecollegeCodeLabel = QtWidgets.QLabel(updateCollegeDialog)
        self.updatecollegeCodeLabel.setGeometry(QtCore.QRect(20, 130, 124, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.updatecollegeCodeLabel.setFont(font)
        self.updatecollegeCodeLabel.setObjectName("updatecollegeCodeLabel")
        self.updatecollegeNameLabel = QtWidgets.QLabel(updateCollegeDialog)
        self.updatecollegeNameLabel.setGeometry(QtCore.QRect(20, 200, 125, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.updatecollegeNameLabel.setFont(font)
        self.updatecollegeNameLabel.setObjectName("updatecollegeNameLabel")
        self.updcollegeCodeLine = QtWidgets.QLineEdit(updateCollegeDialog)
        self.updcollegeCodeLine.setGeometry(QtCore.QRect(160, 120, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updcollegeCodeLine.setFont(font)
        self.updcollegeCodeLine.setObjectName("updcollegeCodeLine")
        self.updcollegeNameLine = QtWidgets.QLineEdit(updateCollegeDialog)
        self.updcollegeNameLine.setGeometry(QtCore.QRect(160, 190, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updcollegeNameLine.setFont(font)
        self.updcollegeNameLine.setObjectName("updcollegeNameLine")
        button_style = """
QPushButton {
    background-color: rgb(114, 137, 218);
    color: white;
    border: none;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: rgb(103, 126, 207);
}
QPushButton:pressed {
    background-color: rgb(92, 115, 196);
}
"""
        self.updateCollegeButton = QtWidgets.QPushButton(updateCollegeDialog)
        self.updateCollegeButton.setGeometry(QtCore.QRect(160, 300, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateCollegeButton.setFont(font)
        self.updateCollegeButton.setObjectName("updateCollegeButton")
        self.updateCollegeButton.setStyleSheet(button_style)
        self.collegeCodeLabel_2 = QtWidgets.QLabel(updateCollegeDialog)
        self.collegeCodeLabel_2.setGeometry(QtCore.QRect(100, 30, 271, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.collegeCodeLabel_2.setFont(font)
        self.collegeCodeLabel_2.setObjectName("collegeCodeLabel_2")

        self.retranslateUi(updateCollegeDialog)
        QtCore.QMetaObject.connectSlotsByName(updateCollegeDialog)

    def retranslateUi(self, updateCollegeDialog):
        _translate = QtCore.QCoreApplication.translate
        updateCollegeDialog.setWindowTitle(_translate("updateCollegeDialog", "Update College"))
        self.updatecollegeCodeLabel.setText(_translate("updateCollegeDialog", "COLLEGE CODE:"))
        self.updatecollegeNameLabel.setText(_translate("updateCollegeDialog", "COLLEGE NAME:"))
        self.updateCollegeButton.setText(_translate("updateCollegeDialog", "UPDATE"))
        self.collegeCodeLabel_2.setText(_translate("updateCollegeDialog", "EDIT COLLEGE"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    updateCollegeDialog = QtWidgets.QDialog()
    ui = Ui_updateCollegeDialog()
    ui.setupUi(updateCollegeDialog)
    updateCollegeDialog.show()
    sys.exit(app.exec_())
