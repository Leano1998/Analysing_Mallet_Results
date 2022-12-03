# Analysing the results of a mallet topic-modelling

This repository tries to help analysing the results of a mallet topic modelling. Therefore, it takes certain
mallet-export files like the diagnostics-file, the output-doc-topics file or others.

## Word-Clouds

The script [`topic_cloud.py`](topic_cloud.py) uses the python-libraries `pandas`, `matplotlib`, `BeautifulSoup` and
`wordlcoud` to create black and white word-clouds for the different topics of the modell. 
You might need to install the missing packages before running the script with:
```
python3 -m pip install --upgrade pip
python3 -m pip install pandas matplotlib wordcloud bs4
```
Then navigate with the shell or terminal into the directory where the `topic_cloud.py` script is and run `python3
topic_cloud.py`. After this just follow the given instructions.

It is important to now, that this file generates the word-clouds based on the diagnostics file (mallet-parameter: 
`diagnostics-file`) of the mallet
topic-modelling, so you'll need enter the full path to this file (so it'll be easier, if it's in the same directory.)

If you want to change variables like the maximum number of words displayed or the size of the plot, you can do this in 
line 77 and following.


## Topics over time

The script[`topic_over_time.py`](topic_over_time.py) can be used to visualize one ore more topics over time. Therefore,
the document names must include some kind of time-information. this can either be a two-digit volume-number or a
four-digit year number. 

This script uses the libraries `seaborn`, `matpoltlib`, `pandas` and `re`. While `re` is normally preinstalled, the
other libraries, might still have to be installed.
```
python3 -m pip install --upgrade pip
python3 -m pip install pandas matplotlib seaborn
```
You can run the script the same way as topic_cloud.py, by typing `python3 topic_cloud.py` (you must be in the same
directory with your shell or terminal).

The script `topic_over_time.py` uses the doc-topic-distribution file of mallet, which can be exported by including the
parameter `output-doc-topics` followed by a file-name into the mallet call. You'll need enter the full path to this file
(so it'll be easier, if it's in the same directory.)
