# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


class SSML:

	def __init__(self):
		self.speak = ET.Element('speak')

	def whisper(self, text):
		e = ET.SubElement(self.speak, 'amazon:effect', {'name' : 'whispered'})
		e.text = unicode(text.decode('utf-8'))
		return self

	def sentence(self, text):
		e = ET.SubElement(self.speak, 's')
		e.text = unicode(text.decode('utf-8'))
		return self

	def pause(self, duration, unit="s"):
		if type(duration) == int:
			duration = str(duration) + unit
		e = ET.SubElement(self.speak, 'break', {"time" : duration})
		return self

	def interjection(self, text):
		e = ET.SubElement(self.speak, 'say-as', {"interpret-as" : "interjection"})
		e.text = unicode(text.decode('utf-8'))
		return self


	def __repr__(self):
		return ET.tostring(self.speak)

	def __str__(self):
		return ET.tostring(self.speak)




if __name__ == '__main__':
	ssml = SSML().sentence("Hallo").whisper("Ich bin dein Vater.").sentence("Überrascht?").interjection("jo").sentence("ok")
	print ssml