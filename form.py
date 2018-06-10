from PyQt4.QtCore import *
from PyQt4.QtGui import *


class dialogForm(QDialog):
    def __init__(self, parent=None):
        super(dialogForm, self).__init__(parent)
        self.resize(400,100) # zmniejszamy rozmiar formy
        self.setWindowTitle("probkowanie")
        self.on_ok = None

        comboLayout=QHBoxLayout() #1
        comboLabel=QLabel("Wybierz plik wektorowy") #2
        self.chooseCombo=QComboBox() #3
        comboLabel.setBuddy(self.chooseCombo) #4
        comboLayout.addWidget(comboLabel) #5
        comboLayout.addWidget(self.chooseCombo) #5
        comboLayout.addStretch()
            
        comboLayout_r=QHBoxLayout() #1
        comboLabel_r=QLabel("Wybierz plik rastrowy") #2
        self.chooseCombo_r=QComboBox() #3
        comboLabel_r.setBuddy(self.chooseCombo_r) #4
        comboLayout_r.addWidget(comboLabel_r) #5
        comboLayout_r.addWidget(self.chooseCombo_r)
        comboLayout_r.addStretch()
            
        fieldLayout=QHBoxLayout()
        fieldLabel=QLabel("&Zapisz do pliku")
        self.chooseField=QLineEdit()
        chooseFieldButton=QPushButton("...")
        fieldLabel.setBuddy(self.chooseField)
        fieldLayout.addWidget(fieldLabel) #5
        fieldLayout.addWidget(self.chooseField)
        fieldLayout.addWidget(chooseFieldButton)

        colLayout=QHBoxLayout()
        colLabel=QLabel("Podaj nazwe kolumny:")
        self.column_choose=QLineEdit()
        colLabel.setBuddy(self.column_choose)
        colLayout.addWidget(colLabel)
        colLayout.addWidget(self.column_choose)
        colLayout.addStretch()
                        
        buttonBox = QDialogButtonBox(self)
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        mainLayout=QVBoxLayout()
        mainLayout.addStretch()
        mainLayout.addLayout(comboLayout) #7
        mainLayout.addStretch()
        mainLayout.addLayout(comboLayout_r)
        mainLayout.addStretch()
        mainLayout.addLayout(colLayout)
        mainLayout.addStretch()
        mainLayout.addLayout(fieldLayout)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)



        self.connect(buttonBox, SIGNAL("accepted()"), self.ok)  # 4
        self.connect(buttonBox, SIGNAL("rejected()"), SLOT("reject()"))
        chooseFieldButton.clicked.connect(self.chooseButton_clicked)

    def chooseButton_clicked(self):  # 2A
        filename = QFileDialog. \
            getSaveFileName(self.chooseField, "Select output file ", "", '*.shp')
        self.chooseField.setText(filename)

    def ok(self):
        self.on_ok()
