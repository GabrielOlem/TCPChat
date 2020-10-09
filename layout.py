import PySimpleGUI as sg

class Screen:
    def __init__(self):
        sg.theme('DarkBrown1')
        layout = [
            [sg.Text('Name'), sg.Input('')],
            [sg.Output(size=(80,20))],
            [sg.Text('Message:'), sg.Input(do_not_clear = False), sg.Button('Send message'), sg.Button('Exit')]
        ]
        self.screen = sg.Window("Chat", layout, return_keyboard_events = True);

    def start(self):
        while 1:
            event, values = self.screen.Read()
            if event == 'Send message':
                if values[0] == '' or values[1] == '':
                    warning = 'You must have a name!' if values[0] == '' else 'Invalid input'
                    sg.popup(warning)
                else:
                    print(f'{values[0]}: {values[1]}')
                    values[1] = ''
            elif event =='Exit' or event == sg.WIN_CLOSED:
                break
        self.screen.close()

UI = Screen()
UI.start()
