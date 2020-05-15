# COMP4641_group_10

## nlp_labeling_test.ipynb
Input: Human-labeled csv <br/>
Outcome: <br/>
1)Pick up the model that gives the highest accuracy, then apply this model to predict labels <br/>
2)Statistics of labels distribution <br/>
3)consufion matrix<br/>

Remember to <br/>
1.markdown which model is used for prediction<br/>
2.screenshot 2) & 3), examples as the following:<br/>
![Alt text](image/label_distribution.png?raw=true "Title" | width=100)
![Alt text](image/confusion_matrix.png?raw=true "Title" | width=100)

## nlp_labeling_predict.ipynb
Input: <br/>
1)Human-labeled csv (training set) <br/>
2)Un-labeled csv (testing set) <br/>
Outcome: human-generated labels

## rumorDetector.py

Simple script that can extract content based on keywords

pre_requisite:
```
pip intall pandas
```

It has 7 args:

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

## rumorDetector_readall.py

This script is a simplified version of rumorDetectors.py but can read all csv files in a folder as source files.

It has only 3 args:

[-s] the folder containing the source csv files

[-o] the folder that place all outputs. The output will be in the folder 'rumors' under the path in -o. The default value will be the folder contains rumorDetector_readall.py

[-t] the path of the input txt. The format of txt is the same as rumorDetector.py

sample use:
```
python rumorDetector_readall.py -s=sample_path -o=sample_out_path -t=sample.txt
```

## EnglishFilter.py

This script can filter out English content in the csv file

2 args:

[-s] the folder containing the source csv file

[-o] (default None) the folder of the output. If is None, the output folder will be made under the source folder.

sample use:
```
python EnglishFilter.py -s=sample_path
```
