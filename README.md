# What is Status?
Status is a tool written in python that allows you to monitor your servers and services with custom bash scripts and other executables.

# Why Status?
This is a very light and easy to use tool that does not require installation in any of the services you are monitoring.

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

# Scripts
The scripts you use to monitor your different services can communicate their status by returning the following codes:

|Code|Explanation|
|---|---|
|0|Up, the service is all ok|
|1|Down, the service is not running|
|2|Warning|
|3|Unknown|
