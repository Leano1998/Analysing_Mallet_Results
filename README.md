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

It is important to now, that this file generates the word-clouds based on the diagnostics file of the mallet
topic-modelling, so you'll need enter the full path to this file (so it'll be easier, if it's in the same directory.)

If you want to change variables like the maximum number of words displayed or the size of the plot, you can do this in 
line 77 and following.
