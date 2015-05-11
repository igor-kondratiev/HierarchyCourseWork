import math
from consts import get_MRCI


def eigenvector_method(matrix, eps=1e-3, iterations_limit=1e6):
	"""
	Iterations method to find maximal eigen value
	and corresponding eigen vector.
	"""
	# TODO: check matrix
	size = len(matrix)

	x0 = [0. for _ in xrange(size)]
	x1 = [1. for _ in xrange(size)]

	iterations = 0
	while math.sqrt(sum(abs(x0[i] - x1[i]) for i in xrange(size))) > eps:
		iterations += 1
		if iterations_limit <= iterations:
			raise Exception("Iterations limit reached")

		x0[:] = x1[:]

		for i in xrange(size):
			x1[i] = 0.
			for j in xrange(size):
				x1[i] += matrix[i][j] * x0[j]

		norm_x = sum(abs(x) for x in x1)
		for i in xrange(size):
			x1[i] /= norm_x

	z = [0 for _ in xrange(size)]
	for i in xrange(size):
		for j in xrange(size):
			z[i] += matrix[i][j] * x1[j]

	eigen_value = sum(abs(x) for x in z) / sum(abs(x) for x in x1)
	
	CI = (eigen_value - size) / (size - 1)
	CR = CI / get_MRCI(size)

	return CR, x1

def additive_normalization(matrix):
	"""
	Additive Normalization (AN) method to find local weights
	"""
	# TODO: check matrix
	size = len(matrix)

	weights = [1 / sum(matrix[i][j] for i in xrange(size)) for j in xrange(size)]

	HM = size / sum(w for w in weights)
	HCI = (HM - size) * (size + 1) / (size * (size + 1))
	HCR = HCI / get_MRCI(size)
	
	return HCR, weights


