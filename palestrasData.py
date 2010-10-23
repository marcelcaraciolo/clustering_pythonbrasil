#Mineracao de dados
import pickle
import nltk
import string
import operator
import unicodedata
import kmeans


normalize = lambda x:  unicodedata.normalize("NFKD", x).encode('ascii', 'ignore')

inp = open('palestrasData.pk1','rb')
dados = pickle.load(inp)




def getWords(text):
	#Parse the statuses and returns the list of words for each text
	
	#Create the stop words list
	stopwords_pt = nltk.corpus.stopwords.words('portuguese')
	stopwords_pt = map(lambda w: unicode(w, 'utf-8'), stopwords_pt)
	
	#Split the words by spaces
	words = text.split(" ")
	
	#Remove all illegal characters and convert to lower case
	RemoveWords = string.punctuation
	for item in RemoveWords:
		words = [word.replace(item,'') for word in words]
	words = map(normalize,words)
	words = filter(lambda word: not word.isdigit(), words)
	words = filter(lambda word: word != '', words)
	words = [word.lower() for word in words]
	words = filter(lambda word: not word in stopwords_pt, words)

	return words

palestrantes = []
keywords = []


for dado in dados:
	tags =[]
	#tags = getWords(dado['tags'].decode('utf-8'))
	keys = dado['keys'].split(',')
	tags.extend(keys)
	#nivel = normalize(dado['nivel'].decode('utf-8').lower())
	#tags.append(nivel)
	palestrante =  normalize(dado['palestrante'].decode('utf-8'))
	palestrantes.append(palestrante)
	tags = list(set(tags))
	keywords.append(tags)


wordList = []

for user in keywords:
	for tag in user:
		if tag not in wordList:
			wordList.append(tag)

keywords2 = []
i = 0
for user in keywords:
	keywords2.append([])
	for word in wordList:
		if word in user:
			keywords2[i].append((word,1))
		else:
			keywords2[i].append((word,0))
	i+=1

	
g = kmeans.open_ubigraph_server()
result,clusters = kmeans.kcluster(g,palestrantes,keywords2,k=8)

dataClusters = []
i = 0
for cluster in result:
	apCount = {}
	for indice in cluster:
		dados = keywords2[indice]
		for word,count in dados:
			apCount.setdefault(word,0)
			apCount[word]+= count
	words = apCount.items()
	words.sort(key=operator.itemgetter(1))
	words.reverse()
	print words
	print '====' 
	dataClusters.append(words[0:10])


kmeans.showResults(dataClusters)



#"""	



"""
f = open('saida2.txt','w')

for dado in dados:
	tags = getWords(dado['tags'].decode('utf-8'))
	keys = dado['keys'].split(',')
	tags.extend(keys)
	tgs = " ".join(tags)
	f.write(tgs)

f.close()
"""



"""
#PEGAR TOTAL DE VOTOS
estado_palestras = {}

for dado in dados:
	estado_palestras.setdefault(dado['cidade'].split('-')[1].replace(' ',''),0)
	estado_palestras[dado['cidade'].split('-')[1].replace(' ','')]+=1




matplotlib.rcParams['font.size'] = 20


labels = []
fracs = []
for it in estado_palestras.items():
	labels.append(it[0])
	fracs.append(it[1])
	
# make a square figure and axes
pylab.figure(1, figsize=(6,6))
ax = pylab.axes([0.1, 0.1, 0.8, 0.8])

explode=(0,) * len(labels)
pylab.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', colors=("b","g","r","y","c", "m", "w"), shadow=True)
pylab.title('Distribuicao de estados das Palestras', bbox={'facecolor':'1.0', 'pad':5})

pylab.show()

"""
