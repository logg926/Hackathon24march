
# coding: utf-8

# In[1]:


import requests
import subprocess
import pandas as pd
from pandas.io.json import json_normalize
import json
import os
import re
from collections import Counter
import nltk
from nltk.tokenize import TweetTokenizer
from nltk import word_tokenize
import numpy as np
import copy
import inflect
import string
demo = True;




# In[2]:


command = 'curl -X GET --header "Accept: application/json" --header "Authorization: Bearer 9172ad8e21e155a3332151de93fa86bd" "https://datastudio-api.hkstp.org:443/scmparticlessample/v1.0/datastore_search?resource_id=0e27027d-ef86-4d03-ba99-3bb0fafec3f9"'
command = command[:5] + '-k ' + command[5:] + ' -o ' + 'temp.json'
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
filename = 'api.json'

a = 'records'
b = 'result'

with open('temp.json', 'r', encoding='utf-8') as handle:
    parsed = json.load(handle)
if(b != ''):
	parsed = parsed[b]

df = pd.DataFrame(parsed[a])
dict_columns = list(parsed[a][0].keys())
if(a != ''):
	df = pd.DataFrame(parsed[a])
else:
	df = pd.DataFrame(parsed)

df = pd.DataFrame(parsed[a])
df = df[dict_columns]
#df.to_csv(filename[:-5] + '.csv', index=False)
#display(df)

r = len(df.index)
df['PWeighting'] = 0
df['VUnique'] = 0
df['Pageviews'] = df['Pageviews'].str.replace(',','')
df['UniqueVistors'] = df['UniqueVistors'].str.replace(',','')
#print(df['Pageviews'])
df['Pageviews'] = pd.to_numeric(df['Pageviews'])
df['UniqueVistors'] = pd.to_numeric(df['UniqueVistors'])
df['Title'] = df['Title'].str.replace("'",'')
#display(df)


# In[3]:


pageviews_mean = df['Pageviews'].mean()
uniquevistors_mean = df['UniqueVistors'].mean()
#print(df['Pageviews'].mean())
#print(df['UniqueVistors'].mean())
#print(df[['Pageviews', 'UniqueVistors']])
#print(uniquevistors_mean)
for x in range(0,r):
    #df.loc[x, 'PWeighting'] = 1
    
    if df.loc[x, 'Pageviews'] > pageviews_mean:
        df.loc[x, 'PWeighting'] = 1.1
    else:
        df.loc[x, 'PWeighting'] = 0.9
    if df.loc[x, 'UniqueVistors'] > uniquevistors_mean:
        df.loc[x, 'VUnique'] = 1.1
    else:
        df.loc[x, 'VUnique'] = 0.9
    
    #print(df.loc[x, 'PWeighting'])
    #print(df.loc[x])
#print(df[['PWeighting', 'VUnique']])
#display(df)


# In[4]:


c = [[]]
c.pop(0)
#print(c)
model = ['IAB_en', 'IPTC_en', 'SocialMedia_en']
#print(len(model))
if demo != True:
    for run in range(len(model)):
        c.clear()
        for x in range(0,r):
            url = "http://api.meaningcloud.com/class-1.1"

            payload = 'key=4c7a17701b4b126a0b755d56fd31a291&title="' + df.loc[x, 'Title'] + '"&txt="' + df.loc[x, 'Descriptions'] + '"&model=' + model[run]
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            #print(payload)
            response = requests.request("POST", url, data=payload, headers=headers)
            #print(response.text)
            #response = '{"status":{"code":"0","msg":"OK","credits":"1","remaining_credits":"19988"},"category_list":[{"code":"Travel","label":"Travel","abs_relevance":"1","relevance":"100"},{"code":"Society","label":"Society","abs_relevance":"1","relevance":"100"}]}'
            cate_list = json.loads(response.text)
            d = 'category_list'
            df_r = pd.DataFrame(cate_list[d])
            #print(df_r)
            print('still running', x, model[run])
            cate_list1 = []
            if df_r.empty == True:
                cate_list1 = ['Uncategorized']
            else:
                cate_list1 = df_r['label'].tolist()
            c.append(cate_list1)
        print(c)
        df[model[run]] = c
else:
    df = pd.read_csv('demo.csv')
#display(df)


# In[5]:


df['combinecate'] = str
for x in range(0,r):
    if df.loc[x, 'IAB_en'] == "['Uncategorized']" :
        df.loc[x, 'IAB_en'] = ''
    if df.loc[x, 'IPTC_en'] == "['Uncategorized']":
        df.loc[x, 'IPTC_en'] = ''
    if df.loc[x, 'SocialMedia_en'] == "['Uncategorized']":
        df.loc[x, 'SocialMedia_en'] = ''
    df.loc[x, 'combinecate'] = df.loc[x, 'IAB_en'] + df.loc[x, 'IPTC_en'] + df.loc[x, 'SocialMedia_en']
    #print('hehe')
#display(df)


# In[6]:


#text = "['Law, Govt & Politics>Legal Issues']['human interest - award and prize', 'arts, culture and entertainment - literature', 'crime, law and justice - judiciary (system of justice)', 'sport - soccer']['art and culture']"
count = Counter()
df['string'] = ''
for i in range(0,r):
    tknzr = TweetTokenizer()
    token = tknzr.tokenize(df.loc[i,'combinecate'])
    token = [tokens.lower() for tokens in token]
    #print(token)
    nonPunct = re.compile('.*[A-Za-z0-9].*')  # must contain a letter or digit
    filtered = [w for w in token if nonPunct.match(w)]
    df.loc[i, 'string'] = ''.join(filtered)
    count += Counter(filtered)
#df.to_csv('count_useful.csv')
#display(df)
df_count = pd.DataFrame.from_dict(count, orient='index').reset_index()
df_count.columns = ['words','freq']
df_count.sort_values('freq')
p = inflect.engine()
for i in range(0,len(df_count.index)):
    #print(p.singular_noun(df_count.loc[i, 'words']), df_count.loc[i, 'words'])
    if p.singular_noun(df_count.loc[i, 'words']) != False:
        df_count.loc[i, 'words'] = p.singular_noun(df_count.loc[i, 'words'])
    if df_count.loc[i, 'words'] == 'govt':
        df_count.loc[i, 'words'] = 'government'
#print(p.singular_noun('logistics'))


df_count.sort_values('freq',ascending = False)
#print(df_count['words'])
#print(df_count)
drop_list = ['and', 'or', 'unrest', 'me', 'of', 'out', 'is', 'he', 'she', 'it']
df_count = df_count.groupby('words',as_index=False).agg({'freq': 'sum'})
#print(df_count.columns)
df_count = df_count[~df_count['words'].isin(drop_list)]

#print(df_count['words'])


#df_count[~df_count['words'].str.contains("and")]

#df_count.to_csv('count.csv')
#display(df_count)
#display(df)


# In[7]:


df_count['weighting'] = 1.0
df_count['result'] = 1
df_count = df_count.reset_index(drop=True)
#display(df_count)
for x in range(0,len(df_count.index)):
    for y in range(0, len(df.index)):
#         print(type(df_count.loc[x,'words']), x , y)
#         print(df_count.loc[x,'words'])
#         print(type(df.loc[y,'string']))
#         print(type(df.loc[y, 'PWeighting']))
        if df_count.loc[x,'words'] in df.loc[y,'string']:
            df_count.loc[x, 'weighting'] *= df.loc[y, 'PWeighting'] * df.loc[y, 'VUnique']
for x in range(0,len(df_count.index)):
    df_count.loc[x, 'result'] = df_count.loc[x, 'weighting'] * df_count.loc[x, 'freq']

#    df_count.loc[x, 'output'] = df_count.loc[x, 'result']
#df_count.loc['output'] = pd.to_numeric(df_count['output'], downcast='signed')
#display(df_count)
#df_output = pd.DataFrame[df_count['words'],df_count['result']]
#display(df_output)
#print(df_count.columns)
df_new = df_count.drop(columns = ['freq', 'weighting'])
#print(df_new.columns)

output = df_new['result']
#output.append(df_new['result'])

df_output = df_new.nlargest(40,'result')
output_string = 'data = { "category" : ' + df_output['words'].to_json(orient = 'values') + ', "score": ' + df_output['result'].to_json(orient = 'values') + '};'
#print(output_string)
with open('test.js', 'w') as f:
    f.write(output_string)
#df_count['UniqueVistors'] = pd.to_numeric(df['UniqueVistors'])
        

