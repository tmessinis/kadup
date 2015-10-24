import subprocess, proc_helpers

from os import walk, path
from string import ascii_uppercase

# Main backup object it gets initialized with a dict.
class BackupObject(object):
    def __init__(self, settings):
        self.settings = settings
        
    def return_settings(self):
        return self.settings


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
        self.settings['Executables'] = {}
        
        # For loop to find all the drive letters in the system.
        for drive in ascii_uppercase:
            if path.exists(drive + ':\\'):
                drive_letters.append(drive)
        
        # Check to see if the user's system is either 64 or 32 bit.
        if self.settings['Architecture'] == 'AMD64':
            architecture = '64'
        else:
            architecture = '32'
        
        # For loop which searches system for the specified executable. Once found they are added
        # to the 'Executables' dict created earlier.
        for drive in drive_letters:
            for root, dirs, files in walk('{0}:\\cygwin{1}\\'.format(drive, architecture)):
                if 'rsync.exe' in files:
                    self.settings['Executables']['rsync'] = str(path.join(root, 'rsync.exe'))
                if 'curl.exe' in files:
                    self.settings['Executables']['curl'] = str(path.join(root, 'curl.exe'))
        
        # Use helper function to write out the json file which will include the 'Executables' dict.
        proc_helpers.parse_json(self.settings, 'w')
        
        return self.settings
    
    
    
class UnixBackup(BackupObject):
    pass
