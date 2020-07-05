import numpy as np
import time, sys, os, csv
import argparse
from functions
from sklearn.metrics.pairwise import cosine_similarity

def FLAGS(args=sys.argv[1:]):
	parser = argparse.ArgumentParser()
	parser.add_argument("-alpha", default=0, type=float, help="Fractional Cluster Presence.")
	parser.add_argument("-delta", default=0, type=float, help="Count-Min Sketch.")
	parser.add_argument("-epsilon", default=0, type=float, help="Count-Min Sketch.")
	parser.add_argument("-num_clusters", default=4, type=int, help="Number of Clusters.")
	flags = parser.parse_args(args)
	return flags


class Event_Detection:
	
	def __init__(self, flags):
		self.flags = flags
		self.standard_deviation = 0
		self.mean = 0
		self.reader_words = self.read_words()
		self.reader_nodes = self.read_nodes()
		self.initialize_clusters()
		self.curr_num_clusters = 0
		return

	def initialize_clusters(self):
		self.clusters = [functions.cluster() for _ in range(self.flags.num_clusters)]
		return

	def read_words(self):
		data = {}
		with open("test_words.csv","r") as file :
			reader = csv.reader(file, delimiter = "\n")
			for i, line in enumerate(reader) :
				data['words'] = []
				data['word_frequencies'] = []
				l = line[0].split(',')
				for i in range(0,len(l)-1,2):
					data['words'].append(l[i])
					data['word_frequencies'].append(l[i+1])
				data['time_stamp'] = l[-1]
				yield data

	def read_nodes(self):
		data = {}
		with open("test_nodes.csv","r") as file :
			reader = csv.reader(file, delimiter = "\n")
			for i, line in enumerate(reader) :
				data['nodes'] = []
				l = line[0].split(',')
				for i in range(len(l)):
					data['nodes'].append(l[i])
				yield data

	def read_tweets(self) :
		A,B = next(self.reader_words), next(self.read_nodes)
		tweet = {}
		tweet['words'] = A['words']
		tweet['word_frequencies'] = A['word_frequencies']
		tweet['time_stamp'] = A['time_stamp']
		tweet['nodes'] = B['nodes']
		tweet['tf_idf'] = []
		return tweet

	def idf(self, word = None) :
		count = 0
		tf_count = np.zeros(self.curr_num_clusters)
		flag = np.zeros(self.curr_num_clusters)
		for index,cluster in enumerate(self.clusters):
			if word in cluster.words:
				##assuming cluster word frequency is a dict
				tf_count[index] = cluster.word_frequencies[word] #check type of word
				count = count + 1
				flag[index] = 1
		idf = np.log((self.curr_num_clusters + 1.0)/count)
		return idf, tf_count

	def content_similarity(self, stream):
		if self.curr_num_clusters == 0 :
			return -1

		similarities = []
		tf_idf_clusters = []
		idf_of_words = []
		for i in range(len(stream['words'])) :				
			idf, vector, x = self.idf(stream['words'][i])
			stream['tf_idf'].append(stream['word_frequencies'][i]*idf)
			tf_idf_clusters.append(x)
			idf_of_words.append(idf)

		for i in range(len(tf_idf_clusters)):
			tf_idf_clusters[i] = np.multiply(tf_idf_clusters[i], idf_of_words[i])
			
		for i in range(self.flags.num_clusters) :
			similarities.append(cosine_similarity(tf_idf_clusters[i], stream['tf_idf']))

		return similarities

	def structural_similarity(self, stream):
		if self.curr_num_clusters == 0 :
			return -1

		similarities = []
		for cluster in self.clusters:
			B = np.zeros(len(cluster.nodes))
			for i,node in enumerate(cluster.nodes):
				if node in stream['nodes']:
					B[i] = 1
			sim = np.sum(np.multiply(B,cluster.node_frequencies))/(np.sqrt(np.sum(stream['nodes'])+1)*np.sum(cluster.node_frequencies))
			similarities.append(sim)
		return similarities

	def assign_to_cluster(self, stream, structural_similarity, content_similarity):
		if self.content_similarity == -1 and self.structural_similarity == -1 :
			self.clusters[0].add_stream(stream)
			self.curr_num_clusters += 1
			self.update_moments(similarity)
			return

		similarity = max(self.Lambda*structural_similarity + (1-self.Lambda)*content_similarity)
		index = similarity.index(max(similarity))
		if similarity < (self.mean - 3*self.standard_deviation) : 
			if self.curr_num_clusters < 4 :
				self.clusters[curr_num_clusters - 1].add_stream(stream)
				self.curr_num_clusters += 1
			else : 
				#remove least active
		else :
			self.clusters[index].add_stream(stream)

		self.update_moments(similarity)
		return

	def update_moments(self, similarity):
		mean = mean * self.flags.num_clusters + similarity
		return
				

	def monitoring(self):
		self.initialize_clusters()
		while True:
			tweet = self.read_tweets()
			if tweet is None:
				break
			else :
				self.content_similarity()
				self.structural_similarity()
				self.assign_to_cluster()

		return


if __name__ == "__main__":

	flags = FLAGS()
	event_detection = Event_Detection()
	event_detection.monitoring()
