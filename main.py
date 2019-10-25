import json

class config():
    def __init__(file_name):
        self.file_name = file_name
        try:
            self.file = open(file_name, 'w')
        except:
            raise ValueError('Failed to open config file')

    def parse_config():



def main():

if __name__ == '__main__':
    main()