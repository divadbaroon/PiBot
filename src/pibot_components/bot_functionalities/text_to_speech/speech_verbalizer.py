
from settings.settings_orchestrator import SettingsOrchestrator
import azure.cognitiveservices.speech as speechsdk
import sys
import time

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.

	Attributes:
	bot_properties (BotProperties): A BotProperties object that contains information about the bot's properties.
	speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
	audio_config (AudioOutputConfig): A configuration object that specifies the use of the default speaker
	speech_synthesizer (SpeechSynthesizer): A synthesizer object that uses the above configurations to generate the spoken words
	"""
 
	def __init__(self, audio_config, speech_config, speech_synthesizer):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_settings = SettingsOrchestrator()
		self.audio_config = audio_config
		self.speech_config = speech_config
		self.speech_synthesizer = speech_synthesizer
		self.reset_language = False
		self.exit_status = False
  
	def verbalize_speech(self, speech: str):
		"""Verbalize the bot's response using the speech synthesizer."""""

		self.bot_settings.reload_bot_settings()
		mute_status = self.bot_settings.retrieve_bot_property('mute_status')
		persona = self.bot_settings.retrieve_bot_property('persona')
		gender = self.bot_settings.retrieve_bot_property('gender')
		current_language = self.bot_settings.retrieve_bot_property('language')

		if speech:

			if not mute_status:

				# If the bot is translating, changing the gender, or changing the language the speech will be a dictionary.
				# This is so that the config can be reinitalized with the new property.
				if isinstance(speech, dict):
					speech = self._handle_special_speech(speech, gender, current_language)

					new_voice_name = self.bot_settings.retrieve_bot_property('current_voice_name')
					if new_voice_name:
						self._update_voice(new_voice_name)

				print('\nResponse:')
				print(f'{persona.title()}: {speech}')

				# Verbalize the response
				self.speech_synthesizer.speak_text(speech)
	
				# Check if user wants to exit the program
				if self.exit_status or speech == 'Exiting. Goodbye!':
					sys.exit()

				# If the user was performing a one shot translation, reset the language back to the original language
				if self.reset_language:

					self.bot_settings.save_bot_property('language', current_language)
					gender = self.bot_settings.retrieve_bot_property('gender')
					new_voice_name = self.bot_settings.retrieve_voice_name(gender, current_language)
					self.bot_settings.save_bot_property('current_voice_name', new_voice_name)

					voice_name = self.bot_settings.retrieve_bot_property('current_voice_name')
					if voice_name:
						self._update_voice(voice_name)

					self.reset_language = False
			else:
				print('\n(muted) Response:')
				print(f'{persona.title()}: {speech}')
		else:
			print('No speech has been provided to verbalize.')

	def _update_voice(self, voice_name):
		"""Update the speech config and synthesizer with a new voice."""
		self.speech_config.speech_synthesis_voice_name = voice_name
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

	def _handle_special_speech(self, speech, gender, current_language):
		"""Handle special cases of speech, such as temporary language changes, gender, and language change."""

		if speech['action'] in ['change_gender', 'change_language', 'change_voice', 'randomize_voice']:
			return speech['response']
  
		# Used to for-shot language translations
		if speech['action'] == 'one_shot_translation':
			# Check if the user asked to exit the program in another language
			if speech['original'] == 'Exiting. Goodbye!':
				self.exit_status = True
			# Reset language after one-shot translation
			self.reset_language = True
			# Save the new language to bot_properties.json
			self.bot_settings.save_bot_property('language', speech['new_language'])
			# Get the new voice name
			new_voice_name = self.bot_settings.retrieve_voice_name(gender, speech['new_language'].lower())

			# Update the current voice name
			self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
			return speech['response']

		if speech['action'] == 'translation':
			# Check if the user asked to exit the program in another language
			if speech['original'] == 'Exiting. Goodbye!':
				self.exit_status = True
			return speech['response']

		if speech['action'] == 'start_timer':
			new_voice_name = self.bot_settings.retrieve_bot_property('current_voice_name')
			if new_voice_name:
				self._update_voice(new_voice_name)

			self.verbalize_speech(speech['response'])
			# start timer
			time.sleep(int(speech['user_time']))
			return 'Time is up!'

		if speech['action'] == 'pause':
			self.verbalize_speech(speech['I am now paused'])
			key_stroke = input('To unpause, press enter.')
			while key_stroke != '':
				key_stroke = input('To unpause, press enter.')
			return 'I am unpaused'

		return None

   