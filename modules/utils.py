from datetime import datetime, timezone, timedelta
import re
import hashlib
import json
import functools
import pathlib
import pickle
import importlib
import ast
from pathlib import Path
from logzero import logger
import os, sys, requests, json, time


class LaceworkTime:

    def __init__(self, time_input: str):
        days_and_hours = time_input.split(":")
        self.delta_hours: int = int(days_and_hours[1])
        self.delta_days: int = int(days_and_hours[0])

    def generate_time_string(self) -> str:
        return (datetime.now(timezone.utc) - timedelta(days=self.delta_days, hours=self.delta_hours)).strftime("%Y-%m-%dT%H:%M:%S%Z")


def generate_md5_from_obj(obj_to_hash):
    json_object = json.dumps(obj_to_hash)
    return hashlib.md5(json_object.encode()).hexdigest()


def cache_results(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        use_cache = args[0].use_cache
        if use_cache:
            func_name = func.__name__
            kwargs_hash = generate_md5_from_obj(kwargs)
            file_path = Path(f"lw_csa_{func_name}{kwargs_hash}.cache")
            if file_path.is_file():
                try:
                    logger.info(f"Reading cache file {str(file_path)}")
                    with file_path.open("rb") as f:
                        result = pickle.load(f)
                except Exception as e:
                    logger.error(f"Cache file {str(file_path)} exists but could not be loaded: {str(e)}")
                    result = func(*args, **kwargs)
                    with file_path.open("wb") as f:
                        pickle.dump(result, f)
            else:
                result = func(*args, **kwargs)
                logger.info(f"Writing cache file {str(file_path)}. You must delete this file manually to generate a new cache.")
                with file_path.open("wb") as f:
                    pickle.dump(result, f)
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper


def get_report_class_name_from_file(file: pathlib.Path):

    try:
        with file.open('r') as f:
            contents = f.read()
    except Exception as e:
        logger.error(f'Could not open report module {str(file)}')
        return False
    node = ast.parse(contents)
    report_classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    if len(report_classes) == 0:
        logger.error(f'File {str(file.name)} does not contain a class to import. Skipping')
        return False
    return report_classes[0].name


def get_available_reports(basedir):
    # load available reports from the
    available_reports = []
    modules_dir = pathlib.Path(basedir + '/modules/reports')
    modules_dir_contents = modules_dir.glob('*.py')
    reports_to_load = []
    for module_path in modules_dir_contents:
        class_name = get_report_class_name_from_file(module_path)
        if class_name:
            module_name = str(str(module_path.name).split('.')[0])
            reports_to_load.append({'class_name': class_name, 'module_name': module_name})
        else:
            continue
    for report_to_load in reports_to_load:
        module_name = 'modules.reports.' + report_to_load['module_name']
        globals()[module_name] = importlib.import_module(module_name)
        #  These following three lines are confusing:
        #  First we get the name of the class as a string from the module
        #  Then we use that string to get the class itself
        #  Then we instantiate it.
        #class_name = getattr(globals()[module_name], 'class_name')
        class_ = getattr(globals()[module_name], report_to_load['class_name'])
        available_reports.append({'report_class': class_,
                                  'report_short_name': class_.report_short_name,
                                  'report_name': class_.report_name,
                                  'report_description': class_.report_description})
        logger.info(f'Found and imported class {class_.__name__} from module {module_name}')
    return available_reports

def alert_new_release():
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    try:
        if getattr(sys, 'frozen', False):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
        with open(os.path.join(basedir,'VERSION'), 'r') as f:
            version_current = json.load(f)
            tag_ref = version_current['tag_ref']
            tag_current = version_current['tag_val']
            upgrade_url = version_current['upgrade_url']
            response = requests.get(tag_ref)
            tag_latest = response.json()["tag_name"]

            if tag_latest != tag_current and tag_current != 'placeholder':
                print(f"{WARNING}IMPORTANT:{ENDC}{BOLD}A newer version of this project is available! The latest version is {tag_latest}.{ENDC}", file=sys.stderr)
                print(f"{BOLD}Visit {upgrade_url} to upgrade.{ENDC}", file=sys.stderr)
                time.sleep(5)
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        print(f"{BOLD}Error occured checking for upgrades{ENDC}", file=sys.stderr)
        logger.debug(e)
