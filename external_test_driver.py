"""Program to test Speech Quality for assistant intergrations.

Reference go/external-speech-testing for instructions
"""

import csv
import json
import os
import string
from StringIO import StringIO
import sys
import time
import wave

from external_test_scoring import score

import pyaudio
import pycurl


# Add assistant IP address here
ASSISTANT_DEVICES_CONFIG = 'device_config.csv'
# DO NOT TOUCH BELOW #
DIR_OF_WAVS = './testdata/wavs'
SPEAKER_TEST_WAV = './testdata/test/speaker_test.wav'
CONFIG_FILE = './testdata/human_truth.csv'
FALSE_ACCEPT_FILE = './testdata/fa/false_accept.wav'
# Seconds to wait for a resposne
SLEEP_FOR_RESPONSE = 10
TIME_START = time.strftime('%Y%m%d-%H%M%S')
FILE_CHUNK = 1024

DEVICES = []

# Testing Mode - Does not ask the Assisant for a machine transcript
TEST_MODE = False
TEST_JSON = r'{"Recognized text":"test transcript","Hotword count":4}'


class Device:

  def close_file(self):
    if hasattr(self, 'results_csv_file'):
      self.results_csv_file.flush()
      self.results_csv_file.close()

  def create_transcript_file(self):
    uri = 'results/%s/%s/' % (TIME_START, self.get_device_name())
    self.file_uri = '%s%s_raw_transcript_results.csv' % (uri, self.ip_address)
    if not os.path.exists(os.path.dirname(uri)):
      os.makedirs(os.path.dirname(uri))
    self.results_csv_file = open(self.file_uri, 'ab')
    fieldnames = ['file_name', 'correct', 'human_truth',
                  'machine_transcript']
    self.writer = csv.DictWriter(self.results_csv_file, fieldnames=fieldnames)
    self.writer.writeheader()

  def get_device_name(self):
    return self.name

  def get_file_uri(self):
    return self.file_uri

  def get_hw_count(self):
    return self.hw_count

  def get_ip_address(self):
    return self.ip_address

  def get_saved_hw_count(self):
    return self.saved_hw_count

  def set_hw_count(self, count):
    self.hw_count = count

  def save_hw_count(self):
    self.saved_hw_count = self.hw_count

  def write_transcript_results(self, audio_file_name, human_truth, machine_transcript):
    human_truth = human_truth.lower().translate(None, string.punctuation)
    machine_transcript = machine_transcript.lower().translate(None,
                                                              string.punctuation)
    if not hasattr(self, 'results_csv_file'):
      self.create_transcript_file()

    self.writer = csv.writer(self.results_csv_file, delimiter=',',
                             quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    self.writer.writerow([audio_file_name, human_truth == machine_transcript,
                          human_truth, machine_transcript])

    print 'Correct: %s Human Truth: %s Machine transcript: %s' % (
        human_truth == machine_transcript, human_truth, machine_transcript)

  def write_fa_file(self):
    uri = 'results/%s/%s/' % (TIME_START, self.get_device_name())
    file_uri = '%s%s_fa_report.txt' % (uri, self.ip_address)
    if not os.path.exists(os.path.dirname(uri)):
      os.makedirs(os.path.dirname(uri))
    fa_stats = 'Starting HW Count %s\nEnding HW Count %s\nHW Fired %s' % (self.get_saved_hw_count(),
                   self.get_hw_count(), self.get_hw_count()-self.get_saved_hw_count())
    with open(file_uri, 'w') as results_fa_file:
      results_fa_file.write(fa_stats)

  def __init__(self, ip_address, name):
    self.ip_address = ip_address
    self.name = name
    self.hw_count = -1


def collect_asr_result(device):
  """Fetches Speech Rec Results from Assistant Device.

  Retrieves JSON file from assistant and parses out the hotword count and the
  machine transcript
  """
  print 'Start Connections %s %s' % (device.get_ip_address(), time.strftime('%Y%m%d-%H%M%S'))

  if TEST_MODE:
    return parse_machine_transcript(TEST_JSON, device)
  string_buffer = StringIO()
  c = pycurl.Curl()
  c.setopt(c.VERBOSE, True)
  c.setopt(pycurl.TIMEOUT, 5)
  c.setopt(pycurl.CONNECTTIMEOUT, 5)
  c.setopt(c.URL, 'http://%s:8007/vars/values' % device.get_ip_address())
  c.setopt(c.WRITEDATA, string_buffer)
  c.perform()
  c.close()

  body = string_buffer.getvalue()
  print 'End Connections %s %s' % (device.get_ip_address(), time.strftime('%Y%m%d-%H%M%S'))
  return parse_machine_transcript(body, device)


def read_truth_file(truth_file):
  with open(truth_file, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    return list(reader)


def read_device_file():
  with open(ASSISTANT_DEVICES_CONFIG, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    return list(reader)


def parse_machine_transcript(json_file, device):
  """Parses JSON file for assistant device.

  Parses out machine transcript, hotword count, and identifies false rejects
  """
  if json_file is None or json_file == '':
    print 'JSON -> device %s :\n Null ' % device.get_device_name()
    return 'null'

  print 'JSON -> device %s :\n %s ' % (device.get_device_name(), json_file)

  # Remove single quotes which could appear in the machine transcript
  parsed_json = json.loads(json_file.replace("'", ""))
  parsed_hotword_count = parsed_json['Hotword count']
  response = 'HOTWORD_FALSE_REJECT'
  # Make sure that the Chirp's HW has not false rejected
  if device.get_hw_count() == -1 or device.get_hw_count() != parsed_hotword_count:
    response = parsed_json['Recognized text'].decode('string_escape')

  device.set_hw_count(parsed_hotword_count)
  return response


def play_audio(audio_file):
  wav_file = wave.open(audio_file, 'rb')
  player = pyaudio.PyAudio()
  stream = player.open(format=player.get_format_from_width(
      wav_file.getsampwidth()), channels=wav_file.getnchannels(),
                       rate=wav_file.getframerate(), output=True)

  audio_data = wav_file.readframes(FILE_CHUNK)

  while audio_data:
    stream.write(audio_data)
    audio_data = wav_file.readframes(FILE_CHUNK)

  stream.stop_stream()
  stream.close()
  player.terminate()

def run_device_test(DEVICES):
  print 'Devices:'

  for device in DEVICES:
    print '  %s @ %s' % (device.get_device_name(), device.get_ip_address())


def run_speaker_test():
  print '*** STARTING SPEAKER TEST ***'
  play_audio(SPEAKER_TEST_WAV)


def run_false_accept():
  for device in DEVICES:
    collect_asr_result(device)
    device.save_hw_count()

  play_audio(FALSE_ACCEPT_FILE)

  for device in DEVICES:
    collect_asr_result(device)
    device.write_fa_file()


def run_queries(truth_file, end_test_after_x_utts):
  queries_played = 0
  audio_human_truth_list = read_truth_file(truth_file)

  for audio_human_truth in audio_human_truth_list:
    if end_test_after_x_utts == queries_played:
      break
    audio_file_name = audio_human_truth[0]
    human_truth = audio_human_truth[1]
    play_audio(DIR_OF_WAVS + '/' + audio_file_name)
    time.sleep(SLEEP_FOR_RESPONSE)

    queries_played += 1

    for device in DEVICES:
      try:
        machine_transcript = collect_asr_result(device)
        device.write_transcript_results(audio_file_name, human_truth,
                             machine_transcript)
      except:
        print('%s Unexpected error: %s' % (device.get_device_name(), sys.exc_info()[0]))
        try:
          time.sleep(SLEEP_FOR_RESPONSE)
          machine_transcript = collect_asr_result(device)
          device.write_transcript_results(audio_file_name, human_truth,
                               machine_transcript)
        except:
          print('2nd Unexpected error:', sys.exc_info()[0])
          device.write_transcript_results(audio_file_name, human_truth,
                               'curlerror')

  for device in DEVICES:
    device.close_file()
    score(device.get_file_uri())


def setup():
  device_config_list = read_device_file()

  for device_config in device_config_list:
    DEVICES.append(Device(device_config[0], device_config[1]))


def main():
  setup()

  print 'Test Menu:\n1.) Speaker Test\n2.) Device Test\n3.) ASR Test\n4.) False Accept Test\n5.) Eraser Test'
  print 'Enter test number [1,2,3,4,5]'
  choice = raw_input().lower()

  if choice == '1':
    run_speaker_test()
  elif choice == '2':
    run_queries(CONFIG_FILE, 5)
  elif choice == '3':
    run_queries(CONFIG_FILE, 10000)
  elif choice == '4':
    run_false_accept()
  elif choice == '5':
    run_queries(CONFIG_FILE, 100)


if __name__ == '__main__':
  main()