import os
import yaml
import shutil
from src.utils.settings.master_settings.master_settings_manager import MasterSettingsManager

profiles_path = os.path.join('src/profiles/profile_storage')

class ProfileManager:
    
    def __init__(self):
        self.profile_name = MasterSettingsManager().retrieve_property('profile')
    
    def create_profile(self, profile_name, config) -> None:
        """
        Creates a new profile with a given name and config
        A directory is created with the given name and the config is saved in a settings.yaml file
        """
        self._make_profile_directory(profile_name, config)
        
    def remove_profile(self, profile_name) -> None:
        """
        Creates a new profile with a given name and config
        A directory is created with the given name and creates a settings.yaml, conversation_history.yaml, and logs.yaml file within the directory
        """
        directory_name = f'{profiles_path}/{profile_name}'
        
        try:
            # Delete the directory associated with the profile
            shutil.rmtree(directory_name)
        except  FileNotFoundError:
            return
    
    def retrieve_property(self, property_name:str) -> str:
        """
        Gets a given property from a given profile
        """
        profile_data = self.load_profile_data(self.profile_name)
        
        if property_name in ['personality', 'prompt', 'role', 'language']:
            return profile_data['interaction'][property_name]
        if property_name in ['startup_sound', 'voice_recognition_engine', 'voice_engine', 'voice_name']:
            return profile_data['system'][property_name]
        if property_name in ['gender', 'name']:
            return profile_data['user'][property_name]
        
    def _make_profile_directory(self, profile_name, config) -> None:
        """
        Creates a directory with the given name and creates a settings.yaml, conversation_history.yaml, and logs.yaml file within the directory
        """
        directory_name = f'{profiles_path}/{profile_name}'
        
        # Create a new directory with the profile's name
        os.makedirs(directory_name, exist_ok=True)
        
        file_names = ["settings.yaml", "conversation_history.yaml", "logs.yaml"]
        
        # Create files in the directory
        for file_name in file_names:
            with open(os.path.join(directory_name, file_name), 'w') as file:
                if file_name == "settings.yaml":
                    formatted_config = self._format_config(config)
                    yaml.dump(formatted_config, file)
                if file_name == "conversation_history.yaml":
                    yaml.dump({"conversation": []}, file)
                if file_name == "logs.yaml":  
                    yaml.dump({"log_sessions": []}, file)
                    
    def load_profile_data(self, profile_name) -> dict:
        """
        Loads a profile with a given name
        """
        try:
            with open(os.path.join(profiles_path, profile_name, 'settings.yaml'), 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return 
        
    def _format_config(self, config) -> dict:
        """
        Formats the config to be saved in the settings.yaml file
        """
        
        formatted_config = {
            'user': {
                'name': config.get('name', 'Juno'),
                'gender': config.get('gender', 'female')
            },
            'system': {
                'startup_sound': config.get('startup_sound', False),
                'voice_engine': config.get('voice_engine', 'azure'),
                'voice_name': config.get('voice_name', 'Ana')
            },
            'interaction': {
                'role': config.get('role', None),
                'prompt': config.get('prompt', "you are a virtual assistant"),
                'personality': config.get('personality', 'friendly'),
            }
        }
        
        return formatted_config