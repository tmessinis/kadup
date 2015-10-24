import platform, backup_models, proc_helpers

settings = {}

BACKUP_OBJECTS_DICT = {
    'Windows': backup_models.WindowsBackup(settings),
    'Darwin': backup_models.UnixBackup(settings),
    'Linux': backup_models.UnixBackup(settings)
}

def main():
    try:
        settings = proc_helpers.get_settings('settings.json')
        
        if settings == None:
            main()
            
        operating_system = settings['Operating_System']
        architecture = settings['Architecture']
        
        backup_dir = proc_helpers.get_valid_path('backup', operating_system)
        dest_dir = proc_helpers.get_valid_path('destination', operating_system)
        
        backup_object = BACKUP_OBJECTS_DICT[operating_system]
        print(backup_object)
        return None
        
    except Exception as error:
        print('Kadup has encountered an error. Please check error.log.')
        proc_helpers.make_log('exception', 'error.log', error)
    
if __name__ == '__main__':
    main()