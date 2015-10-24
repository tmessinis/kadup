import platform, backup_models, proc_helpers

BACKUP_OBJECTS_DICT = {
    'Windows': backup_models.WindowsBackup('Windows'),
    'Darwin': backup_models.UnixBackup('Unix'),
    'Linux': backup_models.UnixBackup('Unix')
}

def main():
    try:
        machine_info = proc_helpers.get_machine_info('settings.json')
        
        if machine_info == None:
            main()
        
        operating_system = machine_info[0]
        architecture = machine_info[1]
        
        backup_dir = proc_helpers.get_valid_path('backup', operating_system)
        dest_dir = proc_helpers.get_valid_path('destination', operating_system)
        
        backup_object = BACKUP_OBJECTS_DICT[machine_info[0]]
        print(backup_object)
        return None
        
    except Exception as error:
        print('Kadup has encountered an error. Please check error.log.')
        proc_helpers.make_log('exception', 'error.log', error)
    
if __name__ == '__main__':
    main()