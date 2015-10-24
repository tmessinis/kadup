import subprocess, proc_helpers, re

class BackupObject(object):
    def __init__(self, operating_system, architecture):
        self.operating_system = operating_system
        self.architecture = architecture               

class WindowsBackup(BackupObject):
    def make_unix_pathname(self, pathname):
        pass
    
class UnixBackup(BackupObject):
    pass
