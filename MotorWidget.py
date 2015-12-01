import sys
import re
from signal import signal, SIGINT, SIG_DFL

from taurus.qt.qtgui.application import TaurusApplication
from manipulatorgui.MainWindow import MainWindow
from taurus.external.qt import uic
from taurus.external.qt.QtGui import QWidget
from taurus.external.qt.QtCore import SIGNAL
from PyTango import DeviceProxy, AttributeProxy


class MotorWidget(QWidget):
	def __init__(self, model, parent=None):
		QWidget.__init__(self, parent)
		uic.loadUi("MotorWidget.ui", self)

		self.connect(self.configButton, SIGNAL("clicked()"), self.openConfig)
		self.connect(self.goButton, SIGNAL("clicked()"), self.go)
		self.connect(self.moveNegButton, SIGNAL("clicked()"), self.moveNeg)
		self.connect(self.movePosButton, SIGNAL("clicked()"), self.movePos)
		self.connect(self.disableButton, SIGNAL("toggled(bool)"), self.disable)

		self.stateLabel.setModel("%s/state" % model)
		self.positionLCD.setModel("%s/position" % model)

		self.motor = DeviceProxy(str(model))
		try:
			self.nameLabel.setText(self.motor.alias())
		except Exception:
			match = re.search(r"((?:[^/]+/){2}[^/]+)$", model)
			if not match:
				self.nameLabel.setText(model)
			else:
				self.nameLabel.setText(match.group(1))

		pos = AttributeProxy("%s/position" % model)
		try:
			self.unitLabel.setText(pos.get_config().unit)
		except Exception:
			self.unitLabel.setText("")

		self.absMotionEdit.setText(str(self.motor.position))

	def openConfig(self):
		pass

	def go(self):
		pass

	def moveNeg(self):
		pass

	def movePos(self):
		pass

	def disable(self, d):
		self.setEnabled(not d)






# -----------------------------------------------------------------------------
if __name__ == "__main__":
	signal(SIGINT, SIG_DFL)			# exit on Ctrl+C

	# start application
	Application = TaurusApplication(sys.argv)
	main = MotorWidget("sim/motor/2")
	main.show()
	sys.exit(Application.exec_())