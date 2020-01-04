import telnetlib
import socket
import requests
import time
from xml.etree import ElementTree
from abc import ABC, abstractmethod

class FNIPOutput:

	def __init__(self, host, port, channel):
	    self._host = host
	    self._port = int(port)
	    self._timeout = 1 # seconds
	    self._channel = int(channel)
	    self._state = None
	    self._updated_time = 0

	def update_state(self, state):
		self._state = state
		self._updated_time = time.time()

	def get_status(self, find):
		if self._updated_time > time.time()-2:
			# Use cached state for 2 seconds
			status = self._state
		else:
			# 2s delay is needed to get state change values ready in status.xml
			response = requests.get("http://" + self._host + "/status.xml")
			tree = ElementTree.fromstring(response.content)
			status = tree.findtext(find, "0")
			self.update_state(status)
		return status

	def send_cmd(self, cmd):
		try:
			tn = telnetlib.Telnet(self._host, self._port, self._timeout)
			tn.write(cmd.encode('ascii') + b"\r\n")
			tn.read_some()
			tn.close()
		except socket.timeout:
			pass		

class FNIPLightsOutput(FNIPOutput):

	@abstractmethod
	def is_on(self):
		status = self.get_status(find)
		return status

	@abstractmethod
	def turn_on(self, state):
		cmd = "FN,ON," + str(self._channel)
		self.send_cmd(cmd)
		self.update_state(1)

	def turn_off(self):
		cmd = "FN,OFF," + str(self._channel)
		self.send_cmd(cmd)
		self.update_state(0)

class FNIP8x10aOutput(FNIPLightsOutput):
	def is_on(self):
		find = "led" + str(int(self._channel)-1)
		status = self.get_status(find)
		return status

	def turn_on(self, state):
		cmd = "FN,ON," + str(self._channel)
		self.send_cmd(cmd)
		self.update_state(1)

class FNIP6x2adOutput(FNIPLightsOutput):
	def is_on(self):
		find = "level" + str(self._channel)
		status = self.get_status(find)
		return status

	def turn_on(self, state):
		cmd = "FN,LEV," + str(self._channel) + "," + str(state)
		self.send_cmd(cmd)
		self.update_state(state)

class FNIP4xshOutput(FNIPOutput):
	_default_max_percentage = 100
	_default_min_percentage = 0

	def set_status(self, status = None):
		if status == None:
			channel_number = str(int(self._channel) - 1) # due to bug in the latest firmware: 1.1.7.
			find = "percent" + channel_number
			status = self.get_status(find)
			self.update_state(status)
		else:
			self.update_state(status)

	def send(self, command, percentage):
		cmd = "FN,"+ str(command) +"," + str(self._channel) + "," + str(percentage)
		self.send_cmd(cmd)
		self.set_status(percentage)			

	def up(self):
		self.send("UP", self._default_max_percentage)

	def down(self):
		self.send("DOWN", self._default_min_percentage)

	def set_percentage(self, percentage):
		self.send("GOTO", percentage)

	def stop(self):
		self.send("STOP", None)
		
