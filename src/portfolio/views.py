from django.shortcuts import render
import datetime
import requests
import json
import pandas as pd
from django.http import HttpResponse
import sqlite3
import numpy as np
from collections import defaultdict
import statsmodels.tsa.stattools as ts 
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import View, ListView, DetailView, TemplateView

from .forms import contactForm

numTradingDays = 255

def pairs(request):
	form = contactForm(request.POST or None)

	if form.is_valid():
		pairs, data = findPairs(form.cleaned_data)
		template = 'portfoliohtml/pairsLoad.html'
		return render(request, template, {'pair' : pairs, 'data_new' : data})

	template = 'portfoliohtml/pairs.html'
	return render(request, template, {'form': form})



def findPairs(dictionary):
	connection = sqlite3.connect('finance.db')
	c = connection.cursor()

	new = (dict(dictionary))


	c.execute('SELECT stock, close FROM stocks')
	data = c.fetchall()
	print(data[1])
	d = defaultdict(list)
	for k, v in data:
		d[k].append(v)

	df  = pd.DataFrame(data=d)
	df2 = df.ix[:, : 10]


	scores, pvalues, pairs = find_cointegrated_pairs(df2)
	pairs = [x for t in pairs for x in t]
	priceDict = {}
	for i in pairs:
		priceDict[i] = d[i]


	c.execute('SELECT day FROM stocks LIMIT 255')
	dates = c.fetchall()
	dates = [i[0] for i in dates]

	totalArr = []
	for k, v in priceDict.items():
		totalArr.append(v)


	new = []
	for i in totalArr:
		list_of_dict = [{'date': dates, 'price': i} for (dates,i) in zip(dates,i)]
		new.append(list_of_dict)

	for i in new:
		


	# mae list of jsonarrays

	return pairs, new

	



def find_cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = ts.coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.10:
                pairs.append((keys[i], keys[j]))
    return score_matrix, pvalue_matrix, pairs


def zscore(series):
    return (series - series.mean()) / np.std(series)


def pairsLoaded(request):
	
	template = 'portfoliohtml/pairsLoaded.html'
	return render(request, template, context)



def portfolio(request):
	context = locals()
	template = 'portfoliohtml/base.html'
	return render(request, template, context)

def home(request):
	context = locals()
	template = 'portfoliohtml/base.html'
	create_table()
	return render(request, template, context)

def create_table():

	try:
		connection = sqlite3.connect('finance.db')
		c = connection.cursor()
		c.execute('SELECT * FROM stocks')
		

	except:
		print('l')
		connection = sqlite3.connect('finance.db')
		c = connection.cursor()


		df = pd.read_csv('constituents.csv')
		sp = df['Symbol']
		
		c.execute('''CREATE TABLE IF NOT EXISTS stocks
		(change FLOAT, changeOverTime FLOAT, changePercent FLOAT, close FLOAT, day DATE, high FLOAT, label TEXT, low FLOAT, open FLOAT, unadjustedVolume INTEGER, volume INTEGER, vwap FLOAT, stock TEXT)''')

		for i in sp:
		
			url = 'https://api.iextrading.com/1.0/stock/'+i+'/chart/1y'
			source = requests.get(url)
			sourceContentByte = source.content.decode()
			sourceContent = json.loads(sourceContentByte)
			df2 = pd.DataFrame(sourceContent)
			df2['stock'] = i
			print(len(df2))
			if len(df2) == numTradingDays:
				for index, row in df2.iterrows():
					c.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)


		connection.commit()
		print('yup')





