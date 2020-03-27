# COMP4641_group_10
## rumorDetector.py

Simple script that can extract content based on keywords

It has 4 args:

  [-source_file =] the path of the source csv file
  
  [-dest_file =] the path of the written file (default = None)
  
  [-rumor_label =] if the dest_file is None, the default new file will contain this label
  
  [-key_words] a list of key words that will be used for searching
  
sample use:

  python rumorDetector.py -source_file=sample.csv -rumor_label=test -key_words haha hehe hoho lol XD
    
