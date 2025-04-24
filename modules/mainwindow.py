# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1049, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_9 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.checkBoxUseCache = QCheckBox(self.centralwidget)
        self.checkBoxUseCache.setObjectName(u"checkBoxUseCache")

        self.horizontalLayout_5.addWidget(self.checkBoxUseCache)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelSelectReport = QLabel(self.centralwidget)
        self.labelSelectReport.setObjectName(u"labelSelectReport")
        self.labelSelectReport.setEnabled(True)

        self.horizontalLayout_6.addWidget(self.labelSelectReport)

        self.comboBoxReportSelector = QComboBox(self.centralwidget)
        self.comboBoxReportSelector.setObjectName(u"comboBoxReportSelector")
        self.comboBoxReportSelector.setEditable(False)

        self.horizontalLayout_6.addWidget(self.comboBoxReportSelector)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.labelCurrentLogo = QLabel(self.centralwidget)
        self.labelCurrentLogo.setObjectName(u"labelCurrentLogo")

        self.horizontalLayout_6.addWidget(self.labelCurrentLogo)

        self.lineEditCustomLogo = QLineEdit(self.centralwidget)
        self.lineEditCustomLogo.setObjectName(u"lineEditCustomLogo")
        self.lineEditCustomLogo.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.lineEditCustomLogo)

        self.pushButtonSelectCustomLogo = QPushButton(self.centralwidget)
        self.pushButtonSelectCustomLogo.setObjectName(u"pushButtonSelectCustomLogo")

        self.horizontalLayout_6.addWidget(self.pushButtonSelectCustomLogo)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelCustomer = QLabel(self.centralwidget)
        self.labelCustomer.setObjectName(u"labelCustomer")

        self.horizontalLayout.addWidget(self.labelCustomer)

        self.lineEditCustomer = QLineEdit(self.centralwidget)
        self.lineEditCustomer.setObjectName(u"lineEditCustomer")

        self.horizontalLayout.addWidget(self.lineEditCustomer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelAuthor = QLabel(self.centralwidget)
        self.labelAuthor.setObjectName(u"labelAuthor")

        self.horizontalLayout_2.addWidget(self.labelAuthor)

        self.lineEditAuthor = QLineEdit(self.centralwidget)
        self.lineEditAuthor.setObjectName(u"lineEditAuthor")

        self.horizontalLayout_2.addWidget(self.lineEditAuthor)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelVulnStartTime = QLabel(self.centralwidget)
        self.labelVulnStartTime.setObjectName(u"labelVulnStartTime")

        self.horizontalLayout_3.addWidget(self.labelVulnStartTime)

        self.spinBoxVulnStartTimeDays = QSpinBox(self.centralwidget)
        self.spinBoxVulnStartTimeDays.setObjectName(u"spinBoxVulnStartTimeDays")

        self.horizontalLayout_3.addWidget(self.spinBoxVulnStartTimeDays)

        self.labelVulnStartTimeDays = QLabel(self.centralwidget)
        self.labelVulnStartTimeDays.setObjectName(u"labelVulnStartTimeDays")

        self.horizontalLayout_3.addWidget(self.labelVulnStartTimeDays)

        self.spinBoxVulnStartTimeHours = QSpinBox(self.centralwidget)
        self.spinBoxVulnStartTimeHours.setObjectName(u"spinBoxVulnStartTimeHours")

        self.horizontalLayout_3.addWidget(self.spinBoxVulnStartTimeHours)

        self.labelVulnStartTimeHours = QLabel(self.centralwidget)
        self.labelVulnStartTimeHours.setObjectName(u"labelVulnStartTimeHours")

        self.horizontalLayout_3.addWidget(self.labelVulnStartTimeHours)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.labelVulnEndTime = QLabel(self.centralwidget)
        self.labelVulnEndTime.setObjectName(u"labelVulnEndTime")

        self.horizontalLayout_3.addWidget(self.labelVulnEndTime)

        self.spinBoxVulnEndTimeHours = QSpinBox(self.centralwidget)
        self.spinBoxVulnEndTimeHours.setObjectName(u"spinBoxVulnEndTimeHours")

        self.horizontalLayout_3.addWidget(self.spinBoxVulnEndTimeHours)

        self.labelVulnEndTimeDays = QLabel(self.centralwidget)
        self.labelVulnEndTimeDays.setObjectName(u"labelVulnEndTimeDays")

        self.horizontalLayout_3.addWidget(self.labelVulnEndTimeDays)

        self.spinBoxVulnEndTimeDays = QSpinBox(self.centralwidget)
        self.spinBoxVulnEndTimeDays.setObjectName(u"spinBoxVulnEndTimeDays")

        self.horizontalLayout_3.addWidget(self.spinBoxVulnEndTimeDays)

        self.labelVulnEndTimeHours = QLabel(self.centralwidget)
        self.labelVulnEndTimeHours.setObjectName(u"labelVulnEndTimeHours")

        self.horizontalLayout_3.addWidget(self.labelVulnEndTimeHours)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelAlertStartTime = QLabel(self.centralwidget)
        self.labelAlertStartTime.setObjectName(u"labelAlertStartTime")

        self.horizontalLayout_4.addWidget(self.labelAlertStartTime)

        self.spinBoxAlertStartTimeDays = QSpinBox(self.centralwidget)
        self.spinBoxAlertStartTimeDays.setObjectName(u"spinBoxAlertStartTimeDays")

        self.horizontalLayout_4.addWidget(self.spinBoxAlertStartTimeDays)

        self.labelAlertStartTimeDays = QLabel(self.centralwidget)
        self.labelAlertStartTimeDays.setObjectName(u"labelAlertStartTimeDays")

        self.horizontalLayout_4.addWidget(self.labelAlertStartTimeDays)

        self.spinBoxAlertStartTimeHours = QSpinBox(self.centralwidget)
        self.spinBoxAlertStartTimeHours.setObjectName(u"spinBoxAlertStartTimeHours")

        self.horizontalLayout_4.addWidget(self.spinBoxAlertStartTimeHours)

        self.labelAlertStartTimeHours = QLabel(self.centralwidget)
        self.labelAlertStartTimeHours.setObjectName(u"labelAlertStartTimeHours")

        self.horizontalLayout_4.addWidget(self.labelAlertStartTimeHours)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_2)

        self.labelAlertEndTime = QLabel(self.centralwidget)
        self.labelAlertEndTime.setObjectName(u"labelAlertEndTime")

        self.horizontalLayout_4.addWidget(self.labelAlertEndTime)

        self.spinBoxAlertEndTimeDays = QSpinBox(self.centralwidget)
        self.spinBoxAlertEndTimeDays.setObjectName(u"spinBoxAlertEndTimeDays")

        self.horizontalLayout_4.addWidget(self.spinBoxAlertEndTimeDays)

        self.labelAlertEndTimeDays = QLabel(self.centralwidget)
        self.labelAlertEndTimeDays.setObjectName(u"labelAlertEndTimeDays")

        self.horizontalLayout_4.addWidget(self.labelAlertEndTimeDays)

        self.spinBoxAlertEndTimeHours = QSpinBox(self.centralwidget)
        self.spinBoxAlertEndTimeHours.setObjectName(u"spinBoxAlertEndTimeHours")

        self.horizontalLayout_4.addWidget(self.spinBoxAlertEndTimeHours)

        self.labelAlertEndTimeHours = QLabel(self.centralwidget)
        self.labelAlertEndTimeHours.setObjectName(u"labelAlertEndTimeHours")

        self.horizontalLayout_4.addWidget(self.labelAlertEndTimeHours)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.labelReccommendations = QLabel(self.centralwidget)
        self.labelReccommendations.setObjectName(u"labelReccommendations")

        self.horizontalLayout_8.addWidget(self.labelReccommendations)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.plainTextEditRecommendations = QPlainTextEdit(self.centralwidget)
        self.plainTextEditRecommendations.setObjectName(u"plainTextEditRecommendations")

        self.verticalLayout.addWidget(self.plainTextEditRecommendations)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButtonRunReport = QPushButton(self.centralwidget)
        self.pushButtonRunReport.setObjectName(u"pushButtonRunReport")

        self.horizontalLayout_7.addWidget(self.pushButtonRunReport)

        self.pushButtonWriteHTML = QPushButton(self.centralwidget)
        self.pushButtonWriteHTML.setObjectName(u"pushButtonWriteHTML")

        self.horizontalLayout_7.addWidget(self.pushButtonWriteHTML)

        self.pushButtonWritePDF = QPushButton(self.centralwidget)
        self.pushButtonWritePDF.setObjectName(u"pushButtonWritePDF")

        self.horizontalLayout_7.addWidget(self.pushButtonWritePDF)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.pushButtonTogglePreview = QPushButton(self.centralwidget)
        self.pushButtonTogglePreview.setObjectName(u"pushButtonTogglePreview")

        self.horizontalLayout_7.addWidget(self.pushButtonTogglePreview)


        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_9.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1049, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FortiCNAPP Extensible Reporting", None))
        self.checkBoxUseCache.setText(QCoreApplication.translate("MainWindow", u"Use Cache", None))
        self.labelSelectReport.setText(QCoreApplication.translate("MainWindow", u"Select Report:", None))
        self.labelCurrentLogo.setText(QCoreApplication.translate("MainWindow", u"Custom Logo:", None))
        self.lineEditCustomLogo.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.pushButtonSelectCustomLogo.setText(QCoreApplication.translate("MainWindow", u"Select...", None))
        self.labelCustomer.setText(QCoreApplication.translate("MainWindow", u"Customer:", None))
        self.labelAuthor.setText(QCoreApplication.translate("MainWindow", u"Author:", None))
        self.labelVulnStartTime.setText(QCoreApplication.translate("MainWindow", u"Vuln Start Time", None))
        self.labelVulnStartTimeDays.setText(QCoreApplication.translate("MainWindow", u"Days and", None))
        self.labelVulnStartTimeHours.setText(QCoreApplication.translate("MainWindow", u"Hours Ago", None))
        self.labelVulnEndTime.setText(QCoreApplication.translate("MainWindow", u"Vuln End Time", None))
        self.labelVulnEndTimeDays.setText(QCoreApplication.translate("MainWindow", u"Days and", None))
        self.labelVulnEndTimeHours.setText(QCoreApplication.translate("MainWindow", u"Hours Ago", None))
        self.labelAlertStartTime.setText(QCoreApplication.translate("MainWindow", u"Alert Start Time", None))
        self.labelAlertStartTimeDays.setText(QCoreApplication.translate("MainWindow", u"Days and", None))
        self.labelAlertStartTimeHours.setText(QCoreApplication.translate("MainWindow", u"Hours Ago", None))
        self.labelAlertEndTime.setText(QCoreApplication.translate("MainWindow", u"Alert End Time", None))
        self.labelAlertEndTimeDays.setText(QCoreApplication.translate("MainWindow", u"Days and", None))
        self.labelAlertEndTimeHours.setText(QCoreApplication.translate("MainWindow", u"Hours Ago", None))
        self.labelReccommendations.setText(QCoreApplication.translate("MainWindow", u"Recommendations Text:", None))
        self.pushButtonRunReport.setText(QCoreApplication.translate("MainWindow", u"Run Report", None))
        self.pushButtonWriteHTML.setText(QCoreApplication.translate("MainWindow", u"Write HTML", None))
        self.pushButtonWritePDF.setText(QCoreApplication.translate("MainWindow", u"Write PDF", None))
        self.pushButtonTogglePreview.setText(QCoreApplication.translate("MainWindow", u"Toggle Preview Window", None))
    # retranslateUi

