# Extensible Report Generator

## Description

A project to abstract the gathering, transformations, and rendering of datasets into reports.

## Installation / Requirements

- `python3`
- `pip3` (latest version is required, run `pip3 install --upgrade pip`)

To install dependencies run:
```
$ pip3 -r requirements.txt
```

## Usage for CSA Reports

### Option 1:

Use the compiled binary on the releases page

### Option 2:

Run the python directly:

```
export LW_PROFILE='some-profile' # optional, will use default profile or other SDK env vars
./generate_report.py [--report-path GENERATED_REPORT_PATH] reports/jinja2/csa_report.py
```

## General Usage

`usage: generate_report.py [-h] [--report-path REPORT_PATH] [--use-cached-data] REPORT_GENERATOR`

NOTE: You can use the env vars [specified in the SDK](https://github.com/lacework/python-sdk#environment-variables) to control api access

### Example commands
```
export LW_PROFILE=some_profile # will use default lacework profile if not provided

./generate_report.py [--use-cached-data] reports/jinja2/csa_report.py --report-path sample_reports/csa_report.html --author "Your Name" --customer "Customer Name"
```

## Architecture

This project is very modular.  Data is collected with provider modules, which return native python `dict`s.  Transformers are used to do grouping, ordering, aggregation, filtering, and customization of columns.  Transformers should return a `pandas` dataframe.  Reports can be created using any library (currently all are using the `datapane` library.)

### Providers

TBD

### Transformers

TBD

### Reports

TBD

### Cached Data

To simplify development and limit the API calls made to a provider's backend, the main CLI interface supports the `--use-cached-data` argument.  If developing a report which uses providers which do not have a cached data equivalent, then it is encouraged to exit with an exception if this flag is passed.

To create a set of cached data, run the `generate_cached_data.py` script.

The script by default will generate cached date for whatever Lacework profile or API credentials you have in your environment.

To only generate cached data for specific sets, add one or more as parameters to the command line.

eg: `./generate_cached_data.py lw_compliance lw_events`

The full set of available data sources is [hardcoded in the script](generate_cached_data.py#L20)

### Logging

TBD

## Contributing

Open a pull request!

## License and Copyright

Copyright 2022, Lacework Inc.

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
