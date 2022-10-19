# Extensible Report Generator

## Description

A project to abstract the gathering, transformations, and rendering of datasets from Lacework into auto-generated reports.


## Usage for CSA Reports

This tool framework simplifies how partners and internal resources can execute Lacework Cloud Security Assessments to prospective customers. Below are a few example screenshots of the report that once generated is an html that can be modified and exported as a PDF and sent to prospects. 

<img width="604" alt="image (1)" src="https://user-images.githubusercontent.com/10535862/196780720-f74c93d1-ebcb-42d4-930f-66d3c2a6571d.png">

<img width="604" src="https://user-images.githubusercontent.com/10535862/196780812-f546f58a-d40b-4e50-a119-38a0a6e3c656.png">

<img width="604" src="https://user-images.githubusercontent.com/10535862/196780860-a9cae2d1-e047-4b23-9d23-ade77c1d6de0.png">

<img width="604" src="https://user-images.githubusercontent.com/10535862/196780942-de7297c0-89ea-4cce-a6f8-ca712f4ea0ed.png">

## Install & Running Reports:

To get started with either option you will need to ensure you first start with configuring your Lacework CLI. Instructions to do so can be found here: https://docs.lacework.com/cli/


### Option 1:

Use the compiled binary on the releases page. This is the easiest option as you do not need to install python3 and the required prerequisites through pip. To execute this binary:
- Download the corresponding binary based on your computer's OS: https://github.com/lacework-dev/extensible-reporting/releases/
- If running on MacOS you will need to:
    1. Launch a terminal and `chmod +x generate_csa_report_mac`
    2. If prompted to trust this code to execute in your terminal, navigate to `System Preferences -> Security & Privacy -> Privacy (tab)` and scroll to `Developer Tools` and ensure that `Terminal` is checked. You will then need to relaunch your Terminal session
 - Run the report: `./generate_csa_report_mac --author your_name --customer your_customer`
 
 The report will be generated in the same directory you execute the binary with a name of `CSA_Report_customer_date.html`

### Option 2:

This option involves running the `generate_report.py` command directly in this repo but has a few prerequisites.

To run the python directly you will need

- `python3`
- `pip3` (latest version is required, run `pip3 install --upgrade pip`)

To install dependencies run:
```
$ pip3 -r requirements.txt
```

Run the python directly:

```
export LW_PROFILE='some-profile' # optional, will use default profile or other SDK env vars
./generate_report.py --author your_name --customer your_customer
```

Once the report is generated, you may edit the html with your own company logo or add in new content. From there, simply print as a PDF and your report is ready to be shared. 


## Architecture

This project is very modular.  Data is collected with provider modules, which return native python `dict`s.  Transformers are used to do grouping, ordering, aggregation, filtering, and customization of columns.  Transformers should return a `pandas` dataframe.  Reports can be created using any library (currently all are using the `datapane` library.)


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
