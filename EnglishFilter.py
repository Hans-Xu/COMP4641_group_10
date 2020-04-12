'''
A simple script that refined data according to whether its language is English
'''

import argparse
import sys
import os
import pandas as pd
import numpy as np
from langdetect import detect

def process(source, dest):
    raw_data = pd.read_csv(source, dtype=str)
    is_text_en = checkEnglish(raw_data['text'])
    is_quoted_en = checkEnglish(raw_data['quoted_text'])
    en_data = raw_data[is_text_en & is_quoted_en]
    en_data.to_csv(dest, date_format='%s', index=False)

# This function return the boolean form of the text list indicating whether the text is English
def checkEnglish(text_list):
    boolean_list = np.empty([len(text_list), 1], dtype = bool)
    for i in range(len(text_list)):
        if str(text_list[i]) == 'nan' or detect(str(text_list[i]))=='en':
            boolean_list[i] = True
        else:
            boolean_list[i] = False
    return boolean_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that reads csv data, searches data, and save data",
    )

    # Add the arguments:
    #   - s(source_file): the source catalog we want to read
    #   - o(output): the path of the ouput catalog

    parser.add_argument(
        '-s',
        help='The location of the source '
    )

    parser.add_argument(
        '-o',
        help='Location of output file ',
        default=None
    )

    # parse the args
    args = parser.parse_args()
    s_path = args.s
    o_path = args.o

    # check the validity of paths
    if o_path == None:
        o_path = s_path
    is_output = os.path.exists(o_path)
    if not is_output:
        print('The output path does not exist!')
        sys.exit(0)
    is_source = os.path.exists(s_path)
    if not is_source:
        print('The source path does not exist!')
        sys.exit(0)

    # Process each file
    for f in os.listdir(s_path):
        if not f.endswith('.csv'):
            continue
        domain = os.path.abspath(s_path)
        csv_file = os.path.join(domain, f)
        filename = os.path.basename(csv_file).split('.')[0]
        print('Process '+csv_file)
        output_path = o_path+'/english_only/'
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        output_path = output_path+filename+'.csv'
        process(csv_file, output_path)