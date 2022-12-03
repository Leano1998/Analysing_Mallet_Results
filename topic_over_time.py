import sys

from seaborn import lineplot, set_theme
import matplotlib.pyplot as plt
import pandas as pd
import re

set_theme(style="whitegrid")

df = None
name = ""
while df is None:
    name_input = input('Please insert the name (and path) of the mallet topic-doc-distribution file: ')
    name = name_input if name_input != '' else name
    try:
        df = pd.read_csv(name, sep='\t', encoding='utf8', header=None)
    except FileNotFoundError:
        print('No File with name %s in the current folder' % name)
        df = None

n_topics = len(df.columns) - 2
df.columns = ['id', 'dokument'] + ['Topic %s' % i for i in range(n_topics)]
##############################################
# Extracting the information about the years.#
##############################################

print('For a correct display of the year-distribution, the time-information must exist in the documents names. This can'
      ' either be through volumen numbers in the format NN (01, 02, ..., 12, ...) or in form of clear year information.'
      ' The second options more stable. The algorithm is looking for 4-digit numbers in the document names.\n')
time_form = None
first_vol = None
while time_form is None:
    inp = input('Shoul\'d the time information be determined by year or volumen (type "year" or "volume")? ')
    if inp in ('Year', 'year'):
        time_form = 'year'
        print('Okay, time-information will be determined by year.')
    elif inp in ('vol', 'Vol', 'volume', 'Volume'):
        time_form = 'vol'
        first_vol = None
        while first_vol is None:
            first_vol = input('Please enter the year of the first volume: ')
            try:
                first_vol = int(first_vol)
            except ValueError:
                print('The input has to be a number.')
                first_vol = None
        print('Okay, time-information will be determined by volume, beginning in year %i.' % first_vol)
    else:
        print('Unfortunately, no time information coul\'d be determined. Please try again.')

years = []
if time_form == 'vol':
    for d in df["dokument"]:
        try:
            volume = int(re.findall(r'[0-9][0-9]', d)[0])
        except IndexError:
            print('\n\tCouldn\'t parse document-name: "%s".\n' % d)
            sys.exit("Please check %s file for wrong document names." % name)
        year = first_vol + volume
        years.append(year)
    df['year'] = years
    df = df[['id', 'year', 'dokument'] + ['Topic %s' % i for i in range(len(df.columns) - 3)]].sort_values(
        by=['year', 'dokument'])
elif time_form == 'year':
    for d in df["dokument"]:
        try:
            year = int(re.findall(r'[1-9][0-9][0-9][0-9]', d)[0])
        except IndexError:
            print('\n\tCouldn\'t parse document-name: "%s".\n' % d)
            sys.exit("Please check %s file for wrong document names." % name)
        years.append(year)
    df['year'] = years
    df = df[['id', 'year', 'dokument'] + ['Topic %s' % i for i in range(len(df.columns) - 3)]].sort_values(
        by=['year', 'dokument'])

# updating the document names, if possible
if '/' in df['dokument'].tolist()[0]:
    documents = []
    for _, v in df.iterrows():
        documents.append(v['dokument'].split('/')[-1])
    df["dokument"] = documents
#######################################
#   Visualizing topic(s) over years   #
#######################################
tm_list = -1
while type(tm_list) is not list:
    tm_list = input('Please insert the topic numbers, of the topics to visualize(number or comma separated): ')
    if ',' in tm_list:
        tm_list = list(map(lambda x: x.strip(), tm_list.split(',')))
    else:
        tm_list = [tm_list]
    try:
        tm_list = [int(i) for i in tm_list]
        tm_list = list(filter(lambda x: 0 <= x < n_topics, tm_list))
    except ValueError:
        print('Only numbers allowed!')
        tm_list = -1

tm_list = set(tm_list)

topic_year = df.groupby(by='year', as_index=False).mean()[['year'] + ['Topic %i' % i for i in tm_list]]
print(topic_year)
for t in ['Topic %i' % i for i in tm_list]:
    lineplot(data=topic_year, y=t, x='year', label=t)
plt.legend()
plt.ylabel('Topics')
plt.show()
