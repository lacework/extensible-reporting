from modules.lacework_interface import LaceworkInterface
from modules.reportgen import ReportGen
import os

basedir = os.path.dirname(os.path.abspath(__file__))
rg = ReportGen(basedir)
now = rg.generate_time_string()
minus_25h = rg.generate_time_string(hours=25)
minus_7d = rg.generate_time_string(days=7)


def test_lacework_interface_reports():
    lw = LaceworkInterface()
    reports = lw.get_compliance_reports()
    assert reports is not False


def test_lacework_interface_alerts():
    lw = LaceworkInterface()
    alerts = lw.get_alerts(minus_7d, now)
    assert alerts is not False


def test_lacework_interface_container_vulns():
    lw = LaceworkInterface()
    container_vulns = lw.get_container_vulns(minus_25h, now)
    assert container_vulns is not False


def test_lacework_interface_host_vulns():
    lw = LaceworkInterface()
    host_vulns = lw.get_host_vulns(minus_25h, now)
    assert host_vulns is not False





