'''
A simple script that can read csv file, search content based on  keywords
and store the result in a new csv
'''

import argparse
import sys
import os
import pandas as pd
import numpy as np
import time

# This function will read csv file 
# and extract all lines whose text contains key words
# then save to the distination path
def findRumor(raw_data, keywords, destination: str, threshold: int):
    # Change the form of keywords for the input requirement of Pandas.Series.str.contains
    k_words = keywords[0]
    for i in range(1, len(keywords)):
        k_words = k_words+'|'+keywords[i]

    # extract all the text&quoted text and check the number of keywords they contain
    text = raw_data[raw_data['text'].fillna('nan').str.contains(k_words)].reset_index(drop=True)
    quoted_text = raw_data[raw_data['quoted_text'].fillna('nan').str.contains(k_words)].reset_index(drop=True)
    valid_text = checkThreshold(text['text'], threshold, keywords)
    valid_quoted_text = checkThreshold(quoted_text['quoted_text'], threshold, keywords)
    
    # extract all the satisfied rows
    #rumor_data = raw_data[np.logical_or(valid_text,valid_quoted_text)]
    text_res = text[valid_text]
    quo_res = quoted_text[valid_quoted_text]
    print(len(text_res))
    print(len(quo_res))
    if len(quo_res) == 0:
        rumor_data = text_res
    elif len(text_res) == 0:
        rumor_data = quo_res
    else:
        columns = list(text_res.columns)
        rumor_data = pd.merge(text_res,quo_res,on=columns, how='outer')

    # save data
    print('No. of potential rumors: '+ str(rumor_data.shape[0]))
    rumor_data.to_csv(destination, date_format='%s', index=False)

# This function return the boolean form of the text list indicating the number of keywords in the text is over the threshold
def checkThreshold(text_list, threshold, keywords):
    
    boolean_list = np.empty([len(text_list), 1], dtype = bool)
    if len(text_list) == 0:
        return boolean_list
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that reads csv data, searches data, and save data",
    )

    # Add the arguments:
    #   - s(source_file): the source catalog we want to read
    #   - o(output): the path of the ouput catalog
    #   - t(txt_path): the path of the input txt file

    parser.add_argument(
        '-s',
        help='The location of the source '
    )

    parser.add_argument(
        '-o',
        help='Location of output file ',
        default='.'
    )

    parser.add_argument(
        '-t',
        help='The path of input txt file'
    )

    # parse the args
    args = parser.parse_args()
    s_path = args.s
    o_path = args.o
    t_path = args.t

    # check the validity of paths
    is_output = os.path.exists(o_path)
    if not is_output:
        print('The output path does not exist!')
        sys.exit(0)
    is_source = os.path.exists(s_path)
    if not is_source:
        print('The source path does not exist!')
        sys.exit(0)
    is_txt = os.path.exists(t_path)
    if not is_txt:
        print('The txt path does not exist!')
        sys.exit(0)

    # read txt input into a list
    txt_input = list()
    line_num = 0
    with open(t_path) as tfile:
        r_label, keywords, threshold = '', None, 1
        for line in tfile:
            if line_num%3 == 0:
                r_label = line.strip()
            elif line_num%3 == 1:
                keywords = line.strip().split(',')
            else:
                threshold = int(line.strip())
                txt_input.append((r_label, keywords, threshold))
            line_num += 1
    out_frame = []
    
    start_time = time.time()
    
    for f in os.listdir(s_path):
        if not f.endswith('.csv'):
            continue
        domain = os.path.abspath(s_path)
        csv_file = os.path.join(domain, f)
        raw_data = pd.read_csv(csv_file, dtype=str, error_bad_lines=False)
        filename = os.path.basename(csv_file).split('.')[0]
        print('Process '+csv_file)
        output_path = o_path+'/rumors/'
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        output_path = output_path+filename+'/'
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        for r_label, keywords, threshold in txt_input:
            d_path = output_path+r_label+'.csv'
            if os.path.isfile(d_path):
                os.remove(d_path)
            print('Rumor label: '+r_label)
            print('Keywords: '+ str(keywords))
            # Search keywords and extract the information
            findRumor(raw_data, keywords, d_path, threshold)
            
    print("--- %s seconds ---" % (time.time() - start_time))

        
