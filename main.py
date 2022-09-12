import Janela2 as jn
import sys
import pyvisa





#pyqtgraph.examples.run()
app = jn.QtWidgets.QApplication(sys.argv)
MainWindow = jn.QtWidgets.QMainWindow()
ui = jn.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())

