import json, re

from os import path
from platform import system, machine

# A helper function that will create log entries based on the type provided. It can be
# used for logging exceptions or for logging the output of a command.
def make_log(type, file, error):
    import logging
    from time import sleep
    
    log_format = '%(asctime)s [%(levelname)s] <%(name)s> %(message)s'
    logging.basicConfig(filename = file, level = logging.DEBUG, format = log_format)
    logger = logging.getLogger(__file__)
    
    if type == 'exception':
        logger.exception(error)
        open('error.log', 'a').write('\n')  

    sleep(5)

# Helper function which parses json whether it's from a json file or from a python dict.    
def parse_json(json_data, option):
    if type(json_data) == dict:
        try:
            with open('settings.json', option) as data:
                return json.dump(json_data, data)
        except Exception as error:
            print('There was an problem generating the settings.json file. Check error.log.')
            make_log('exception', 'error.log', error)
            
            return None
    else:
        try:
            with open(json_data, option) as data:
                parsed_json = json.load(data)
            return parsed_json
        except Exception as error:
            print('The json file {0} does not contain valid json! Check error.log.\
                \nIf {0} does not exist then Kadup will attempt to generate one.'.format(json_data))
            make_log('exception', 'error.log', error)
            
            return None               
    
def check_valid_path(dir, operating_system):
    if operating_system == 'Windows':
        return re.match(r"^[A-Za-z]+?:\\[^<>:\"/\|\?\*]*\\*\.?[^<>:\"/\|\?\*]*$", dir)
    else:
        return None
    
def get_valid_path(label, operating_system):
    while True:
        inputted_pathname = input('Enter {0} directory: '.format(label))
        if check_valid_path(inputted_pathname, operating_system):
            return inputted_pathname
        print('\nThat path is not valid! Please enter a valid path for your OS.\n')
    
# Helper function, returns a tuple which includes the OS and system architecture of the user's
# computer.
def get_machine_info(json_file):

    parsed_json = parse_json(json_file, 'r')
    
    if parsed_json != None:   
        try:
            return parsed_json['Operating_System'], parsed_json['Architecture']
        except Exception as error:
            print('The entry for Operating_System is missing in settings.json! Check error.log')
            make_log('exception', 'error.log', error)
            
            return None
    else:
        json_data = {"Operating_System": system(),
                     "Architecture": machine()}
        parse_json(json_data, 'w')
        
        
        
        
        
        
        