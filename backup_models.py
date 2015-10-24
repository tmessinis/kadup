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
        
    def get_executables(self):
        drive_letters = []
        
        self.settings['Executables'] = {}
        
        # For loop to find all the drive letters in the system.
        for drive in ascii_uppercase:
            if path.exists(drive + ':\\'):
                drive_letters.append(drive)
        
        if self.settings['Architecture'] == 'AMD64':
            architecture = '64'
        else:
            architecture = '32'
        
        for drive in drive_letters:
            for root, dirs, files in walk('{0}:\\cygwin{1}\\'.format(drive, architecture)):
                if 'rsync.exe' in files:
                    self.settings['Executables']['rsync'] = str(path.join(root, 'rsync.exe'))
                if 'curl.exe' in files:
                    self.settings['Executables']['curl'] = str(path.join(root, 'curl.exe'))
                
        proc_helpers.parse_json(self.settings, 'w')
        
        return self.settings
    
    
    
class UnixBackup(BackupObject):
    pass
