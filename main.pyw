import requests
import webbrowser
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

from requests import ConnectTimeout


switches = [
    '10.43.0.150',
    '10.43.0.151',
    '10.43.0.152',
    '10.43.0.153',
]

root = tk.Tk()
root.withdraw()

password = simpledialog.askstring(title='TP-Link admin password',
                                  prompt='Please enter the admin password:',
                                  show='*')

is_warning = False
login_statuses = []

for switch_ip in switches:
    try:
        # check logged in
        response = requests.get(f'http://{switch_ip}', timeout=1)
        if 'logonInfo' not in response.text:
            print(f'Switch {switch_ip} was already logged in.')
            login_statuses.append((switch_ip, 'Already logged in'))
            continue

        # log in
        requests.post(f'http://{switch_ip}/logon.cgi', timeout=1, data={
            'username': 'admin',
            'password': password,
            'cpassword': '',
            'logon': 'Login',
        })

        # check log in
        response = requests.get(f'http://{switch_ip}', timeout=1)
        if 'logonInfo' in response.text:
            print(f'Switch {switch_ip} failed to log in.')
            login_statuses.append((switch_ip, 'Wrong password'))
            is_warning = True
        else:
            print(f'Successfully logged in on switch {switch_ip}')
            login_statuses.append((switch_ip, 'Success'))

    except ConnectTimeout:
        print(f'Connection timeout for {switch_ip}')
        login_statuses.append((switch_ip, 'Connection timeout'))
        is_warning = True

message = '\n'.join([f'{s[0]}: {s[1]}' for s in login_statuses])
if not is_warning:
    messagebox.showinfo('Success', message)
else:
    messagebox.showwarning('Warning', message)

open_browser_tabs = messagebox.askyesno('Open tabs in browser?',
                                        'Do you want to open the GUI interfaces in the webbrowser?')
if open_browser_tabs:
    print('Opening tabs in browser')

    for switch_ip in switches:
        webbrowser.open(f'http://{switch_ip}')
