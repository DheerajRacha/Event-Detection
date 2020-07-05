import numpy as np

class count_min_sketch:

	def __init__(self, epsilon, delta, input_data):

		"""
		Hyper Parameters
		"""
		self.input_data = input_data
		self.epsilon = epsilon
		self.delta = delta
		self.width = int(np.exp(1)/self.epsilon) + 1
		self.depth = int(np.log(1/self.delta)) + 1
		self.hashed_data = np.zeros((self.depth,self.height))

		
		## Hashing Functions generated randomly
		
		self.hash_fn = [] 
		for _ in range(self.depth):
			l = np.arange(self.width)
			random.shuffle(l)
			self.hash_fn.append(l)


		for i in range(len(self.input_data)):
			for j in range(self.depth):
				self.hashed_data[j][ self.hash_fn[j][i] ] = self.hashed_data[j][ self.hash_fn[j][i] ] + self.input_data[i]

		return
