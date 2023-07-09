from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QFileDialog, QErrorMessage
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
from logzero import logger
from modules.utils import LaceworkTime
from __feature__ import true_property
import traceback
import datetime
import os


class ReportPreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.web_viewer = QWebEngineView()
        self.setCentralWidget(self.web_viewer)
        self.resize(1280, 720)
        self.setWindowTitle("Lacework Report Preview")
        self.web_viewer.pdfPrintingFinished.connect(self.pdf_print_finished)

    def load_report(self, report):
        self.web_viewer.setHtml(report)
        self.show()

    def reload_report(self, report):
        self.web_viewer.setHtml(report)

    def pdf_print_finished(self, path, success):
        if success:
            dialog = InfoDialog(f"Successfully wrote {path}")
        else:
            dialog = ErrorDialog(f"Couldn't write {path}, check that you have write permissions.")

    def save_pdf(self, path):
        self.web_viewer.page().printToPdf(path)



class ErrorDialog(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Error Occurred:")
        self.text = message
        self.exec()


class InfoDialog(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Information:")
        self.text = message
        self.exec()


class ExtensibleReportingGUI(QApplication):

    def __init__(self, args, pre_processed_args, available_reports, basedir):
        super().__init__()
        self.args = args
        self.pre_processed_args = pre_processed_args
        self.available_reports = available_reports
        self.basedir = basedir
        if args.report_path:
            self.report_file_name = args.report_path
        else:
            self.report_file_name = None
        self.report = None
        self.report_saved = True
        loader = QUiLoader()
        self.window = loader.load(f"{basedir}/assets/mainwindow.ui", None)
        if args.logo:
            self.window.lineEditCustomLogo.text = args.logo
        else:
            self.window.lineEditCustomLogo.text = "None"
        self.report_preview = ReportPreview()
        self.connect_ui_elements()
        self.populate_fields_from_args()
        self.window.show()


    def connect_ui_elements(self):
        self.window.comboBoxReportSelector.currentTextChanged.connect(self.report_changed)
        self.window.pushButtonRunReport.clicked.connect(self.run_report)
        self.window.pushButtonTogglePreview.clicked.connect( self.toggle_preview)
        self.window.plainTextEditRecommendations.textChanged.connect(self.lineedits_changed)
        self.window.pushButtonWriteHTML.clicked.connect(self.write_html)
        self.window.pushButtonWritePDF.clicked.connect(self.write_pdf)
        self.window.checkBoxUseCache.stateChanged.connect(self.use_cache)
        self.window.lineEditCustomer.textChanged.connect(self.lineedits_changed)
        self.window.lineEditAuthor.textChanged.connect(self.lineedits_changed)
        self.window.pushButtonSelectCustomLogo.clicked.connect(self.set_custom_logo)


    def use_cache(self, state):
        self.report_generator.use_cache = bool(state)

    def lineedits_changed(self):
        self.report_generator.recommendations = self.window.plainTextEditRecommendations.plainText

        if self.report:
            self.report = self.report_generator.render(self.window.lineEditCustomer.text, self.window.lineEditAuthor.text)
            self.report_preview.reload_report(self.report)

    def write_html(self):
        if self.report:
            if not self.report_file_name:
                self.report_file_name = f'{self.window.lineEditCustomer.text}_{self.window.lineEditAuthor.text}_{datetime.datetime.now().strftime("%Y%m%d")}.html'
            else:
                self.report_file_name = str(self.report_file_name).replace(".pdf", ".html")
            filename, _ = QFileDialog.getSaveFileName(self.window, "Save HTML Location", self.report_file_name)
            try:
                if filename:
                    with open(filename, 'w') as f:
                        f.write(self.report)
            except Exception as e:
                error = str(traceback.format_exc())
                logger.error(error)
                dialog = ErrorDialog(str(e))
            else:
                if filename:
                    dialog = InfoDialog(f"Successfully wrote {filename}")

    def write_pdf(self):
        if self.report:
            if not self.report_file_name:
                self.report_file_name = f'{self.window.lineEditCustomer.text}_{self.window.lineEditAuthor.text}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
            else:
                self.report_file_name = str(self.report_file_name).replace(".html", ".pdf")
            filename, _ = QFileDialog.getSaveFileName(self.window, "Save PDF Location", self.report_file_name)
            try:
                if filename:
                    self.report_preview.save_pdf(filename)
            except Exception as e:
                error = str(traceback.format_exc())
                logger.error(error)
                dialog = ErrorDialog(str(e))


    def set_custom_logo(self):
        filename, _ = QFileDialog.getOpenFileName(self.window, "Open Custom Logo", filter="PNG File (*.png)")
        if filename:
            if os.access(filename, os.R_OK):
                self.window.lineEditCustomLogo.text = filename
            else:
                dialog = ErrorDialog("Can't read that file. Check permissions?")


    def toggle_preview(self):
        if self.report_preview.visible:
            self.report_preview.hide()
        else:
            self.report_preview.show()

    def populate_fields_from_args(self):
        for available_report in self.available_reports:
            self.window.comboBoxReportSelector.addItem(available_report['report_name'])
        if self.args.cache_data:
            self.window.checkBoxUseCache.setCheckState(Qt.Checked)
        self.window.lineEditCustomer.text = self.args.customer
        self.window.lineEditAuthor.text = self.args.author
        self.window.spinBoxVulnStartTimeDays.value = int(self.args.vulns_start_time.split(":")[0])
        self.window.spinBoxVulnStartTimeHours.value = int(self.args.vulns_start_time.split(":")[1])
        self.window.spinBoxVulnEndTimeDays.value = int(self.args.vulns_end_time.split(":")[0])
        self.window.spinBoxVulnEndTimeHours.value = int(self.args.vulns_end_time.split(":")[1])
        self.window.spinBoxAlertStartTimeDays.value = int(self.args.alerts_start_time.split(":")[0])
        self.window.spinBoxAlertStartTimeHours.value = int(self.args.alerts_start_time.split(":")[1])
        self.window.spinBoxAlertEndTimeDays.value = int(self.args.alerts_end_time.split(":")[0])
        self.window.spinBoxAlertEndTimeHours.value = int(self.args.alerts_end_time.split(":")[1])

    def report_changed(self, report_name):
        self.report_to_run = [report['report_class'] for report in self.available_reports if report['report_name'] == report_name][0]
        self.report_generator = self.report_to_run(self.basedir, use_cache=self.window.checkBoxUseCache.checked, api_key_file=self.pre_processed_args['api_key_file'])
        logger.debug(f"Currently Selected Report: {report_name}")
        self.window.plainTextEditRecommendations.plainText = self.report_to_run.default_recommendations


    def run_report(self):
        try:
            vuln_start_time = LaceworkTime(f"{self.window.spinBoxVulnStartTimeDays.value}:{self.window.spinBoxVulnStartTimeHours.value}")
            vuln_end_time = LaceworkTime(f"{self.window.spinBoxVulnEndTimeDays.value}:{self.window.spinBoxVulnEndTimeHours.value}")
            alert_start_time = LaceworkTime(f"{self.window.spinBoxAlertStartTimeDays.value}:{self.window.spinBoxAlertStartTimeHours.value}")
            alert_end_time = LaceworkTime(f"{self.window.spinBoxAlertEndTimeDays.value}:{self.window.spinBoxAlertEndTimeHours.value}")
            if self.window.lineEditCustomLogo.text == "None":
                custom_logo = None
            else:
                custom_logo = self.window.lineEditCustomLogo.text
            self.report = self.report_generator.generate(self.window.lineEditCustomer.text,
                                                         self.window.lineEditAuthor.text,
                                                         vulns_start_time=vuln_start_time,
                                                         vulns_end_time=vuln_end_time,
                                                         alerts_start_time=alert_start_time,
                                                         alerts_end_time=alert_end_time,
                                                         custom_logo=custom_logo)
            self.report_saved = False
            self.report_preview.load_report(self.report)

        except:
            traceback_message = traceback.format_exc()
            logger.error(f"Report Generation failed.")
            logger.error(traceback_message)
            QErrorMessage.showMessage(f"Report Generation failed.\n{traceback_message}")
            return

