import subprocess, proc_helpers

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
        
        proc_helpers.parse_json(self.settings, 'w')
        
        return self.settings
    
    # Generates the syntax of the rsync command to be used.
    def rsync_command(self, rsync_path, backup_path, dest_path):
        return '{0} -azt --verbose --delete "{1}" "{2}"'.format(rsync_path, backup_path, dest_path)

class WindowsBackup(BackupObject):
    def __init__(self, settings):
        BackupObject.__init__(self, settings)
    
    # Helper function that converts Windows style pathnames to Unix for use with Cygwin.
    # Used for the backup and destination directories.
    def make_unix_pathname(self, pathname):
        split_pathname = pathname.split('\\')
        cygwin_pathname = '/cygdrive'
        for path in split_pathname:
            if ':' in path:
                cygwin_pathname += '/' + path[:-1]
            else:
                cygwin_pathname += '/' + path
        return cygwin_pathname
    
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
        
    def run_backup(self):
        runtime_settings = self.settings
        
        if runtime_settings['Settings']['Questions'] == None:
            runtime_settings = self.cli_questions()
            
        if runtime_settings['Settings']['Executables'] == None:
            runtime_settings = self.get_executables()
        self.run_rsync(runtime_settings)
    
class UnixBackup(BackupObject):
    pass
