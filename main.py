import json
from subprocess import run
import threading
import signal


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
        if self.script_list == None:
            self.script_list  = self.data['check']

        return self.script_list


class Check():
    def __init__(self, config):
        self.config = config
        self.scripts = []
        self.threads = []

    def run_script(self, script_dict):
        print('Running {}...'.format(script_dict['name']), end=' ')

        try:
            ret = run([self.config.script_dir + script_dict['script']])
            if ret.returncode == 0:
                print('[OK]')
            else:
                print('[ERROR]')
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

        print('Added ' + script_dict['name'])

    def add_all(self):
        for script in self.config.get_scripts():
            self.add_script(script)

    def run(self):
        for script_lambda in self.scripts:
            script_lambda()
        
    def stop(self):
        for thread in self.threads:
            thread.cancel()

class Signals():
    def __init__(self, config):
        self.config = config
    
    def sigint(self, sig, frame):
        self.config.stop()

    def setup(self):
        signal.signal(signal.SIGINT, self.sigint)

def main():
    config = Config("config.json")
    check = Check(config)
    signal = Signals(check)
    
    # Start signal handlers
    signal.setup()

    # Add scripts and run
    check.add_all()
    check.run()

if __name__ == '__main__':
    main()