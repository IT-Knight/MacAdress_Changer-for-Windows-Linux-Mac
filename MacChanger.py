# Копируем в .py файл

"""
Windows:
    - открываем cmd с правами админа
    - вводим: python change_macV5.py -i [имя адаптера] -m [МАС-адресс]
Linux:
    - открываем терминал
    - вводим: sudo python3 change_macV5.py -i [имя адаптера] -m [МАС-адресс]

Доп. инфо:
    - флаг -i [имя адаптера], например -i Ethernet, -i ens33, -i eth0
    - флаг -m [МАС-адресс]:
        - для windows в формате: 00-00-00-00-00-00 или 000000000000
        - для линукс в формате: 00:00:00:00:00:00
    - флаг --help - для вывода помощи
"""

from subprocess import run, PIPE
import subprocess
import optparse
import re
import os



class MacChangerLinux:

    def __init__(self):
        self.options = self.get_arguments() 
        self.basic_mac = self.get_mac()
        self.main_process(self.options)

    def main_process(self, options):
        print('Current MAC = ' + self.basic_mac)
        self.change_mac(options.interface, options.new_mac)  
        current_mac = self.get_mac()
        if current_mac == self.basic_mac:
            print('[-] MAC address did not get changed.')
        else:
            print('[+] MAC address was succesfully changed to', current_mac)
        

    def get_mac(self):
        return re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', subprocess.check_output(['ifconfig', self.options.interface]).decode()).group(0)


    def change_mac(self, interface, new_mac):
        print("[+] Changing MAC address for", interface, 'to', new_mac)
        subprocess.call(['sudo', 'ifconfig', interface, 'down'])
        subprocess.call(['sudo' ,'ifconfig', interface, 'hw', 'ether', new_mac])
        subprocess.call(['sudo','ifconfig', interface, 'up'])
        

    def get_arguments(self):
        parser = optparse.OptionParser()
        parser.add_option('-i', '--interface', dest='interface', help='Interface Name to change its MAC adress.                     Get the Name by command "ifconfig"')
        parser.add_option('-m', '--mac', dest='new_mac', help='New MAC address format 00:00:00:00:00:00')
        options, arguments = parser.parse_args()
        if not options.interface:
            parser.error('[-] Please specify an inteface, use --help for more info.')
        elif not options.new_mac:
            parser.error('[-] Please specify new mac, use --help for more info.')
        return options



class MacChangerWindows:

    def __init__(self):
        basic_mac = self.get_current_mac()
        interface, new_mac = self.get_arguments()
        print('\nCurrent MAC..................: ' + basic_mac)
        self.change_mac(interface, new_mac)
        after_mac = self.get_current_mac()
        if after_mac == basic_mac:
            print('\n[-] MAC address did not changed.')
        else:
            print('\n\n[+] MAC address was succesfully changed to', after_mac)


    def get_arguments(self):
        parser = optparse.OptionParser()
        parser.add_option('-i', '--interface', dest='interface', help='Interface Name to change its MAC adress.                 Get the Name by "netsh inteface show interface" or                "powershell -command "Get-NetAdapter | format-list"')
        parser.add_option('-m', '--mac', dest='new_mac', help='New MAC address in format: 00-00-00-00-00-00')
        options, arguments = parser.parse_args()
        if not options.interface:
            parser.error('[-] Please specify an inteface, use --help for more info.')
        elif not options.new_mac:
            parser.error('[-] Please specify new mac, use --help for more info.')
        return (options.interface, options.new_mac)

    def get_current_mac(self):
        return re.findall(r'\w\w-\w\w-\w\w-\w\w-\w\w-\w\w', run('ipconfig /all', shell=True, stdout=PIPE).stdout.decode('cp866'))[0]


    def change_mac(self, interface, new_mac):
        print('\nChanging MAC address for', interface, 'to............:', new_mac)
        print("\nIt may take about munite, please wait. Do not press any key and do not input nothing.")
        subprocess.run(["powershell.exe", '-command', f'Set-NetAdapter -Name {interface} -MacAddress {new_mac}'], input='y', text=True)



if os.name == 'nt':
    MacChangerWindows()
elif os.name == 'posix':
    MacChangerLinux()

