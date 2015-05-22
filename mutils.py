import math
from operator import mul

from consts import get_MRCI, get_CR_limit, get_GCI_limit


def __check_matrix(matrix):
	"""
	Method to check that "matrix" is real square matrix.
	"""
	if not hasattr(matrix, "__getitem__"):
		raise Exception("Matrix is not iterable")

	if not all(hasattr(row, "__getitem__") for row in matrix):
		raise Exception("Matrix is not iterable")

	if not all(len(row) == len(matrix) for row in matrix):
		raise Exception("Matrix is square")


def eigenvector_method(matrix, eps=1e-3, iterations_limit=1e6):
	"""
	Iterations method to find maximal eigen value
	and corresponding eigen vector.
	"""
	__check_matrix(matrix)

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

	return CR, x1, CR <= get_CR_limit(size)


def additive_normalization(matrix):
	"""
	Additive Normalization (AN) method to find local weights
	"""
	__check_matrix(matrix)

	size = len(matrix)

	weights = [1 / sum(matrix[i][j] for i in xrange(size)) for j in xrange(size)]

	HM = size / sum(w for w in weights)
	HCI = (HM - size) * (size + 1) / (size * (size + 1))
	HCR = HCI / get_MRCI(size)
	
	return HCR, weights, HCR <= get_CR_limit(size)


def row_geometric_mean_method(matrix):
	"""
	RGM method to find local weights
	"""
	__check_matrix(matrix)

	size = len(matrix)

	v = [1 for _ in xrange(size)]
	for line in matrix:
		for i in xrange(size):
			v[i] *= line[i]

	for i in xrange(size):
		v[i] = v[i] ** (1. / size)

	weights = [x / sum(v) for x in v]

	GCI = 2 * sum(math.log(matrix[i][j] * v[j] / v[i]) ** 2 for j in xrange(i + 1, size) for i in xrange(size)) / (size - 1) / (size - 2)

	return GCI, weights, GCI <= get_GCI_limit(size)


def __calc_global_common(hier, local_weigths, f_norm):
	"""
	Distributive method to calculate global weigths
	"""
	normed_weights = dict((item, f_norm(x)) for (item, x) in local_weigths.iteritems())

	target = hier[0][0]

	global_weights = {}
	global_weights[target] = 1.0

	for i in xrange(len(hier)):
		child_count = len(normed_weights[hier[i][0]])
		if i + 1 < len(hier):
			for k, item in enumerate(hier[i + 1]):
				global_weights[item] = sum(normed_weights[parent][k] * global_weights[parent] for parent in hier[i])
		else:
			result = [0 for _ in xrange(child_count)]
			for k in xrange(child_count):
				result[k] = sum(normed_weights[parent][k] * global_weights[parent] for parent in hier[i])

	return __norm_sum(result)


def __norm_sum(vec):
	return [x / sum(vec) for x in vec]


def __norm_max(vec):
	return [x / max(vec) for x in vec]


def distributive_global_calc(hier, local_weigths):
	return __calc_global_common(hier, local_weigths, __norm_sum)


def ideal_global_calc(hier, local_weigths):
	return __calc_global_common(hier, local_weigths, __norm_max)


def multiplicative_global_calc(hier, local_weigths):
	target = hier[0][0]

	global_weights = {}
	global_weights[target] = 1.0

	for i in xrange(len(hier)):
		child_count = len(local_weigths[hier[i][0]])
		if i + 1 < len(hier):
			for k, item in enumerate(hier[i + 1]):
				global_weights[item] = reduce(mul, (local_weigths[parent][k] ** global_weights[parent] for parent in hier[i]), 1)
		else:
			result = [0 for _ in xrange(child_count)]
			for k in xrange(child_count):
				result[k] = reduce(mul, (local_weigths[parent][k] ** global_weights[parent] for parent in hier[i]), 1)

	return __norm_sum(result)
