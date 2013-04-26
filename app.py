#!/usr/bin/env python

import sys
from PyQt4 import QtGui
import sqlite3 as db

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
			print "Error %s:" % e.args[0]

		finally:
			if con:
				con.close()

	def findDay(self, day):
		con = None
		try:
			con = db.connect(self.dbName)
			cur = con.cursor()
			cur.execute("SELECT time,note FROM todo WHERE day=%d" % day)

			data = cur.fetchall()

			while self.results.count() > 0:
				it = self.results.takeItem(0)
				self.results.removeItemWidget(it)

			print len(data), 'rows'
			for i in data:
				print i
				self.results.addItem(i[0] + ' | ' + i[1])

			
			self.results.show()

		except db.Error, e:
			print "Error %s:" % e.args[0]

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

		self.findDay(self.cb.currentIndex())

		self.setGeometry(300, 500, 350, 300)

		self.setWindowTitle('Application');

		self.show()

def main():

	app = QtGui.QApplication(sys.argv)
	ex = Application()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

