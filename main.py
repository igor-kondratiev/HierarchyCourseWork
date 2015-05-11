from mutils import additive_normalization, eigenvector_method


def main():
	matrix = [
		[1.,   3.,    4.  , 4./7 ],
		[1./3, 1.,    4./3, 4./21],
		[1./4, 3./4,  1.  , 1./7 ],
		[7./4, 21./4, 7.,   1,   ]
	]
	print additive_normalization(matrix)
	print eigenvector_method(matrix)

if __name__ == '__main__':
	print "Hello"
	main()
