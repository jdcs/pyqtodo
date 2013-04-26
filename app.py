#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
import sqlite3 as db
import codecs as cs

DAYS = {
	0: "Mon",
	1: "Tue",
	2: "Wed",
	3: "Thu",
	4: "Fri",
	5: "Sat",
	6: "Sun",
}

class Application(QtGui.QWidget):

	def __init__(self):
		super(Application, self).__init__()

		self.dbName = '.qtodo.db'
		self.initDB()
		self.initUI()

	def initDB(self):
		con = None
		try:
			con = db.connect(self.dbName)
			cur = con.cursor()
			cur.execute('SELECT SQLITE_VERSION()')

			data = cur.fetchone()

			print "SQLite version: %s" % data
		except db.Error, e:
			print "Error '%s'" % e.args[0]
			mbox = QtGui.QMessageBox()
			mbox.critical(self, 'Error', e.args[0])

		finally:
			if con:
				con.close()

	def findDay(self, day):
		con = None
		try:
			con = db.connect(self.dbName)
			cur = con.cursor()
			cur.execute("SELECT h,m,note FROM todo WHERE day=%d" % day)

			data = cur.fetchall()

			while self.results.count() > 0:
				it = self.results.takeItem(0)
				self.results.removeItemWidget(it)

			print len(data), 'rows'
			for i in data:
				print i
				h = str(i[0])
				m = str(i[1])
				note = unicode(i[2])
				if int(i[0]) < 10:
					h = '0' + str(i[0])
				if int(i[1]) < 10:
					m = '0' + str(i[1])
				self.results.addItem(h + ':' + m + ' ' + note)

			
			self.results.show()

		except db.Error, e:
			print "Error '%s'" % e.args[0]
			mbox = QtGui.QMessageBox()
			mbox.critical(self, 'Error', e.args[0])


		finally:
			if con:
				con.close()

	def getDay(self):
		print 'Index:', self.cb.currentIndex()
		self.findDay(self.cb.currentIndex())

	def initUI(self):

		QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

		self.setToolTip('This is a <b>QWidget</b> widget')

		self.cb = QtGui.QComboBox(self)
		self.cb.move(10, 22)
		self.cb.resize(300, 25)

		for k,v in DAYS.items():
			self.cb.insertItem(k, v);

		self.cb.currentIndexChanged.connect(self.getDay)


		self.results = QtGui.QListWidget(self)
		self.results.move(10, 50)
		self.results.resize(300, 200)

		self.results.setStyleSheet("QListWidget::item { color: #0f0; border: 1px solid #0f0; border-radius: 5px; margin-bottom: 1px; background-color: #000; }")

		self.findDay(self.cb.currentIndex())

		gbox = QtGui.QGridLayout()
		gbox.addWidget(self.cb)
		gbox.addWidget(self.results)

		self.setLayout(gbox)

		self.setGeometry(300, 500, 350, 300)

		self.setWindowTitle('Application');

		self.show()

def main():

	app = QtGui.QApplication(sys.argv)
	ex = Application()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

