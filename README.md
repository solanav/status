# What is Status?
Status is a tool written in python that allows you to monitor your servers and services with custom bash scripts. A web interface is in progress.

# Config
The configuration file is a json file that contains two sections:

## General
|Option|Explanation|Required|Example|
|---|---|--|---|
|script_dir|Directory where the scripts are|Yes|/home/user/scripts|

## Check
Contains a list of json objects which describe a service checker with these options:

|Option|Explanation|Required|Example|
|---|---|---|---|
|name|Name of the script|Yes|/home/user/scripts|
|script|Name of the file to execute|Yes|check_apache.sh|
|timer|Time in seconds between each call to this script|Yes|5|
