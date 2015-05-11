import random


_FUNDAMENTAL_SCALE = (1./9, 1./8, 1./7, 1./6, 1./5, 1./4, 1./3, 1./2, 1., 2., 3., 4., 5., 6., 7., 8., 9., )


def generate_matrix(size):
	"""
	Generate consistent pairs comparing matrix (PCM)
	"""
	matrix = []

	for i in xrange(size):
		matrix.append([None] * size)
		matrix[i][i] = 1

	# first row generation
	for i in xrange(1, size):
		matrix[0][i] = random.choice(_FUNDAMENTAL_SCALE)
		matrix[i][0] = 1. / matrix[0][i]

	for i in xrange(1, size):
		for j in xrange(1, size):
			if i == j:
				continue

			matrix[i][j] = matrix[i][0] * matrix[0][j]

	return matrix