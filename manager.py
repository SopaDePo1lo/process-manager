import math
import os
import pandas as pd
from random import *
import csv
import gettext
import readline

ru = gettext.translation('base', localedir='locales', languages=['ru'])
ru.install()
_ = gettext.gettext


class Manager():

	processes = []
	amount = int
	algorith = ""
	runTime = int
	waitTime = int
	totalTime = 0
	quant = int

	def __init__(self, new_processes=[], amount = None, quant = 4):
		self.amount = amount
		if (new_processes == [] and amount == None):
			self.processes = new_processes
		elif (new_processes==[] and amount!=None):
			for i in range(amount):
				process = Process(i, randint(1, 15))
				# self.totalTime += process.runTime
				self.totalTime = self.totalTime + process.runTime
				self.processes.append(process)
				self.amount = amount
		else:
			self.processes = []
		self.quant = quant
		pass
	
	def saveConfig(self):
		enteredFileName = False
		while (enteredFileName==False):
			fileName = input('Enter file name for config: ')
			files = [f for f in os.listdir('.') if os.path.isfile(f)]
			if (fileName+'.csv') not in files:
				print(f'Saved config file as {fileName}.csv')
				enteredFileName = True
			else:
				print('Config file already exists')
				choice = input('Do you want to replace file: ')
				if (choice.lower()=='yes'):
					print(f'Saved config file as {fileName}.csv')
					enteredFileName = True
				else:
					return
		processesRunTime, processesPriority = [], []
		# processesPriority = []
		for process in self.processes:
			processesRunTime.append(process.runTime)
			processesPriority.append(process.priority)
		config = {'cpu burst' : processesRunTime, 'priority' : processesPriority}
		df = pd.DataFrame(config)
		df.index.name = 'Process'
		df.to_csv(f'{fileName}.csv')

	def loadConfig(self):
		files = [f for f in os.listdir('.') if os.path.isfile(f)]
		for file in files:
			if ('.csv' in file):
				print(f'{file} ')
		file = input('Choose file to load: ')
		try:
			with open(file) as csv_file:
				self.processes = []
				self.amount = 0
				csvReader = csv.reader(csv_file, delimiter=',')
				lineCount = 0
				for row in csvReader:
					if lineCount == 0:
						lineCount+=1
					else:
						print(f'P{row[0]}\t{row[1]}\t{row[2]}')
						lineCount += 1
						self.add(int(row[0]), int(row[1]), int(row[2]))
				self.processes.sort(key=getIndex)
		except (FileNotFoundError):
			print('File not found')

	def add(self, index, runttime, priority):
		self.processes.append(Process(index, runttime, priority))
		self.amount += 1

	def display(self, type="default"):
		if (type == "default"):
			for process in self.processes:
				print(f'P{process.creationIndex}\tCPU Burst = {process.runTime}\tPriority = {process.priority}')
		print(f'\nQuant value = {self.quant}')
	
	def displayFcfs(self):
		print('FCFS')
		waitTime, runTime = 0, 0
		fcfs = self.fcfs()
		for line in range(len(fcfs)):
			print(f'P{self.processes[line].creationIndex}\t' + fcfs[line])
			waitTime += self.processes[line].waitTime
			runTime += self.processes[line].runTime + self.processes[line].waitTime
		print()
		for line in range(len(fcfs)):
			print(f'P{self.processes[line].creationIndex}\tWait time = {self.processes[line].waitTime}; Run time = {self.processes[line].runTime + self.processes[line].waitTime}')
		print(f'Average wait time = {round(waitTime/self.amount, 2)}; Average run time = {round(runTime/self.amount, 2)}')

	def displaySjf(self):
		print('''SJF''')
		waitTime, runTime = 0, 0
		sjf = self.sjf()
		for line in range(len(sjf)):
			waitTime += self.processes[line].waitTime
			runTime += self.processes[line].runTime + self.processes[line].waitTime
			print(f'P{self.processes[line].creationIndex}\t' + sjf[line])
		print()
		for line in range(len(sjf)):
			print(f'P{self.processes[line].creationIndex}\tWait time = {self.processes[line].waitTime}; Run time = {self.processes[line].runTime + self.processes[line].waitTime}')
		print(f'Average wait time = {round(waitTime/self.amount, 2)}; Average run time = {round(runTime/self.amount, 2)}')

	def getTotalRunTime(self):
		totalRunTime = 0
		for process in self.processes:
			totalRunTime += process.runTime
		return totalRunTime

	def getMaxRunTime(self):
		maxTime = 0
		for process in self.processes:
			if (process.runTime > maxTime):
				maxTime = process.runTime
		return maxTime

	def displayRRfcfs(self):
		print('''RR FCFS''')
		self.rrFcfs(True)
		print(f'Single quant = {self.quant}')

	def displayRRsjf(self):
		print('''RR SJF''')
		self.rrSjf(True)
		print(f'Single quant = {self.quant}')

	def displayRRpriority(self):
		print('''RR Priority''')
		self.rrPriority(True)
		print(f'Single quant = {self.quant}')

	def optimizeQuantTime(self, algorith):
		originalQuant = self.quant
		minQuant = 1
		maxQuant = int(self.getMaxRunTime()/2)
		currentWaitTime = 10000000
		if (algorith == 'fcfs'):
			for i in range(1, maxQuant):
				self.quant = i
				waitTime = self.rrFcfs()
				if (currentWaitTime > waitTime):
					currentWaitTime = self.rrFcfs()
					minQuant = i
			self.quant = minQuant
			return minQuant, currentWaitTime
		elif (algorith == 'sjf'):
			for i in range(1, maxQuant):
				self.quant = i
				waitTime = self.rrSjf()
				if (currentWaitTime > waitTime):
					currentWaitTime = self.rrSjf()
					minQuant = i
			self.quant = minQuant
			return minQuant, currentWaitTime
		else:
			self.quant = originalQuant

	def fcfs(self):
		self.totalTime = self.getTotalRunTime()
		line = []
		for i in range(self.amount):
			line.append('')
		timePassed = 0
		self.calculateWaitTime("default")
		for process in self.processes:
			process.executeTime = process.waitTime+process.runTime
			line[process.creationIndex] = process.waitTime*"-" + process.runTime*"+"+(self.totalTime-process.waitTime-process.runTime)*"-"
			# print(line[process.creationIndex] + f"process ran for {process.executeTime}; waited for {process.waitTime}")
			# print(line[process.creationIndex])
			timePassed += process.runTime
		return line

	def prioritySort(self):
		self.totalTime = self.getTotalRunTime()
		line = []
		for i in range(self.amount):
			line.append('')
		timePassed = 0
		self.calculateWaitTime("prio")
		self.processes.sort(key=getIndex)
		for process in self.processes:
			process.executeTime = process.waitTime+process.runTime
			line[process.creationIndex] = process.waitTime*"-" + process.runTime*"+"+(self.totalTime-process.waitTime-process.runTime)*"-"
			# print(line[process.creationIndex] + f"process ran for {process.executeTime}; waited for {process.waitTime}")
			timePassed += process.runTime
		return line

	def displayPriority(self):
		print('''Priority''')
		waitTime, runTime = 0, 0
		prio = self.prioritySort()
		for line in range(len(prio)):
			waitTime += self.processes[line].waitTime
			runTime += self.processes[line].runTime + self.processes[line].waitTime
			print(f'P{self.processes[line].creationIndex}\t' + prio[line])
		print()
		for line in range(len(prio)):
			print(f'P{self.processes[line].creationIndex}\tWait time = {self.processes[line].waitTime}; Run time = {self.processes[line].runTime + self.processes[line].waitTime}; Priority = {self.processes[line].priority}')
		print(f'Average wait time = {round(waitTime/self.amount, 2)}; Average run time = {round(runTime/self.amount, 2)}')

	def sjf(self):
		self.totalTime = self.getTotalRunTime()
		line = []
		for i in range(self.amount):
			line.append('')
		timePassed = 0
		self.calculateWaitTime("sjf")
		self.processes.sort(key=getIndex)
		for process in self.processes:
			process.executeTime = process.waitTime+process.runTime
			line[process.creationIndex] = process.waitTime*"-" + process.runTime*"+"+(self.totalTime-process.waitTime-process.runTime)*"-"
			# print(line[process.creationIndex] + f"process ran for {process.executeTime}; waited for {process.waitTime}")
			timePassed += process.runTime
		return line

	def rrPriority(self, display = False):
		processesFinished = 0
		timePassed = 0
		procs = []
		self.calculateWaitTime("prio")
		self.processes.sort(key=getPriority)
		for i in range(self.amount):
			procs.append("")
		while processesFinished < self.amount+10:
			for process in self.processes:
				if (self.quant > (process.runTime-process.alreadyRan)):
					procs[process.creationIndex] += (timePassed-len(procs[process.creationIndex]))*"-" + (process.runTime-process.alreadyRan)*"+"
					timePassed += (process.runTime-process.alreadyRan)
					process.alreadyRan += (process.runTime-process.alreadyRan)
				elif (self.quant <=  (process.runTime-process.alreadyRan)):
					procs[process.creationIndex] += (timePassed-len(procs[process.creationIndex]))*"-" + self.quant*"+"
					timePassed += self.quant
					process.alreadyRan += self.quant
				if (process.alreadyRan >= process.runTime):
					processesFinished += 1
			pass
		totalWaitTime, totalRunTime = 0, 0
		for i in range(self.amount):
			totalWaitTime += self.counter(procs[i])
			totalRunTime += self.counter(procs[i]) + procs[i].count("+")
			if len(procs[i])<self.getTotalRunTime():
				procs[i] += '-'*(self.getTotalRunTime()-len(procs[i]))
			if (display == True):
				print(f'P{i}\t'+ procs[i])
		if (display == True):
			print()
		for i in range(self.amount):
			if (display == True):
				print(f'P{i}\tWait time = {self.counter(procs[i])}; Run time = {self.counter(procs[i]) + procs[i].count("+")}')
		for process in self.processes:
			process.alreadyRan = 0
		if (display == True):
			print(f'Average wait time = {round(totalWaitTime/self.amount, 2)}; Average run time = {round(totalRunTime/self.amount, 2)}')
		self.processes.sort(key=getIndex)
		return round(totalWaitTime/self.amount, 2)


	def rrSjf(self, display = False):
		processesFinished = 0
		timePassed = 0
		procs = []
		self.calculateWaitTime("sjf")
		self.processes.sort(key=getRunTime)
		for i in range(self.amount):
			procs.append("")
		while processesFinished < self.amount+10:
			for process in self.processes:
				if (self.quant > (process.runTime-process.alreadyRan)):
					procs[process.creationIndex] += (timePassed-len(procs[process.creationIndex]))*"-" + (process.runTime-process.alreadyRan)*"+"
					timePassed += (process.runTime-process.alreadyRan)
					process.alreadyRan += (process.runTime-process.alreadyRan)
				elif (self.quant <=  (process.runTime-process.alreadyRan)):
					procs[process.creationIndex] += (timePassed-len(procs[process.creationIndex]))*"-" + self.quant*"+"
					timePassed += self.quant
					process.alreadyRan += self.quant
				if (process.alreadyRan >= process.runTime):
					processesFinished += 1
			pass
		totalWaitTime, totalRunTime = 0, 0
		for i in range(self.amount):
			totalWaitTime += self.counter(procs[i])
			totalRunTime += self.counter(procs[i]) + procs[i].count("+")
			if len(procs[i])<self.getTotalRunTime():
				procs[i] += '-'*(self.getTotalRunTime()-len(procs[i]))
			if (display == True):
				print(f'P{i}\t'+ procs[i])
		if (display == True):
			print()
		for i in range(self.amount):
			if (display == True):
				print(f'P{i}\tWait time = {self.counter(procs[i])}; Run time = {self.counter(procs[i]) + procs[i].count("+")}')
		for process in self.processes:
			process.alreadyRan = 0
		if (display == True):
			print(f'Average wait time = {round(totalWaitTime/self.amount, 2)}; Average run time = {round(totalRunTime/self.amount, 2)}')
		self.processes.sort(key=getIndex)
		return round(totalWaitTime/self.amount, 2)

	def rrFcfs(self, display = False):
		processesFinished = 0
		timePassed = 0
		procs = []
		for i in range(self.amount):
			procs.append("")
		while processesFinished < self.amount+10:
			for process in self.processes:
				if (self.quant > (process.runTime-process.alreadyRan)):
					procs[process.creationIndex] += (timePassed-len(procs[process.creationIndex]))*"-" + (process.runTime-process.alreadyRan)*"+"
					timePassed += (process.runTime-process.alreadyRan)
					process.alreadyRan += (process.runTime-process.alreadyRan)
				elif (self.quant <=  (process.runTime-process.alreadyRan)):
					procs[process.creationIndex] += (timePassed-len(procs[process.creationIndex]))*"-" + self.quant*"+"
					timePassed += self.quant
					process.alreadyRan += self.quant
				if (process.alreadyRan >= process.runTime):
					processesFinished += 1
			pass
		totalWaitTime, totalRunTime = 0, 0
		for i in range(self.amount):
			totalWaitTime += self.counter(procs[i])
			totalRunTime += self.counter(procs[i]) + procs[i].count("+")
			if len(procs[i])<self.getTotalRunTime():
				procs[i] += '-'*(self.getTotalRunTime()-len(procs[i]))
			if (display == True):
				print(f'P{i}\t'+ procs[i])
		if (display == True):
			print()
		for i in range(self.amount):
			if (display == True):
				print(f'P{i}\tWait time = {self.counter(procs[i])}; Run time = {self.counter(procs[i]) + procs[i].count("+")}')
		for process in self.processes:
			process.alreadyRan = 0
		if (display == True):
			print(f'Average wait time = {round(totalWaitTime/self.amount, 2)}; Average run time = {round(totalRunTime/self.amount, 2)}')
		return round(totalWaitTime/self.amount, 2)

	def counter(self, line):
		line = line[0:line.rfind("+")]
		return line.count("-")

	def calculateWaitTime(self, type="default", rr = False):
		timePassed = 0
		if (type == "default" and rr==False):
			for process in self.processes:
				process.waitTime = timePassed
				timePassed+=process.runTime
		elif (type == "sjf" and rr==False):
			self.processes.sort(key=getRunTime)
			for process in self.processes:
				process.waitTime = timePassed
				timePassed+=process.runTime
		elif (type == 'prio' and rr==False):
			self.processes.sort(key=getPriority)
			for process in self.processes:
				process.waitTime = timePassed
				timePassed+=process.runTime

class Process():

	creationIndex = int
	runTime = int
	waitTime = int
	executeTime = int
	alreadyRan = 0
	finished = False
	priority = int
	maxTime = 15
	minTime = 1

	def __init__(self, creationIndex = None, runTime = None, priority=None, time=(1,15)):
		minTime, maxTime = time
		if (runTime==None):
			self.runTime = randint(minTime, maxTime)
		else:
			self.runTime = runTime
		self.creationIndex = creationIndex
		if (priority==None):
			self.priority = randint(-20, 20)
		else:
			self.priority = priority
		pass

def getRunTime(process):
	return process.runTime

def getPriority(process):
	return process.priority

def getIndex(process):
	return process.creationIndex