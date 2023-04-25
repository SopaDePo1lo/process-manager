from manager import *
import gettext
import os
import readline
# from random import *

# pygettext.py -d base -o locales/base.pot src/main.py
# msgfmt.py -o base.mo base

#VARIABLES
ru = gettext.translation('base', localedir='locales', languages=['ru'])
es = gettext.translation('base', localedir='locales', languages=['es'])
uz = gettext.translation('base', localedir='locales', languages=['uz'])
uz.install()
ru.install()
es.install()
# _ = gettext.gettext
_ = ru.gettext

running = True
processManager = None
processManagerMade = False

# languageLocalization = 'ru'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#FUNCTIONS

def helpinfo():
    print(_('help - displays all commands\ninfo - outputs info of all the current processes\ncreate - create a process manager\nadd - add a new process to ProcessManager\nsetQuant - set the quant value\nfcfs - runs FCFS algorithm for ProcessManager\nsjf - runs SJF algorithm for ProcessManager\nrrFcfs - runs RR FCFS algorithm for ProcessManager\nrrSjf - runs RR SJF algorithm for ProcessManager\nexit - exits app\nclear - clear terminal\nedit - edit processes\nlanguage - change language'))

def processManagerNotMade():
    print(_("You must create a ProcessManager first"))

def remove():
    pass
    # processManager = Manager([], 0)
    # processManagerMade = False

def setLanguage():
    global _
    lc = input(_("Enter preferred language(ru, en): "))
    if (lc.lower()=='ru'):
        _ = ru.gettext
    elif (lc.lower()=='es'):
        _ = es.gettext
    elif (lc.lower() == 'uz'):
        _ = uz.gettext
    else:
        _ = gettext.gettext

def info():
    if (processManagerMade):
        processManager.display()
    else:
        processManagerNotMade()

def create():
    global processManagerMade
    global processManager
    try:
        amount =  int(input(_("Enter amount of processes: ")))
        quant = input(_("Enter value of quant: "))
        if (quant == ''):
            quant = 4
        processManager = Manager([], amount)
        processManager.quant = int(quant)
        processManagerMade = True
    except (ValueError):
        pass

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def setquant():
    if (processManagerMade):
        quant = int(input(_("Enter value of quant: ")))
        processManager.quant = quant
    else:
        processManagerNotMade()

def fcfs():
    if (processManagerMade):
        processManager.displayFcfs()
    else:
        processManagerNotMade()

def sjf():
    if (processManagerMade):
        processManager.displaySjf()
    else:
        processManagerNotMade()

def rrfcfs():
    if (processManagerMade):
        processManager.displayRRfcfs()
    else:
        processManagerNotMade()

def rrsjf():
    if (processManagerMade):
        processManager.displayRRsjf()
    else:
        processManagerNotMade()

def rrPriority():
    if (processManagerMade):
        processManager.displayRRpriority()
    else:
        processManagerNotMade()

def priority():
    if (processManagerMade):
        processManager.displayPriority()
    else:
        processManagerNotMade()

def exit():
    global running
    running = False

def saveConfig():
    if (processManagerMade):
        processManager.saveConfig()
    else:
        processManagerNotMade()

def loadConfig():
    global processManagerMade
    global processManager
    if (processManagerMade):
        processManager.loadConfig()
    else:
        processManager = Manager([], 0)
        processManagerMade = True
        processManager.loadConfig()
        # processManagerNotMade()

def configs():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if ('.csv' in file):
            print(f'{file} ')

def readConfig():
    file = input(_('Enter config file name: '))
    try:
        with open(file) as csv_file:
            csvReader = csv.reader(csv_file, delimiter=',')
            lineCount = 0
            for row in csvReader:
                if lineCount == 0:
                    lineCount+=1
                else:
                    print(f'P{row[0]}\t{row[1]}\t{row[2]}')
                    lineCount += 1
    except (FileNotFoundError):
        print(_('File not found'))

def edit():
    try:
        pId = int(input(_('Enter process id: '))) 
        if (pId > len(processManager.processes)-1):
            print(_('Cant find a process with that index'))
            return
        newRunTime = int(input(_('Enter CPU Burst: ')))
        newPriority = (input(_('Enter process priority: ')))
        if (newPriority != ''):
            processManager.processes[pId].priority = int(newPriority)
        processManager.processes[pId].runTime = newRunTime
    except(ValueError):
        pass

def add():
    pRunTime = input(_('Enter CPU Burts (leave empty for random): '))
    pPriority = input(_('Enter process priority (leave empty for random): '))
    if (pRunTime == ''):
        pRunTime = randint(1, 15)
    if (pPriority == ''):
        pPriority = randint(-20, 20)
    processManager.add(processManager.amount, int(pRunTime), int(pPriority))

def optimize():
    fcfsQuant, waitTimeFcfs = processManager.optimizeQuantTime("fcfs")
    sjfQuant, waitTimeSjf = processManager.optimizeQuantTime("sjf")
    print(_(f'Best quant for FCFS is {fcfsQuant} with a average wait time of {waitTimeFcfs}\nBest quant for SJF is {sjfQuant} with a average wait time of {waitTimeSjf}\nQuant set to {sjfQuant}'))

functions = {'help':helpinfo, 'info':info, 'setquant':setquant, 'fcfs':fcfs, 'sjf':sjf,
 'rrfcfs':rrfcfs, 'rrsjf':rrsjf, 'exit':exit, 'optimize':optimize, 'clear':clear, 'create':create,
 'saveconfig':saveConfig, 'loadconfig':loadConfig, 'add':add, 'edit':edit, 'configs':configs, 'readconfig':readConfig,
 'priority' : priority, 'rrpriority': rrPriority, 'language' : setLanguage, 'remove' : remove}

clear()
while running:
    try:
        command = input(f'{bcolors.OKCYAN}~/process-manager{bcolors.BOLD}{bcolors.HEADER}${bcolors.ENDC} ')
        if command.lower() not in functions:
            functions['help']()
        else:
            functions[command.lower()]()
    except (KeyboardInterrupt):
        print(_('Exiting programm'))
        exit()
    pass
