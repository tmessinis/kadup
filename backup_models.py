import subprocess, proc_helpers, re

class BackupObject(object):
    def __init__(self, settings):
        self.settings = settings


class WindowsBackup(BackupObject):
    def make_unix_pathname(self, pathname):
        pass
    
class UnixBackup(BackupObject):
    pass
