import requests
import uuid

class TranslateSpeech:
	"""
	A class that translates user given speech to a desired language.
	"""
			
	def __init__(self, translator_key:str, setting_objects:dict):
		self.region = 'eastus'
		self.translator_key = translator_key
		self.bot_settings = setting_objects['bot_settings']
		self.voice_settings = setting_objects['voice_settings']
		self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"
			
	def translate_speech(self, speech_to_translate:str, current_language:str, new_language:str, one_shot_translation:bool=False) -> str:
		"""
		Translates a given string of text to a desired langauge.
		"""
  
		if speech_to_translate == 'Exiting. Goodbye!':
			self.bot_settings.save_property('status', True, 'exit')
   
		if one_shot_translation:
			self.bot_settings.save_property('language', True, 'reset')

		# Clean the language input for any punctuation
		current_language, new_language = self._clean_language(current_language, new_language)
   
		# Get the language codes for the current and new languages
		current_language_code = self.voice_settings.retrieve_language_code(current_language.lower())
		new_language_code = self.voice_settings.retrieve_language_code(new_language.lower())
  
		# If the language is not supported, return an error message
		if current_language_code is None:
			return f'Sorry, {current_language} is not currently supported. Try asking again.'

		if new_language_code is None:
			return f'Sorry, {new_language} is not currently supported. Try asking again.'

		# Get the translated speech from Azure's Translator service
		response = self._send_request(current_language_code, new_language_code, speech_to_translate)
   
		return response

	def _clean_language(self, current_language:str, new_language:str) -> tuple:
		# Language sometimes ends in a question mark
		if current_language.endswith('?'):
			current_language = current_language.rstrip('?')

		elif new_language.endswith('?'):
			new_language = new_language.rstrip('?')

		return current_language, new_language

	def _send_request(self, current_language_code:str, new_language_code:str, speech_to_translate:str) -> str:
		"""Send a request to Azure's Translator service to translate a given string of text to a desired language."""
  
		# prepare a request to Azure's Translator service
		params = {
			'api-version': '3.0',
			'from': current_language_code,
			'to': new_language_code
		}
		headers = {
			'Ocp-Apim-Subscription-Key': self.translator_key,
			'Ocp-Apim-Subscription-Region': self.region,
			'Content-type': 'application/json',
			'X-ClientTraceId': str(uuid.uuid4())
		}

		body = [{"text": speech_to_translate}]

		# attempt to send a request to Azure's Translator service
		try:
			request = requests.post(self.endpoint, params=params, headers=headers, json=body)
			response = request.json()

			# get the translated speech
			response = response[0]['translations'][0]['text']
		except Exception as e:
			print(f"An exception occurred: {type(e).__name__}")
			response = f'Sorry, there was an error while trying to translate: {speech_to_translate}. Try asking again.'
   
		return response
