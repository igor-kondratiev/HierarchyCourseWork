import math


def eigenvector_method(matrix, eps=1e-3, iterations=1e6):
	"""
	Iterations method to find maximal eigen value
	and corresponding eigen vector.
	"""
	# TODO: check matrix
	size = len(matrix)

	x0 = [0. for _ in xrange(size)]
	x1 = [1. for _ in xrange(size)]
	while math.sqrt(sum(abs(x0[i] - x1[i]) for i in xrange(size))) > eps:
		x0[:] = x1[:]

		for i in xrange(size):
			x1[i] = 0.
			for j in xrange(size):
				x1[i] += matrix[i][j] * x0[j]

		norm_x = sum(abs(x) for x in x1)
		for i in xrange(size):
			x1[i] /= norm_x

	# TODO: implement MRCI
	return x1

def additive_normalization(matrix):
	"""
	Additive Normalization (AN) method to find local weights
	"""
	# TODO: check matrix
	size = len(matrix)

	weights = [1 / sum(matrix[i][j] for i in xrange(size)) for j in xrange(size)]

	# TODO: implement HRCI
	return weights


