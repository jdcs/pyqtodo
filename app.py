#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from string import join
from PyQt4.QtCore import Qt
import sqlite3 as db
from popen2 import popen2 as ps

DAYS = {
	0: "Sun",
	1: "Mon",
	2: "Tue",
	3: "Wed",
	4: "Thu",
	5: "Fri",
	6: "Sat",
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
		print 'list day:', day
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

	def delRow(self):
		if len(self.results.selectedItems()):
			it = self.results.selectedItems()[0]
			i = self.results.row(it)
			it = self.results.takeItem(i)
			text = unicode(it.text())
			hm = text.split(' ')[0]
			d = int(self.cb.currentIndex())
			n = join(unicode(text).split(' ')[1:])
			h = int(hm.split(':')[0])
			m = int(hm.split(':')[1])
			print d, h, m, n
			self.deleteRow(d, h, m, n)
			self.results.removeItemWidget(it)


	def edRow(self):
		text = ''
		it = 0
		if len(self.results.selectedItems()):
			it = self.results.selectedItems()[0]
			i = self.results.row(it)
			it = self.results.takeItem(i)
			text = unicode(it.text())
		else:
			return
		self.ib.setHidden(False)
		self.ib.setText(text)
		self.results.removeItemWidget(it)
		hm = text.split(' ')[0]
		d = int(self.cb.currentIndex())
		n = join(unicode(text).split(' ')[1:])
		h = int(hm.split(':')[0])
		m = int(hm.split(':')[1])
		self.deleteRow(d, h, m, n)

	def butsHide(self):
		if not self.bt.isHidden():
			self.btDel.setHidden(True)
			self.btEd.setHidden(True)
			self.bt.setHidden(True)
			self.btHide.setText("v")
			self.btHide.setToolTip("Expand toolbar")
		else:
			self.btDel.setHidden(False)
			self.btEd.setHidden(False)
			self.bt.setHidden(False)
			self.btHide.setText("^")
			self.btHide.setToolTip("Hide toolbar")

	def addRow(self):
		if not self.ib.isHidden():
			self.getInp()
			self.ib.setHidden(True)
			return
		self.ib.setHidden(False)
		self.ib.setText('Enter task here in "h:m some task" format')

	def getInp(self):
		text = unicode(self.ib.text())
		hm = text.split(' ')[0]
		d = int(self.cb.currentIndex())
		n = join(unicode(text).split(' ')[1:])
		h = int(hm.split(':')[0])
		m = int(hm.split(':')[1])
		print d, h, m, n
		self.insertRow(d, h, m, n)
		self.findDay(self.cb.currentIndex())
		self.ib.setHidden(True)

	def deleteRow(self, day, h, m, note):
		try:
			con = db.connect(self.dbName)
			cur = con.cursor()
			cur.execute("DELETE FROM todo WHERE		\
					day=%d AND h=%d			\
					AND m=%d AND note='%s';"	\
					% (day,h,m,note))
			con.commit()

		except db.Error, e:
                        print "Error '%s'" % e.args[0]
                        mbox = QtGui.QMessageBox()
                        mbox.critical(self, 'Error', e.args[0])
                finally:
                        if con:
                                con.close()

	def insertRow(self, d, h, m, n):
		try:
			con = db.connect(self.dbName)
			cur = con.cursor()
			cur.execute("INSERT into todo(day,h,m,note) VALUES \
					(%d, %d, %d, '%s');" % (d, h, m, n))
			con.commit()

		except db.Error, e:
                        print "Error '%s'" % e.args[0]                         
                        mbox = QtGui.QMessageBox()                             
                        mbox.critical(self, 'Error', e.args[0])                
                                                                               
                finally:
                        if con:
                                con.close()

	def initUI(self):

		try:
			self.setAttribute(Qt.WA_Maemo5AutoOrientation, True)
		except AttributeError, e:
			print 'Platform is not Maemo:', e.args[0]

		self.cb = QtGui.QComboBox(self)
		self.cb.setStyleSheet("QComboBox { font-size: 22pt; }")

		for k,v in DAYS.items():
			self.cb.insertItem(k, v);

		self.cb.currentIndexChanged.connect(self.getDay)

		self.bt = QtGui.QPushButton(self)
		self.bt.setStyleSheet("QPushButton { font-size: 32pt; height: 30px; font-weight: bold; }")
		self.bt.setText("+")
		self.bt.setToolTip("Add")
		self.bt.clicked.connect(self.addRow)

		self.btEd = QtGui.QPushButton(self)
		self.btEd.setStyleSheet("QPushButton { font-size: 15pt; height: 30px; font-weight: bold; }")
		self.btEd.setText("\\")
		self.btEd.setToolTip("Edit")
		self.btEd.clicked.connect(self.edRow)


		self.btDel = QtGui.QPushButton(self)
		self.btDel.setStyleSheet("QPushButton { font-size: 32pt; height: 30px; font-weight: bold; }")
		self.btDel.setText("-")
		self.btDel.setToolTip("Delete")
		self.btDel.clicked.connect(self.delRow)

		self.ib = QtGui.QLineEdit(self)
		self.ib.setHidden(True)
		self.ib.returnPressed.connect(self.getInp)

		self.btHide = QtGui.QPushButton(self)
		self.btHide.setText("^")
		self.btHide.setToolTip("Hide toolbar")
		self.btHide.setStyleSheet("QPushButton { font-size: 12pt; height: 15px; font-weight: bold; padding-top: 5px; }")
		self.btHide.clicked.connect(self.butsHide)

		self.results = QtGui.QListWidget(self)

		d = ps('date +%w')[0].read()
		d = int(d[:1])
		self.findDay(d)
		self.cb.setCurrentIndex(d)

		self.gbox = QtGui.QGridLayout(self)

		self.gbox.addWidget(self.cb)
		self.gbox.addWidget(self.bt)
		self.gbox.addWidget(self.btEd)
		self.gbox.addWidget(self.btDel)
		self.gbox.addWidget(self.btHide)
		self.gbox.addWidget(self.ib)

		self.gbox.addWidget(self.results)

		self.setLayout(self.gbox)

		self.setGeometry(300, 500, 350, 300)

		self.setWindowTitle('PyQtodo');

		self.show()

def main():

	app = QtGui.QApplication(sys.argv)
	ex = Application()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

