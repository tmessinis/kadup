import subprocess, proc_helpers, pprint

from os import walk, path
from string import ascii_uppercase

# Main backup object it gets initialized with a dict.
class BackupObject(object):
    def __init__(self, settings):
        self.settings = settings

    def cli_questions(self):
        self.settings['Settings']['Questions'] = {}
        
        print('Welcome to Kadup backup!\n')
        self.settings['Settings']['Questions']['backup_dir'] = \
            proc_helpers.get_valid_path('backup', self.settings['Settings']['Operating_System'])
        self.settings['Settings']['Questions']['dest_dir'] = \
            proc_helpers.get_valid_path('destination', self.settings['Settings']['Operating_System'])
        self.settings['Settings']['Questions']['one_time'] = \
            proc_helpers.get_valid_yes_no('Is this a one time task (y/n)? ')
                
        if self.settings['Settings']['Questions']['one_time'] is 'n' or \
        self.settings['Settings']['Questions']['one_time'] is 'no':
            print('Please answer the following questions to define time and frequency of the backup task')
            self.settings['Settings']['Questions']['schedule'] = {}
            self.settings['Settings']['Questions']['schedule']['start_time'] = \
                input('Enter the time, in 24-hour format HH:MM, that kadup should begin backing up: ')
            self.settings['Settings']['Questions']['schedule']['interval'] = \
                input('Should this backup run DAILY, WEEKLY, or MONTHLY? ')
            
            if self.settings['Settings']['Questions']['schedule']['interval'] == 'WEEKLY' or \
            self.settings['Settings']['Questions']['schedule']['interval'] == 'weekly':
                self.settings['Settings']['Questions']['schedule']['day_of_week'] = \
                    input('Which day of the week do you want kadup to run (MON-SUN)? ')
                    
            if self.settings['Settings']['Questions']['schedule']['interval'] == 'MONTHLY' or \
            self.settings['Settings']['Questions']['schedule']['interval'] == 'monthly':
                self.settings['Settings']['Questions']['schedule']['day_of_month'] = \
                    input('Which day of the month do you want kadup to run (1-31)? ')
        
        proc_helpers.parse_json(self.settings, 'w')
        
        return self.settings
        
    # A simple command line interface for kadup.
    def kadup_cli(self):
        saved_settings = proc_helpers.get_settings('settings.json')
        intro_help = """
====================================================================================================
    Welcome to Kadup's command line interface!
    Commands:   * run-backup - Run's rsync based on the settings.json file. If that file is missing    
                    info kadup will go through its questionnaire.
                * print-settings - Will list the contents of your settings.json file.
                * help - Will print this information again.
                * exit or quit - Exits the command line interface.
====================================================================================================
        """
        print(intro_help)
        while True:
            command = input('->>>--kadup---> ')
            if command == 'exit' or command == 'quit':
                break
            elif command == 'help':
                print(intro_help)
            elif command == 'print-settings':
                pprint.pprint(saved_settings)
            elif command == 'run-backup':
                if saved_settings['Settings']['Questions'] == None:
                    saved_settings = self.cli_questions()
                if saved_settings['Settings']['Executables'] == None:
                    saved_settings = self.get_executables()
                self.run_rsync(saved_settings)
                
    # Generates the syntax of the rsync command to be used.
    def rsync_command(self, rsync_path, backup_path, dest_path):
        return '{0} -azt --verbose --delete "{1}" "{2}"'.format(rsync_path, backup_path, dest_path)

class WindowsBackup(BackupObject):
    def __init__(self, settings):
        BackupObject.__init__(self, settings)
    
    # Helper function that converts Windows style pathnames to Unix for use with Cygwin.
    # Used for the backup and destination directories.
    def make_unix_pathname(self, pathname):
        if '\\' in pathname:
            split_pathname = pathname.split('\\')
            cygwin_pathname = '/cygdrive'
            for path in split_pathname:
                if ':' in path:
                    cygwin_pathname += '/' + path[:-1]
                else:
                    cygwin_pathname += '/' + path
            return cygwin_pathname
        else:
            return pathname
    
    # A method which searches the users HDDs in a Windows environment for the cygwin executables
    # to be used with this program. The program assumes that the cygwin folder is installed at the
    # root of one of the HDDs. This is to save time, since python can take a long time searching
    # each directory and sub-directory.
    def get_executables(self):
        drive_letters = []
        
        # New dict entry for the executables. They are going to be part of a sub-dict.
        self.settings['Settings']['Executables'] = {}
        
        # For loop to find all the drive letters in the system.
        for drive in ascii_uppercase:
            if path.exists(drive + ':\\'):
                drive_letters.append(drive)
        
        # Check to see if the user's system is either 64 or 32 bit.
        if self.settings['Settings']['Architecture'] == 'AMD64':
            architecture = '64'
        else:
            architecture = '32'
        
        # For loop which searches system for the specified executable. Once found they are added
        # to the 'Executables' dict created earlier.
        for drive in drive_letters:
            for root, dirs, files in walk('{0}:\\cygwin{1}\\'.format(drive, architecture)):
                if 'rsync.exe' in files:
                    self.settings['Settings']['Executables']['rsync'] = \
                    str(path.join(root, 'rsync.exe'))
                if 'curl.exe' in files:
                    self.settings['Settings']['Executables']['curl'] = \
                    str(path.join(root, 'curl.exe'))
        
        # Use helper function to write out the json file which will include the 'Executables' dict.
        proc_helpers.parse_json(self.settings, 'w')
        
        return self.settings
    
    def run_rsync(self, runtime_settings):
        command_parameters = {
            'rsync_path': runtime_settings['Settings']['Executables']['rsync'],
            'backup_path': self.make_unix_pathname\
            (runtime_settings['Settings']['Questions']['backup_dir']),
            'dest_path': self.make_unix_pathname\
            (runtime_settings['Settings']['Questions']['dest_dir'])
        }
        
        command = self.rsync_command(command_parameters['rsync_path'],
                                    command_parameters['backup_path'],
                                    command_parameters['dest_path'])
    
        run_command = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\
        universal_newlines=True, shell=True)
        
        proc_helpers.make_log('info', run_command.stdout.read())
        
        return None
        
    def schtasks_command(self):
        pass
        
    def schedule_task(self):
        pass
    
    # The main function to begin a backup operation.
    def run_backup(self):
        runtime_settings = self.settings
        
        if runtime_settings['Settings']['Questions'] == None:
            runtime_settings = self.cli_questions()
            
        if runtime_settings['Settings']['Executables'] == None:
            runtime_settings = self.get_executables()
        self.run_rsync(runtime_settings)
    
class UnixBackup(BackupObject):
    pass
