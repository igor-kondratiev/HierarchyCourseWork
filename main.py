import os

from mutils import additive_normalization, eigenvector_method
from gutils import generate_matrix_file


HIERARCHY = (
	("Target", ),
	("Price", "Comfort", "Safety"),
	("Fuel", "Quality", "Capacity", "Power"),
)

ALTERNATIVES_COUNT = 4


def save_vector_file(v, filename):
	with open(filename, "w") as f:
		f.write("{0}\n".format(", ".join("{0:.2f}".format(x) for x in v)))


def main():
	if not os.path.exists("results"):
		os.mkdir("results")

	matrixes = {}
	for i, level in enumerate(HIERARCHY):
		for item in level:
			size = ALTERNATIVES_COUNT if i == len(HIERARCHY) - 1 else len(HIERARCHY[i + 1])
			matrixes[item] = generate_matrix_file(size, "results/{0}.txt".format(item.lower()))

	local_weights = {}
	for level in HIERARCHY:
		for item in level:
			_, local_weights[item] = eigenvector_method(matrixes[item])
			save_vector_file(local_weights[item], "results/{0}_local_w.txt".format(item.lower()))

	# norming all local weights
	for v in local_weights.itervalues():
		s = sum(v)
		for i in xrange(len(v)):
			v[i] /= s

	# calculating global weights
	g_weights = {}
	for item in HIERARCHY[-1]:
		g_weights[item] = local_weights[item][:]

	for i in reversed(xrange(1, len(HIERARCHY))):
		for head in HIERARCHY[i - 1]:
			g_weights[head] = [0 for _ in xrange(ALTERNATIVES_COUNT)]
			for j in xrange(ALTERNATIVES_COUNT):
				for k, item in enumerate(HIERARCHY[i]):
					g_weights[head][j] += local_weights[head][k] * g_weights[item][j]

			s = sum(g_weights[head])
			for k in xrange(ALTERNATIVES_COUNT):
				g_weights[head][k] /= s

	print g_weights["Target"]


if __name__ == '__main__':
	main()
