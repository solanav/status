import json
from subprocess import run
import threading
import signal

# States of the scripts
UP = 'up'
DOWN = 'down'
WARNING = 'warning'
UNKNOWN = 'unknown'

class Config():
    def __init__(self, file_name):
        try:
            self.file = open(file_name, 'r+')
        except FileNotFoundError:
            raise ValueError('Failed to find config file')
        
        self.file_name = file_name # File name
        self.data = json.load(self.file) # JSON data

        # Loaded data
        self.script_list = None

        # General Options
        self.script_dir = self.data['general']['script_dir']

    def get_scripts(self):
        self.script_list  = self.data['check']
        return self.script_list


class Check():
    def __init__(self, config):
        self.config = config
        self.scripts = []
        self.threads = []
        self.state = {}

    def get_all_info(self):
        scripts = self.config.get_scripts()

        # Script list with updated status attatched
        status_script_list = []

        # Stats counting each 
        stats = {}
        stats[UP] = 0
        stats[DOWN] = 0
        stats[WARNING] = 0
        stats[UNKNOWN] = 0

        # Append status of script each time this is reloaded
        for script in scripts:
            script['status'] = self.state[script['name']]
            status_script_list.append(script)

            # Add one to the status counter
            if script['status'] == UP:
                stats[UP] += 1
            elif script['status'] == DOWN:
                stats[DOWN] += 1
            elif script['status'] == WARNING:
                stats[WARNING] += 1
            else:
                stats[UNKNOWN] += 1

        return status_script_list, stats

    def run_script(self, script_dict):
        try:
            ret = run([self.config.script_dir + script_dict['script']])
            if ret.returncode == 0:
                self.state[script_dict['name']] = UP
            elif ret.returncode == 1:
                self.state[script_dict['name']] = DOWN
            elif ret.returncode == 2:
                self.state[script_dict['name']] = WARNING
            else:
                self.state[script_dict['name']] = UNKNOWN

        except PermissionError as e:
            raise e

    def run_all(self):
        for script in self.config.get_scripts():
            self.run_script(script)
    
    def add_script(self, script_dict):
        def run_script_repeat(script_dict):
            t = threading.Timer(int(script_dict['timer']), run_script_repeat, [script_dict, ])
            self.threads.append(t)
            self.run_script(script_dict)
            t.start()

        self.scripts.append(lambda: run_script_repeat(script_dict))

        print('[BUILD] Added ' + script_dict['name'])

    def add_all(self):
        for script in self.config.get_scripts():
            self.add_script(script)

    def run(self):
        for script_lambda in self.scripts:
            script_lambda()
        
    def stop(self):
        for thread in self.threads:
            thread.cancel()