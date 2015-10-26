import subprocess, proc_helpers

from os import walk, path
from string import ascii_uppercase

# Main backup object it gets initialized with a dict.
class BackupObject(object):
    def __init__(self, settings):
        self.settings = settings

    def cli_questions(self):
        return_dict = {}
        
        print('Welcome to Kadup backup!\n')
        return_dict['backup_dir'] = \
        proc_helpers.get_valid_path('backup', self.settings['Settings']['Operating_System'])
        return_dict['dest_dict'] = \
        proc_helpers.get_valid_path('destination', self.settings['Settings']['Operating_System'])
        return_dict['schedule'] = \
        proc_helpers.get_valid_yes_no('Is this a one time task or is it going to repeat?')
        

class WindowsBackup(BackupObject):
    def __init__(self, settings):
        BackupObject.__init__(self, settings)

    def make_unix_pathname(self):
        pass
    
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
    
    
    
class UnixBackup(BackupObject):
    pass
