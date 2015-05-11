_MRCI = {
	1: 0.52,
	2: 0.52,
	3: 0.52,
	4: 0.89,
	5: 1.11,
	6: 1.25,
	7: 1.35,
	8: 1.40,
	9: 1.45,
	10: 1.49,
	11: 1.52,
	12: 1.54,
	13: 1.56,
	14: 1.58,
	15: 1.59,
}

def get_MRCI(n):
	if n <= 0:
		raise Exception("Matrix size must be positive")

	return _MRCI.get(n, 1.59)

_CR_LIMIT = {
	3: 0.05,
	4: 0.08,
	5: 0.1,
}

def get_CR_limit(n):
	if n <= 0:
		raise Exception("Matrix size must be positive")

	max_n, min_n = max(_CR_LIMIT.iterkeys()), min(_CR_LIMIT.iterkeys())
	n = min(max_n, max(n, min_n))

	return _CR_LIMIT[n]
