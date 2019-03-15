"""Program to Score Speech Quality for assistant intergrations.

Reference go/external-speech-testing for instructions
"""

import argparse
import csv
import os
import subprocess

def read_results_file(file_name):
  with open(file_name, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    next(reader, None)
    return list(reader)


def score(results_file_uri):
  hyp_file_uri = results_file_uri.replace('_raw_transcript_results.csv', '_hyp.trn')
  ref_file_uri = results_file_uri.replace('_raw_transcript_results.csv', '_ref.trn')

  results_list = read_results_file(results_file_uri)
  
  num_frs = 0
  num_errors = 0
  
  hyp_file = open(hyp_file_uri, 'w')
  ref_file = open(ref_file_uri, 'w')

  for results in results_list:
    audio_file = results[0]
    ref = results[2]
    hyp = results[3]

    '''print '\nfile:%s \nref:  %s\nhyp: %s\n' % (audio_file, ref, hyp)'''

    if hyp == 'hotwordfalsereject':
      num_frs += 1
    if hyp =='curlerror':
      num_errors =+1
    else:
      hyp_file.write('%s (%s)\n' % (hyp, audio_file))
      ref_file.write('%s (%s)\n' % (ref, audio_file))

  hyp_file.close()
  ref_file.close()

  fr_stats = 'Utterances Tested: %s\n\n' % len(results_list)
  fr_stats += 'False Rejects: %s\n' % num_frs
  fr_percent = str(round((float(num_frs)/float(len(results_list))) *  100, 2))
  fr_stats += 'False Rejects Rate: %s%%\n' % fr_percent
  fr_stats += 'Error collecting transcript from device %s times\n' % num_errors
  error_percent = str(round((float(num_errors)/float(len(results_list))) *  100, 2))
  fr_stats += 'Error collecting transcript %s%%\n\n' % error_percent

  print subprocess.check_output(['sclite','-h' , hyp_file_uri, 'trn', '-r',
                                 ref_file_uri, 'trn', '-o', 'dtl', '-i', 'wsj'])

  final_report_uri = results_file_uri.replace('_raw_transcript_results.csv', '_transcript_report.txt')

  print fr_stats
  with open('%s.dtl' % hyp_file_uri, 'r') as hyp_file:
    with open(final_report_uri, 'w') as final_report_file:
      final_report_file.write(fr_stats)
      final_report_file.write(hyp_file.read())

  os.remove(hyp_file_uri)
  os.remove(ref_file_uri)
  os.remove('%s.dtl' % hyp_file_uri)


def main():
  parser = argparse.ArgumentParser(description='Score raw results')
  parser.add_argument('--raw_results', required=True,
                      help='URI to raw_results.csv file.')
  args = parser.parse_args()
  score(args.raw_results)

if __name__ == '__main__':
  main()
