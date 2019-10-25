import json

class Check():

class Config():
    def __init__(self, file_name):
        try:
            self.file = open(file_name, 'r+')
        except FileNotFoundError:
            raise ValueError('Failed to find config file')
        
        self.file_name = file_name

        self.load_options()

    def load_options(self):
        self.data = json.load(self.file)
    
    def script_dir(self):
        return self.data['general']['script_dir']

def main():
    main_config = Config("config.json")
    print(main_config.data)

if __name__ == '__main__':
    main()