from src.juno import Juno
 
def create_custom_profile():
    """
    Create and save a custom profile to be used by Juno
    """
    # Get available voice names for Elevenlabs or Azure voice engine
    Juno.get_voices(engine='elevenlabs') 
    # Test text-to-speech with a given voice name and engine
    Juno.verbalize(input='This is to test a voice name before using it', voice_name='sarah', engine='elevenlabs') 
    
   # Creating configs for both agents with optional args
    time_traveler_config = {
        'name': 'Dr. Chronos', 
        'role': 'time_traveler', 
        'gender': 'male', 
        'language': 'english', 
        'personality': 'inquisitive', 
        'gpt_model': 'gpt-3.5-turbo', 
        'prompt': "You are a time traveler from the 25th century coming in contact with an alien from the far reaches of the galaxy", 
        'package': 'basic', # 'basic' you can pause, resume, and exit conversations with user input from microphone. 
                            # 'interactive' is 'basic' plus the ability to interact with agents using user input from microphone.
                            # None: No input from microphone is used, conversation must be manually stopped.
        'voice_engine': 'azure', 
        'voice_name': 'matthew', 
        'startup_sound': False
    }
    
    alien_config = {
        'name': 'Zog', 
        'role': 'alien', 
        'gender': 'female', 
        'language': 'english', 
        'personality': 'curious', 
        'gpt_model': 'gpt-3.5-turbo', 
        'prompt': "You are an alien from the far reaches of the galaxy coming in contact with a traveler from the 25th century", 
        'package': 'basic',
        'voice_engine': 'azure', 
        'voice_name': 'zara', 
        'startup_sound': False
    }
    
    #save profiles
    Juno.create_profile(name='time_traveler', config=time_traveler_config) 
    Juno.create_profile(name='alien', config=alien_config)
    
    #see profiles
    print(Juno.load_profile_data())
    
    # delete profiles
    # Juno.remove_profile(name='pilot') 
    # Juno.remove_profile(name='atc')
    
    # example of usage for created profiles can be seen in pizza_order_example.py