import platform, backup_models, proc_helpers, sys
from argparse import ArgumentParser

def main():
    try:
        settings = proc_helpers.get_settings('settings.json')
        
        BACKUP_OBJECTS_DICT = {
            'Windows': backup_models.WindowsBackup(settings),
            'Darwin': backup_models.UnixBackup(settings),
            'Linux': backup_models.UnixBackup(settings)
        }
        
        if settings == None:
            main()
        else:    
            operating_system = settings['Settings']['Operating_System']
            
            #architecture = settings['Settings']['Architecture']
            
            #backup_dir = proc_helpers.get_valid_path('backup', operating_system)
            #dest_dir = proc_helpers.get_valid_path('destination', operating_system)
            
            backup_object = BACKUP_OBJECTS_DICT[operating_system]
            
            help_text = "To start the Kadup CLI simply run: $ python3 kadup.py -c run"
            
            arg_parser = ArgumentParser()
            arg_parser.add_argument('-c', dest='cli', help=help_text, default=None)
            
            if arg_parser.parse_args().cli == 'run':
                backup_object.kadup_cli()
            else:
                backup_object.run_backup()
                
            return None
        
    except Exception as error:
        print('Kadup has encountered an error. Please check kadup.log.')
        proc_helpers.make_log('exception', error)
    
if __name__ == '__main__':
    main()