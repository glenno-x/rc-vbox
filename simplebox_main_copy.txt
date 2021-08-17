import PySimpleGUI as sg
from configparser import ConfigParser
'''

    SimpleRemoteVbox - A PySimpleGUI app to manage settings of remote Vbox virtual machines.

'''
FILENAME = 'opensuse.showvminfo.machinereadable'
config = ConfigParser()

with open(FILENAME) as stream:
    config.read_string("[DEFAULT]\n" + stream.read())  # insert missing [DEFAULT] section heading


# with open(FILENAME + '.out', 'w') as fw:
#     config.write(fw)


def create_form(fconfig):
    vlist = []
    subconfig = fconfig[fconfig.default_section]
    for key in subconfig:
        # print(key, subconfig[key])
        vlist.append([sg.Text(key), sg.Input(default_text=subconfig[key], key=key)])
    return vlist


sg.theme('BluePurple')
layout = [[sg.Text('Settings:')],
          create_form(config),
          [sg.Button('Change'), sg.Button('Exit')]]

window = sg.Window('Virtual_Machine', layout)

while True:  # Event Loop
    event, values = window.read()
    # print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Change':
        pass
        # Update the "output" text element to be the value of "input" element
        # window['-OUTPUT-'].update(values['-IN-'])

window.close()
