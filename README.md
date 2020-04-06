# COMP4641_group_10
## rumorDetector.py

Simple script that can extract content based on keywords

pre_requisite:
```
pip intall pandas
```

It has 4 args:

  [-source_file =] the path of the source csv file
  
  [-txt_input =] whether or not to use txt file as input (default = True) The format of the txt should be: for each rumor, it has three lines. The first line is its label, the second line is the kewords seperated by commas, the third line is the threshold
  
  [-txt_path = ] The path of the input txt file (default = None)
  
  [-output =] the path of the output file. It should be a catalog in txt input mode, a file else. If it's None, the output will be in the same catalog of rumorDetector.py (default = None)
  
  [-rumor_label =] if the dest_file is None, the default new file will contain this label (default = None)
  
  [-key_words] a list of key words that will be used for searching (default = ['corona'])
  
  [-search_threshold] the threshold of the number of keywords in a text that should be extracted (default = 1)
  
txt input sample use:

  ```
  python rumorDetector.py -source_file=sample.csv -txt_path=sample.txt
  ```

non-txt sample use:
  ```
  python rumorDetector.py -source_file=sample.csv -rumor_label=test -search_threshold=3 -key_words haha hehe hoho lol XD 
  ``` 
