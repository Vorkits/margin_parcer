from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication)
from design import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
from parser_starter import App_view
import multiprocessing

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.btnClicked)
 
 
    def btnClicked(self):
        print((self.ui.comboBox.currentText()))
        fname = QFileDialog.getOpenFileName(self, 'Open file',None, "Table (*.xlsx)")[0]
        name_col=self.ui.spinBox.value()-1
        opt_col=self.ui.spinBox_2.value()-1
        kaspi_margin=self.ui.spinBox_3.value()
        print(fname)
        # f = open(fname, 'r')
        # with f:
        #     data = f.read()
        #     print(data)
        App_view().start_app(fname,kaspi_margin,name_col,opt_col)
if __name__ =='__main__':
    multiprocessing.freeze_support()

    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    
    sys.exit(app.exec())
