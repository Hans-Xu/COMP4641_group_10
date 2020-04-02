'''
A simple script that can read csv file, search content based on  keywords
and store the result in a new csv
'''

import argparse
import os
import pandas as pd

# This function will read csv file 
# and extract all lines whose text contains key words
# then save to the distination path
def findRumor(source_path: str, keywords: str, destination: str):
    raw_data = pd.read_csv(source_path, dtype=str)
    rumor_data = raw_data[raw_data['text'].str.contains(keywords)]
    rumor_data.to_csv(destination, date_format='%s', index=False)  
    print('Work done!')    

'''
# This function can tranlate all content in the list to English
def translate2En(original_text):
    result = []
    illegal_count = 0
    total = len(original_text)
    print('total: '+str(total))
    count = 0.0
    print_threshold = 0
    for t in original_text:
        try:
            trans = Translator()
            count += 1
            if (count/total*10000) > print_threshold:
                print('process rate: '+ str(print_threshold)+'/10000')
                print('current count: '+str(count))
                print('current illegal: '+str(illegal_count))
                print_threshold += 1
            temp_res = trans.translate(t)
        except Exception as e:
            illegal_count += 1
            temp_res = t
        finally:
            result.append(temp_res)
    print(illegal_count)
    print(str(len(original_text)))
    return result
'''

if __name__ == "__main__":
    # Create our Argument parser and set its description
    parser = argparse.ArgumentParser(
        description="Script that reads csv data, searches data, and save data",
    )
    # Add the arguments:
    #   - source_file: the source file we want to read
    #   - dest_file: the destination where the output should go
    #   - rumor_label: the name/label of this rumor
    #   - key_words: the words that will be used to search in text

    parser.add_argument(
        '-source_file',
        help='The location of the source '
    )
    
    parser.add_argument(
        '-dest_file',
        help='Location of dest file ',
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
        nargs = '+'
    )
    
    # Parse the args (argparse automatically grabs the values from
    # sys.argv)
    args = parser.parse_args()

    s_file = args.source_file
    d_file = args.dest_file
    r_label = args.rumor_label
    keywords = args.key_words
    
    # If the destination file wasn't passed, then assume we want to
    # create a new file based on the old one
    # If the file already exists, delete it and create a new one
    if d_file is None:
        file_path, file_extension = os.path.splitext(s_file)
        d_file = f'{file_path}_{r_label}{file_extension}'
    elif os.path.isfile(d_file):
        os.remove(d_file)
        d_file = f'{d_file}'
    else:
        d_file = f'{d_file}'
    
    
    # Change the form of keywords for the input requirement of Pandas.Series.str.contains
    k_words = keywords[0]
    for i in range(1, len(keywords)):
        k_words = k_words+'|'+keywords[i]

    # Search keywords and extract the information
    findRumor(s_file, k_words, d_file)

    
