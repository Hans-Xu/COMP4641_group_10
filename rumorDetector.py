'''
A simple script that can read csv file, search content based on  keywords
and store the result in a new csv
'''

import argparse
import sys
import os
import pandas as pd
import numpy as np
from langdetect import detect

# This function will read csv file 
# and extract all lines whose text contains key words
# then save to the distination path
def findRumor(source_path: str, keywords, destination: str, threshold: int):
    raw_data = pd.read_csv(source_path, dtype=str)
    # extract all the text&quoted text and check the number of keywords they contain
    text = raw_data['text']
    quoted_text = raw_data['quoted_text']
    valid_text = checkThreshold(text, threshold, keywords)
    valid_quoted_text = checkThreshold(quoted_text, threshold, keywords)
    # extract all the satisfied rows
    rumor_data = raw_data[np.logical_or(valid_text,valid_quoted_text)]
    # extract all the text&quoted text in the rumor data and check whether they are in English
    '''
    rumor_text = rumor_data['text']
    rumor_quoted_text = rumor_data['quoted_text']
    en_rumor = checkEnglish(rumor_text) & checkEnglish(rumor_quoted_text)
    # extract the english rumor
    rumor_data = rumor_data[en_rumor]
    '''
    # save data
    print('No. of potential rumors: '+ str(rumor_data.shape[0]))
    rumor_data.to_csv(destination, date_format='%s', index=False)     

# This function return the boolean form of the text list indicating the number of keywords in the text is over the threshold
def checkThreshold(text_list, threshold, keywords):
    boolean_list = np.empty([len(text_list), 1], dtype = bool)
    for i in range(len(text_list)):
        if countKeyWords(text_list[i], keywords) >= threshold:
            boolean_list[i] = True
        else:
            boolean_list[i] = False
    return boolean_list
        
# This function count the number of keywords that the text contains
def countKeyWords(text, keywords): 
    count = 0
    text = str(text)
    for word in keywords:
        if word in text:
            count += 1
    return count

# This function return the boolean form of the text list indicating whether the text is English
def checkEnglish(text_list):
    boolean_list = np.empty([len(text_list), 1], dtype = bool)
    for i in range(len(text_list)):
        if detect(str(text_list[i]))=='en':
            boolean_list[i] = True
        else:
            boolean_list[i] = False
    return boolean_list

if __name__ == "__main__":
    # Create our Argument parser and set its description
    parser = argparse.ArgumentParser(
        description="Script that reads csv data, searches data, and save data",
    )
    # Add the arguments:
    #   - source_file: the source file we want to read
    #   - txt_input: determine whether use txt file as input parameters or not
    #   - txt_path: the path of the input txt
    #   - output: the path for the output; it should be a file if txt_input is False, and should be a path to a folder if txt_input is True 
    #   - rumor_label: the name/label of this rumor
    #   - key_words: the words that will be used to search in text
    #   - search_threshold: the threshold of the number of keywords in a text that should be extracted

    parser.add_argument(
        '-source_file',
        help='The location of the source '
    )
    
    parser.add_argument(
        '-output',
        help='Location of output file ',
        default=None
    )
    
    parser.add_argument(
        '-rumor_label',
        help='The label of this rumor',
        default = None
    )
    
    parser.add_argument(
        '-key_words',
        help='All keywords you want to search, use space to separate each word',
        nargs = '+',
        default = ['corona']
    )

    parser.add_argument(
        '-search_threshold',
        help='Only when the content contains more than or equal to this threshold will it be extracted',
        default = 1,
        type = int
    )

    parser.add_argument(
        '-txt_input',
        help='Decide whether to use txt file to input rumor label and keywords',
        default = True
    )

    parser.add_argument(
        '-txt_path',
        help='The path of input txt file',
        default = None
    )
    
    # parse the args
    args = parser.parse_args()
    txt = args.txt_input
    s_file = args.source_file
    d_file = args.output
    if txt == False:
        r_label = args.rumor_label
        keywords = args.key_words
        threshold = args.search_threshold
    else:
        txt_path = args.txt_path

    if txt == False:
        # If the destination file wasn't passed, then assume we want to
        # create a new file 
        # If the file already exists, delete it and create a new one
        if d_file is None:
            file_path, file_extension = os.path.splitext(s_file)
            if os.path.isfile(file_path+'_'+r_label+file_extension):
                os.remove(file_path+'_'+r_label+file_extension)
            d_file = f'{file_path}_{r_label}{file_extension}'
        elif os.path.isfile(d_file):
            os.remove(d_file)
            d_file = f'{d_file}'
        else:
            d_file = f'{d_file}'
    
        # check whether the threshold is illegal
        if threshold > len(keywords):
            print('The threshold can not be larger than the number of keywords!')
            sys.exit(0)

        # Search keywords and extract the information
        findRumor(s_file, keywords, d_file, threshold)
        print('Work Done!')
   
    else:
        # If the output path exists, then create a folder in that path
        if d_file is None:
            d_file = '.'
        folder = os.path.exists(d_file)
        if folder:
            path = d_file+'/rumors/'
            if os.path.exists(path) == False:
                os.mkdir(path)
        else:
            print('The path does not exitst!')
            sys.exit(0)

        # The form of the txt file:
        # For each rumor, the first line is the rumor's label
        # the second line is the keywords separeted by comma
        # the third line is a number indicating the threshold

        # input stores tuples of inputs in a form (label, keywords, threshold)
        input = list()
        line_num = 0
        with open(txt_path) as tfile:
            r_label, keywords, threshold = '', None, 1
            for line in tfile:
                if line_num%3 == 0:
                    r_label = line.strip()
                elif line_num%3 == 1:
                    keywords = line.strip().split(',')
                else:
                    threshold = int(line.strip())
                    input.append((r_label, keywords, threshold))
                line_num += 1
        
        for r_label, keywords, threshold in input:
            d_path = path+'/'+r_label+'.csv'
            if os.path.isfile(d_path):
                os.remove(d_path)
            d_file = f'{d_path}'
            print('Rumor label: '+r_label)
            print('Keywords: '+ str(keywords))
            # Search keywords and extract the information
            findRumor(s_file, keywords, d_file, threshold)
            

    
