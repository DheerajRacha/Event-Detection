import numpy as np
import time, sys, os

class cluster:

	def __init__(self):
		self.create_new_cluster()
		return

	def nodes(self):
		return self.nodes

	def node_frequencies(self):
		return self.node_frequencies

	def words(self):
		return self.words

	def word_frequencies(self):
		return self.word_frequencies

	def create_new_cluster(self):
		self.nodes, self.node_frequencies = [], []
		self.words, self.word_frequencies = [], {}
		return 


	def add_stream(self,stream):
		for node in stream['nodes']:
			if node in self.nodes:
				self.node_frequencies[self.nodes.index(node)] = self.node_frequencies[self.nodes.index(node)] + 1
			else:
				self.nodes.append(node)
				self.node_frequencies.append(1)

		for i,word in enumerate(stream['words']):
			if word in self.words:
				self.word_frequencies[word] = self.word_frequencies[word] + stream['word_frequencies'][i]
			else:
				self.words.append(word)
				self.word_frequencies[word] = stream['word_frequencies']
		return 

