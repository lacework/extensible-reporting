# Extensible Report Generator

## Description

A project to abstract the gathering, transformations, and rendering of datasets from Lacework into auto-generated reports.

## Quickstart

1. Download the binary for your platform from the releases section

2. Ensure you have some method of authenticating against your FortiCNAPP API. The easiest
    way is to download an API key file from your FortiCNAPP UI under Settings ->  API Keys. 

3. Run the binary <i> from the command line </i> using the following flags: 

`--gui --api-key-file <keyfile>`

Where \<keyfile> is the name of the api key file you downloaded. 

For example on an ARM based Mac download the ARM binary file from the "Releases" section of this page (lw_report_gen_mac_arm
) and execute it:

`./lw_report_gen_mac_arm --gui --api-key-file example.json`

On Mac you may get an error regarding it being an unsigned application. If so you can read the following article on how to run the binary:

https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unknown-developer-mh40616/mac

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
python3 lw_report_gen.py --author your_name --customer your_customer
```
Once the report is generated, you may edit the html with your own company logo or add in new content. From there, simply print as a PDF and your report is ready to be shared. 

## GUI Mode

A new GUI mode has been added to the script. To run the script in GUI mode use the "--gui"
command line flag. 

## Specifying a Lacework instance and credentials:

You must have a valid Lacework API key for your Lacework instance to run this tool. You can read about creating and downloading 
an API key here: 

https://docs.lacework.com/api/api-access-keys-and-tokens

Once you have created an API key There are three ways to specify the Lacework API instance/credentials used when generating a report:

1. Install and configure the Lacework CLI to setup a credentials file which this tool will read.
2. Specify a JSON file containing your API instance/credentials. 
3. Specify your credentials via variables.

### Method 1: Lacework CLI
Though it is not required, you may wish to install and configure the Lacework CLI to create a .lacework.toml file containing your API credentials. Instructions to do so can be found here: https://docs.lacework.com/cli/

### Method 2: JSON File

You may download an API key JSON file from your Lacework instance (Settings > Configuration > API keys) and specify it using the ````"--api-key-file"```` command line
parameter. 

### Method 3: Environment Variables

If you wish to configure the LaceworkClient instance using environment variables, this tool honors the same
variables used by the Lacework CLI. The `account`, `subaccount`, `api_key`, `api_secret`, and `profile` parameters
can all be configured as specified below.

| Environment Variable | Description                                                          | Required |
| -------------------- | -------------------------------------------------------------------- | :------: |
| `LW_PROFILE`         | Lacework CLI profile to use (configured at ~/.lacework.toml)         |    N     |
| `LW_ACCOUNT`         | Lacework account/organization domain (i.e. `<account>`.lacework.net) |    Y     |
| `LW_SUBACCOUNT`      | Lacework sub-account                                                 |    N     |
| `LW_API_KEY`         | Lacework API Access Key                                              |    Y     |
| `LW_API_SECRET`      | Lacework API Access Secret                                           |    Y     |
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

## Creating Your Own Custom Report

Since this tool outputs html by default the most approachable (but manual) way to create a custom report is to modify the
html report it generates. If however you want to modify the tool itself to automatically create reports for you then read  on...

First you must download the source code. There is not currently a way to automatically create custom reports using the executable binary version of this tool.
You should have some familiarity with python object-oriented programming if you are going to attempt automating a custom report. 

To create your own report you must create a custom python module containing a class that inherits from```modules.reportgen```. Place that module file in the
```modules/reports```folder. Be sure to define the following class variables (strings) to ensure that the dynamic module loader can read the class metadata:

```
report_short_name
report_name
report_description
```

Have a look at the default CSA report in `modules/reports/reportgen_csa.py`  for an example.

This tool uses the "jinja2" templating engine to generate the report HTML. Depending on how customized
you want your report to be you may also need to create a custom jinja2 template and 
put it in the `templates` folder. You can then reference this template in your custom report class.  

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
