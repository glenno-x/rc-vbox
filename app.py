from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem
)
from PyQt5.QtGui import (
    QFont
)
from PyQt5.QtCore import Qt
import subprocess
from configparser import ConfigParser
# Only needed for access to command line arguments
# import sys
from main_window import Ui_MainWindow
from connection_dialog import Ui_ConnectionDialog

CONFIG_FILE = 'rc-vbox.ini'
MONO_FONT = QFont('Arundin Sans Mono', 10)


class ConnectionDialog(QDialog, Ui_ConnectionDialog):
    def __init__(self, parent, default_user, default_machine):
        super().__init__(parent)
        self.setupUi(self)
        self.lineEdit_user.setText(default_user)
        self.lineEdit_machine.setText(default_machine)


class AppMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._cmd_prefix = ''
        self.setupUi(self)
        self.connect_signals_slots()
        # self.model = SettingsModel()
        # self.model = QStandardItemModel(1, 2, self)
        # self.listView_settings.setModel(self.model)
        # self.tableView_settings.setModel(self.model)

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
        self.actionSettings.triggered.connect(self.load_settings)
        self.tableWidget_settings.itemChanged.connect(self.tag_settings)

    def connection_dialog(self):
        r_args = []
        config = ConfigParser()

        # Detect and load config.ini
        try:
            with open(CONFIG_FILE, 'r') as file:
                config.read_file(file)
        except FileNotFoundError:
            config['DEFAULT'] = {'user': '', 'machine': ''}
        config_user = config['DEFAULT']['user']
        config_machine = config['DEFAULT']['machine']

        dialog = ConnectionDialog(self, config_user, config_machine)
        if dialog.exec():
            if dialog.lineEdit_user.text() and dialog.lineEdit_machine.text():
                self.cmd_prefix = dialog.lineEdit_user.text() + '@' + dialog.lineEdit_machine.text()
            else:
                self.cmd_prefix = None

            # Save the connection config
            config['DEFAULT']['user'] = dialog.lineEdit_user.text()
            config['DEFAULT']['machine'] = dialog.lineEdit_machine.text()
            try:
                with open(CONFIG_FILE, 'wt') as file:
                    config.write(file)
            except FileNotFoundError:
                pass

            # Launch the vbox command
            if self.cmd_prefix:
                r_args.extend(['ssh', self.cmd_prefix])
            r_args.extend(['VBoxManage', 'list', 'vms'])
            try:
                result = subprocess.run(r_args, capture_output=True, check=True, text=True)
                vm_dict = {}
                for line in result.stdout.splitlines():
                    items = line.split()
                    if len(items) > 1:
                        # key, value = items
                        # vm_dict[key] = value
                        vm_dict[items[0]] = items[1]
                        self.listWidget.addItem(items[0].strip('"'))    # strip double-quotes
            except subprocess.CalledProcessError as err:
                mbox = QMessageBox(self)
                mbox.setText(err.__str__())
                mbox.setFont(MONO_FONT)
                mbox.exec()

    def get_selected_vm(self):
        # get selected vm
        if self.listWidget.selectedItems():
            selected_vm = self.listWidget.selectedItems()[0].text()
            return selected_vm
        else:
            mbox = QMessageBox(self)
            mbox.setText('No vm selected.')
            mbox.exec()
            return None

    def start_vm(self):
        selected_vm = self.get_selected_vm()
        if not selected_vm:
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
        mbox.setFont(MONO_FONT)
        mbox.exec()

    def stop_vm(self):
        selected_vm = self.get_selected_vm()
        if not selected_vm:
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
        mbox.setFont(MONO_FONT)
        mbox.exec()

    def tag_settings(self, item: QTableWidgetItem):
        item.setForeground(Qt.red)

    def load_settings(self):
        self.tableWidget_settings.itemChanged.disconnect(self.tag_settings)
        selected_vm = self.get_selected_vm()
        if not selected_vm:
            return
        r_args = []
        if self.cmd_prefix:
            r_args.extend(['ssh', self.cmd_prefix])
        r_args.extend(['VBoxManage', 'showvminfo', '--machinereadable', selected_vm])
        try:
            result = subprocess.run(r_args, capture_output=True, check=True, text=True)
            self.tableWidget_settings.clear()
            self.tableWidget_settings.setRowCount(0)
            self.tableWidget_settings.setColumnCount(2)
            for line in result.stdout.splitlines():
                items = line.split('=')
                if len(items) == 2:
                    items[1] = items[1].strip()
                    q_items = [QTableWidgetItem(items[i]) for i in range(2)]
                    q_items[0].setFlags(Qt.ItemIsEditable)
                    # self.model.appendRow(q_items)
                    rows = self.tableWidget_settings.rowCount()
                    self.tableWidget_settings.insertRow(rows)
                    self.tableWidget_settings.setItem(rows, 0, q_items[0])
                    self.tableWidget_settings.setItem(rows, 1, q_items[1])

        except subprocess.CalledProcessError as err:
            mbox = QMessageBox(self)
            mbox.setText(err.__str__())
            mbox.setFont(MONO_FONT)
            mbox.exec()

        self.tableWidget_settings.itemChanged.connect(self.tag_settings)


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
