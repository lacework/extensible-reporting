# Extensible Report Generator

## Description

A project to abstract the gathering, transformations, and rendering of datasets from Lacework into auto-generated reports.


## Usage for CSA Reports

This tool framework simplifies how partners and internal resources can execute Lacework Cloud Security Assessments to prospective customers. Below are a few example screenshots of the report that once generated is an html that can be modified and exported as a PDF and sent to prospects. 

<img width="604" alt="image (1)" src="https://user-images.githubusercontent.com/10535862/196780720-f74c93d1-ebcb-42d4-930f-66d3c2a6571d.png">

<img width="604" src="https://user-images.githubusercontent.com/10535862/196780812-f546f58a-d40b-4e50-a119-38a0a6e3c656.png">

<img width="604" src="https://user-images.githubusercontent.com/10535862/196780860-a9cae2d1-e047-4b23-9d23-ade77c1d6de0.png">

<img width="604" src="https://user-images.githubusercontent.com/10535862/196780942-de7297c0-89ea-4cce-a6f8-ca712f4ea0ed.png">




## Downloading and Setting up the Tool

### Option 1:

Use the compiled binary on the releases page. This is the easiest option as you do not need to install python3 and the required prerequisites through pip. To execute this binary:
- Download the corresponding binary based on your computer's OS: https://github.com/lacework/extensible-reporting/releases/

- If running on MacOS you will need to:
    1. Launch a terminal and `chmod +x lw_report_gen_mac`
    2. If prompted to trust this code to execute in your terminal, navigate to `System Preferences -> Security & Privacy -> Privacy (tab)` and scroll to `Developer Tools` and ensure that `Terminal` is checked. You will then need to relaunch your Terminal session
 - Run the report: `./lw_report_gen_mac --author your_name --customer your_customer`
 
- If running on Windows you will need to:
    1. Launch a command prompt and run the report from the directory you downloaded it to `lw_report_gen.exe --author your_name --customer your_customer`
    
    
 
 The report will be generated in the same directory you execute the binary with a name of `CSA_Report_customer_date.html`

### Option 2:

This option involves running the `lw_report_gen.py` command directly in this repo but has a few prerequisites.

To run the python directly you will need

- `python3`
- `pip3` (latest version is required, run `pip3 install --upgrade pip`)

To install dependencies run:
```
$ pip3 install -r requirements.txt
```

On Windows or Linux run the script using the python interpreter:
```
python lw_report_gen.py --author your_name --customer your_customer
```
On a Mac you may need to specify "python3" instead of "python" ("python" references python 2, which won't work). so...
```
python lw_report_gen.py --author your_name --customer your_customer
```
Once the report is generated, you may edit the html with your own company logo or add in new content. From there, simply print as a PDF and your report is ready to be shared. 

## Specifying a Lacework instance and credentials:

Though it is not required, you may wish to install and configure the Lacework CLI. Instructions to do so can be found here: https://docs.lacework.com/cli/

Configuring the Lacework CLI with a default account and credentials will create a .lacework.toml in your home directory which this tool will then use by default. 

If you do not choose to set up the CLI you may download an API key json file from your Lacework instance and specify it using the ````"--api-key-file"```` command line
parameter.

## Query Time Ranges

By default the tool will query Lacework for data in the following time ranges:
```
Vulnerability Data Start: 25 hours prior to execution time -> End : Current time at execution
Alert Data Start Time: 7 days prior to execution time -> End: Current time at execution
```
If you with to change the time range of these queries you can specify new start and stop times using the following flags:

```
--vulns-start-time
--vulns-end-time
--alerts-start-time
--alerts-end-time
```

To use these flags you must specify a number of days and hours prior to execution time in the format `````"days:hours"`````

For example to specify a 14 day window for alerts you would specify:
```
./lw_report_gen_mac --author your_name --customer your_customer --alerts-start-time 14:0
```

Whereas to specify a 7 day window for alerts that starts 2 weeks in the past you would specify:
```
./lw_report_gen_mac --author your_name --customer your_customer --alerts-start-time 14:0 --alerts-end-time 7:0
```
## Cached Data

To simplify development and limit the API calls made to a provider's backend, the main CLI interface supports the `--cache-data` flag. 
If you are customizing this script you may wish to use this flag to speed up script execution during testing and eliminate most of the API calls to Lacework. 
Note that the cache files created the first time you use this flag will be used in all subsequent runs in which you use this flag. They will not expire. 
If you want to create new cache files you need to manually delete the cache files. For instance on Mac and Linux:
```
rm *.cache
```

## Logging

The script will generate a log file called ```lw_report_gen.log```If you encounter an issue or bug please include the relevant log entries when filing an issue on our github page. 

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
