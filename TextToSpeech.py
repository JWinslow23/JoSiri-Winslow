import re
import wave
import pyaudio
import _thread
import time
from pydub import AudioSegment

class TextToSpeech:
	
	CHUNK = 1024
	
	def __init__(self, words_pron_dict:str = 'cmudict-0.7b.txt'):
		self._l = {}
		self._load_words(words_pron_dict)
	
	def _load_words(self, words_pron_dict:str):
		print("Loading dictionary...")
		with open(words_pron_dict, 'r') as file:
			for line in file:
				if not line.startswith(';;;'):
					key, val = line.split('  ',2)
					self._l[key] = re.findall(r"[A-Z]+",val)
	
	def get_pronunciation(self, str_input):
		list_pron = []
		for word in re.findall(r"[\w']+",str_input.upper()):
			if word in self._l:
				list_pron += self._l[word]
			else:
				list_pron += ["umm"]
			list_pron += ['0']
		print(list_pron)
		output_sound = AudioSegment.from_wav("sounds/0.wav")
		for pron in list_pron:
			output_sound += AudioSegment.from_wav("sounds/"+pron+".wav")
		output_sound.export("output.wav", format="wav")
	
		try:
			wf = wave.open("output.wav", 'rb')
			p = pyaudio.PyAudio()
			stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
				channels=wf.getnchannels(),
				rate=wf.getframerate(),
				output=True)
			
			data = wf.readframes(TextToSpeech.CHUNK)
			
			while data:
				stream.write(data)
				data = wf.readframes(TextToSpeech.CHUNK)
			
			stream.stop_stream()
			stream.close()
			
			p.terminate()
		except:
			pass




if __name__ == '__main__':
	tts = TextToSpeech()
	tts.get_pronunciation('Enter a word or phrase')
	while True:
		tts.get_pronunciation(input('Enter a word or phrase: '))