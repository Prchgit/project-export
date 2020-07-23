# This file is the actual code for the Python runnable project-migration
from dataiku.runnables import Runnable

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        #Initialise local project
        project = self.client.get_project(self.project_key)
        export_options = self.config.get('Export_Options')
        
        #Initialise remote client
        remote_host = self.config.get('Target_Instance')
        rapi_key = self.config.get('Target_apikey')        
        remote_client = dataikuapi.DSSClient(remote_host, rapi_key)
        
        #Initialise dictionary based on user inputs for export options
        
        dict = {'exportAnalysisModels':('true' if 'export_analysis_models' in export_options else 'false'),
                'exportSavedModels':('true'if 'export_saved_models' in export_options else 'false'),
                'exportAllInputDatasets':('true'if 'export_input_datasets' in export_options else 'false'),
                'exportUploads': ('true'if 'export_uploads' in export_options else 'false'),
                'exportAllDatasets': ('true'if 'export_all_datasets' in export_options else 'false'),
                'exportManagedFS': ('true'if 'export_managed_fs' in export_options else 'false'),
                'exportManagedFolders':('true'if 'export_managed_folders' in export_options else 'false'),
                'exportAllInputManagedFolders':('true'if 'export_all_input_managed_folders' in export_options else 'false')                
               }
        
        with project.get_export_stream(dict) as s:            
            handle = remote_client.prepare_project_import(s)
            handle.execute()
        
        #return(dict.items())
    