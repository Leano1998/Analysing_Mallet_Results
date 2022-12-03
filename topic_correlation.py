import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import sys

################################################
#   Standard workflow for importing the data   #
################################################
sns.set_theme(style="whitegrid")
df = None
name = ""
while df is None:
    name_input = input('Please insert the name (and path) of the mallet topic-doc-distribution file: ')
    name = name_input if name_input != '' else name
    name = name.strip()
    try:
        df = pd.read_csv(name, sep='\t', encoding='utf8', header=None)
    except FileNotFoundError:
        print('No File with name "%s" in the current folder' % name)
        df = None

n_topics = len(df.columns) - 2
df.columns = ['id', 'dokument'] + ['Topic %s' % i for i in range(n_topics)]
##############################################
# Extracting the information about the years.#
##############################################

vol_pattern = r'[0-9][0-9]?'
"""
    The pattern to determine the volume of a document.
"""

print('For a correct display of the year-correlation, the time-information must exist in the documents names. This can'
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
            volume = int(re.findall(vol_pattern, d)[0])
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

df.pop('dokument')
df.pop('id')
df = df.groupby(by='year', as_index=False).mean()
df.pop('year')
print(df)

##########################################
#   Calculating the topic-correlations   #
##########################################

topic_corr = np.corrcoef([df[t] for t in list(df)])

print(pd.DataFrame(topic_corr))

plt.rcParams["figure.figsize"] = (12, 12)
sns.heatmap(pd.DataFrame(topic_corr), xticklabels=True, vmin=-1, vmax=1, yticklabels=True)
plt.show()

inp = input('Do you want to visualize certain correlations? (y, n)')
while inp not in ('N', 'n'):
    x = int(input('Please insert the number of the topic for the x-axe: '))
    y = int(input('Please insert the number of the topic for the y-axe: '))
    sns.scatterplot(x=df['Topic %i' % x], y=df['Topic %i' % y])

    f = lambda z: (z * topic_corr[x][y]) + (0 if topic_corr[x][y] >= 0 else (topic_corr[x][y] * -1) / 2)
    step = 0.01
    rng = [i * step for i in range(int(max(df['Topic %i' % x]) / step))]
    sns.lineplot(x=rng, y=list(map(f, rng)), label='correlation=%s' % topic_corr[x][y])
    plt.xlabel('Topic %i' % x)
    plt.ylabel('Topic %i' % y)
    print(topic_corr[x][y])
    plt.legend()
    plt.show()
    inp = input('Do you want to visualize more correlations? (y, n)')
