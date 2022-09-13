# Lacework API Report Generator
## Usage

`usage: generate_report.py [-h] [--report-path REPORT_PATH] [--use-dummy-data] REPORT_GENERATOR`


### Example commands
```
./generate_report.py --use-dummy-data reports/datapane/compliance_report.py --report-path sample_reports/dp_compliance_report.html
./generate_report.py --use-dummy-data reports/datapane/container_vulns_report.py --report-path sample_reports/dp_container_vulns_report.html
./generate_report.py --use-dummy-data reports/datapane/events_report.py --report-path sample_reports/dp_events_report.html
./generate_report.py --use-dummy-data reports/datapane/host_vulns_report.py --report-path sample_reports/dp_host_vulns_report.html
./generate_report.py --use-dummy-data reports/datapane/integrations_report.py --report-path sample_reports/dp_integrations_report.html
./generate_report.py --use-dummy-data reports/jinja2/host_vulns_report.py --report-path sample_reports/j2_host_vulns_report.html
```

## Architecture

This project is very modular.  Data is collected with provider modules, which return native python `dict`s.  Transformers are used to do grouping, ordering, aggregation, filtering, and customization of columns.  Transformers should return a `pandas` dataframe.  Reports can be created using any library (currently all are using the `datapane` library.)

### Providers

TBD

### Transformers

TBD

### Reports

TBD

### Dummy Data

To simplify development and limit the API calls made to a provider's backend, the main CLI interface supports the `--use-dummy-data` argument.  If developing a report which uses providers which do not have a dummy data equivalent, then it is encouraged to exit with an exception if this flag is passed.

To create a set of dummy data, run the `generate_dummy_data.py` script.

### Logging

TBD

## Contributing

TBD. Open a pull request!