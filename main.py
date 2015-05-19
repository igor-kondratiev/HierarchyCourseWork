import os

from mutils import additive_normalization, eigenvector_method, row_geometric_mean_method
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

def ensure_dir(path):
	if not os.path.exists(path):
		os.mkdir(path)

def read_matrix(filename):
	matrix = []
	with open(filename, "r") as f:
		for line in f:
			matrix.append(list(map(float, line.strip().split(","))))

	return matrix

def save_matrix_file(matrix, filename):
	with open(filename, "w") as f:
		for line in matrix:
			f.write("{0}\n".format(", ".join("{0:.2f}".format(x) for x in line)))

def main():
	ensure_dir("results")
	ensure_dir("results/matrixes")

	matrixes = {}
	for i, level in enumerate(HIERARCHY):
		for item in level:
			if os.path.exists("input/{0}.txt".format(item.lower())):
				matrixes[item] = read_matrix("input/{0}.txt".format(item.lower()))
				save_matrix_file(matrixes[item], "results/matrixes/{0}.txt".format(item.lower()))
				continue

			size = ALTERNATIVES_COUNT if i == len(HIERARCHY) - 1 else len(HIERARCHY[i + 1])
			matrixes[item] = generate_matrix_file(size, "results/matrixes/{0}.txt".format(item.lower()))

	ensure_dir("results/local_weights")

	local_weights = {"EM": {}, "AN": {}, "RGMM": {}}
	for level in HIERARCHY:
		for item in level:
			CR, local_weights["EM"][item], consist = eigenvector_method(matrixes[item])
			save_vector_file(local_weights["EM"][item], "results/local_weights/{0}_EM.txt".format(item.lower()))
			if not consist:
				print "ERROR: matrix for {0} is inconsistent by CR: {1}".format(item, CR)

			HCR, local_weights["AN"][item], consist = additive_normalization(matrixes[item])
			save_vector_file(local_weights["AN"][item], "results/local_weights/{0}_AN.txt".format(item.lower()))
			if not consist:
				print "ERROR: matrix for {0} is inconsistent by HCR: {1}".format(item, HCR)

			GCI, local_weights["RGMM"][item], consist = row_geometric_mean_method(matrixes[item])
			save_vector_file(local_weights["RGMM"][item], "results/local_weights/{0}_RGMM.txt".format(item.lower()))
			if not consist:
				print "ERROR: matrix for {0} is inconsistent by GCI: {1}".format(item, GCI)
			
			with open("results/local_weights/{0}_consistency.txt".format(item.lower()), "w") as f:
				f.write("CR: {0:.3f}\n".format(CR))
				f.write("HCR: {0:.3f}\n".format(HCR))
				f.write("GCI: {0:.3f}\n".format(GCI))

	# norming all local weights
	for v in local_weights["EM"].itervalues():
		s = sum(v)
		for i in xrange(len(v)):
			v[i] /= s

	# calculating global weights
	g_weights = {}
	for item in HIERARCHY[-1]:
		g_weights[item] = local_weights["EM"][item][:]

	for i in reversed(xrange(1, len(HIERARCHY))):
		for head in HIERARCHY[i - 1]:
			g_weights[head] = [0 for _ in xrange(ALTERNATIVES_COUNT)]
			for j in xrange(ALTERNATIVES_COUNT):
				for k, item in enumerate(HIERARCHY[i]):
					g_weights[head][j] += local_weights["EM"][head][k] * g_weights[item][j]

			s = sum(g_weights[head])
			for k in xrange(ALTERNATIVES_COUNT):
				g_weights[head][k] /= s

	save_vector_file(g_weights["Target"], "results/global.txt")

if __name__ == '__main__':
	main()
