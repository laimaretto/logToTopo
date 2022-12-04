# README #

This idea was born because of a need for a simple tool to generate a network topology out of the information obtained from the output of `show router interface` command.

---
## Setup ##

### System Libraries
These libraries have been tested under Ubuntu 20.04 and Windows10 with Python3.8.

###### Ubuntu
```bash
pip3 install getTopo
```
###### Windows
For Windows users, make sure you have Python and [PIP](https://pip.pypa.io/en/stable/installing/) installed.
```bash
py -m pip install getTopo
```
---
## Usage ##

1) Getting data
To obatain the data, use [taskAutom](https://pypi.org/project/taskAutom/) where the plugin uses only the `show router inteface` command.

Example: `taskAutom -d data -py plugin -j 2`

2) Parse the outputs with [logChecker](https://pypi.org/project/logChecker/) using as input folder, the one generated at step 1.

Example: `logChecker -tf folder_of_templates/ -pre folder_step_1`

3) Generate the topology. `logChecker` at step 2. will generate an Excel file with the parsed content. Use that as input.

Example: `logToTopo -xf excel_step_2 -xs sheet_name`.

