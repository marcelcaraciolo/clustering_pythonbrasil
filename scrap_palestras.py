#-*-coding:utf-8-*-


#Pegar os dados das palestras do python Brasil
#Jogar tudo isso em um banco de dados

__author__ = 'Marcel Caraciolo'

import os, re, sys
from Queue import Queue
from BeautifulSoup import BeautifulSoup
import urllib2, urllib
from pymongo import Connection
import pickle




class PythonBrasilScraper(object):
	
	def __init__(self,http_client= urllib2):
		self.url = 'http://www.pythonbrasil.org.br/2010/resultado_avaliacao'
		self.http_client  = http_client
		self.opener = self.http_client.build_opener()
		self.tags_pattern = re.compile(r"<td>(.*)</td>")
		self.span_pattern = re.compile(r"<span>(.*)</span>")
		
		self.headers = {}
	
	
	def parseDetalhesPalestra(self, url):
		request = self.opener.open(url)
		data = request.read()
		soup = BeautifulSoup(data)
		result =  soup.findAll('p')
		
		nivel = self.span_pattern.findall(str(result[2].findAll('span')[0] ) ) [0] 	
		resumo =  result[3].contents[0]
		cidade =  result[4].contents[0].encode('utf-8')
		
		return {'nivel': nivel , 'cidade': cidade, 'resumo': resumo}
				
	def parsePalestras(self):
		request = self.opener.open(self.url)
		data = request.read()
		soup = BeautifulSoup(data)
		resp = soup.findAll('tr',{'class':['even'] })
		palestras = []
		for palestra in resp[6:]:
			pl = {}
			
			info =  palestra.findAll('td')
			
			url = info[1].findAll('a')[0]['href']
			dados = self.parseDetalhesPalestra(url)
			pl.update(dados)
			pl['titulo'] = info[1].findAll('a')[0].contents[0].encode('utf-8')		
			pl['tags'] =  self.tags_pattern.findall(str(info[2]))[0]
			pl['palestrante'] = self.tags_pattern.findall(str(info[3]))[0]
			pl['pontos'] = self.tags_pattern.findall(str(info[4]))[0]
			
			
			print pl['titulo']
			print pl['resumo']
			
			#a = raw_input()
			#pl['keys'] = a
			
			palestras.append(pl)
			
		return palestras
			


if __name__ == '__main__':
	info = PythonBrasilScraper()
	palestras = info.parsePalestras()
	#output = open('palestrasData.pk1','wb')
	#pickle.dump(palestras,output)
	#output.close()
	print len(palestras)