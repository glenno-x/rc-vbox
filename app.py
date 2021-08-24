from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow
)
import subprocess
# import sys

# Only needed for access to command line arguments
# import sys

from main_window import Ui_MainWindow
from connecton_dialog import Ui_ConnectionDialog


class ConnectionDialog(QDialog, Ui_ConnectionDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


class AppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._cmd_prefix = ''
        self.setupUi(self)
        self.connect_signals_slots()

    def get_cmd_prefix(self):
        return self._cmd_prefix

    def set_cmd_prefix(self, m_str):
        self._cmd_prefix = m_str

    cmd_prefix = property(get_cmd_prefix, set_cmd_prefix)

    def connect_signals_slots(self):
        self.actionConnect.triggered.connect(self.connection_dialog)
        self.actionE_xit.triggered.connect(self.close)
        '''
        self.action_Find_Replace.triggered.connect(self.findAndReplace)
        self.action_About.triggered.connect(self.about)
        '''

    def connection_dialog(self):
        dialog = ConnectionDialog(self)
        if dialog.exec():
            self.cmd_prefix = dialog.lineEdit_user.text() + '@' + dialog.lineEdit_machine.text()
            # TODO:  Save the user/server pair as config
            r_args = ['ssh', self.cmd_prefix, 'VBoxManage', 'list', 'vms']
            # r2_args = ['lsblk']
            result = subprocess.run(r_args, capture_output=True, text=True)
            print(result.stdout)
            vm_dict = {}
            for line in result.stdout.splitlines():
                items = line.split()
                if len(items) > 1:
                    # key, value = items
                    # vm_dict[key] = value
                    vm_dict[items[0]] = items[1]
                    self.listWidget.addItem(items[0])
            print(vm_dict)


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication([])
app.setApplicationDisplayName('rc-vbox')

# Create a Qt widget, which will be our window.
window = AppMainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()


# Your application won't reach here until you exit and the event
# loop has stopped.
