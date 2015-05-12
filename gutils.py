import random


_FUNDAMENTAL_SCALE = (1./9, 1./8, 1./7, 1./6, 1./5, 1./4, 1./3, 1./2, 1., 2., 3., 4., 5., 6., 7., 8., 9., )

def closest_to_scale(value):
	return min(_FUNDAMENTAL_SCALE, key = lambda x : abs(x - value))

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

def generate_matrix_by_weights(size):
    weights = []
    matrix = []
    for i in xrange(size):
        matrix.append([None] * size)
        weights.append(None)
        matrix[i][i] = 1
        weights[i] = random.random()

    for i in xrange(0, size):
        for j in xrange(i + 1, size):
            matrix[i][j] = closest_to_scale(weights[i] / weights[j])
            matrix[j][i] = closest_to_scale(1. / matrix[i][j])

    return matrix

def generate_matrix_file(size, filename):
	matrix = generate_matrix_by_weights(size)
	with open(filename, "w") as f:
		for line in matrix:
			f.write("{0}\n".format(", ".join("{0:.2f}".format(x) for x in line)))

	return matrix