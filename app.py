from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
import subprocess
from configparser import ConfigParser
# Only needed for access to command line arguments
# import sys
from main_window import Ui_MainWindow
from connection_dialog import Ui_ConnectionDialog

CONFIG_FILE = 'rc-vbox.ini'


class ConnectionDialog(QDialog, Ui_ConnectionDialog):
    def __init__(self, parent, default_user, default_machine):
        super().__init__(parent)
        self.setupUi(self)
        self.lineEdit_user.setPlaceholderText(default_user)
        self.lineEdit_machine.setPlaceholderText(default_machine)


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
        self.actionStart.triggered.connect(self.start_vm)
        self.actionStop.triggered.connect(self.stop_vm)
        '''
        self.action_Find_Replace.triggered.connect(self.findAndReplace)
        self.action_About.triggered.connect(self.about)
        '''

    def connection_dialog(self):
        r_args = []
        config = ConfigParser()

        # Detect and load config.ini
        try:
            with open(CONFIG_FILE) as file:
                config.read(file)
        except FileNotFoundError:
            pass
        if not ('connection' in config):
            config['connection'] = {'user': '', 'machine': ''}
        sub_config = config['connection']
        config_user = sub_config['user']
        config_machine = sub_config['machine']

        dialog = ConnectionDialog(self, config_user, config_machine)
        if dialog.exec():
            if dialog.lineEdit_user.text() and dialog.lineEdit_machine.text():
                self.cmd_prefix = dialog.lineEdit_user.text() + '@' + dialog.lineEdit_machine.text()
            else:
                self.cmd_prefix = None

            # Save the connection config
            config['connection']['user'] = dialog.lineEdit_user.text()
            config['connection']['machine'] = dialog.lineEdit_machine.text()
            try:
                with open(CONFIG_FILE, 'wt') as file:
                    config.write(file)
            except FileNotFoundError:
                pass

            # Launch the vbox command
            if self.cmd_prefix:
                r_args.extend(['ssh', self.cmd_prefix])
            r_args.extend(['VBoxManage', 'list', 'vms'])
            result = subprocess.run(r_args, capture_output=True, text=True)
            vm_dict = {}
            for line in result.stdout.splitlines():
                items = line.split()
                if len(items) > 1:
                    # key, value = items
                    # vm_dict[key] = value
                    vm_dict[items[0]] = items[1]
                    self.listWidget.addItem(items[0].strip('"'))    # strip double-quotes

    def start_vm(self):
        # get selected vm
        if self.listWidget.selectedItems():
            selected_vm = self.listWidget.selectedItems()[0].text()
        else:
            mbox = QMessageBox(self)
            mbox.setText('No vm selected.')
            mbox.exec()
            return
        r_args = []
        options = []
        if self.cmd_prefix:
            r_args.extend(['ssh', self.cmd_prefix])
            options = ['--type', 'headless']
        r_args.extend(['VBoxManage', 'startvm', selected_vm])
        if options:
            r_args.extend(options)
        # print(r_args)
        mbox = QMessageBox(self)
        try:
            result = subprocess.run(r_args, capture_output=True, check=True, text=True, timeout=30)
            mbox.setText(result.stdout)
        except subprocess.CalledProcessError as err:
            mbox.setText(err.__str__())
        mbox.exec()

    def stop_vm(self):
        # get selected vm
        if self.listWidget.selectedItems():
            selected_vm = self.listWidget.selectedItems()[0].text()
        else:
            mbox = QMessageBox(self)
            mbox.setText('No vm selected.')
            mbox.exec()
            return
        r_args = []
        if self.cmd_prefix:
            r_args.extend(['ssh', self.cmd_prefix])
        r_args.extend(['VBoxManage', 'controlvm', selected_vm, 'poweroff'])
        mbox = QMessageBox(self)
        try:
            result = subprocess.run(r_args, capture_output=True, check=True, text=True, timeout=30)
            mbox.setText(result.stdout + '\n' + result.stderr + '\n' + selected_vm + ' stopped.')
        except subprocess.CalledProcessError as err:
            mbox.setText(err.__str__())
        mbox.exec()


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication([])
app.setApplicationDisplayName('rc-vbox')

# Create a Qt widget, which will be our window.
window = AppMainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
