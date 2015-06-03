import math

from pulp import *

AL = [
	[1.,   3.,   6.,   6.],
	[1./4, 1.,   3.,   3.],
	[1./6, 1./4, 1.,   3.],
	[1./7, 1./4, 1./4, 1.],
]

AU = [
	[1.,   4.,   6.,   7.],
	[1./3, 1.,   4.,   4.],
	[1./6, 1./3, 1.,   4.],
	[1./6, 1./3, 1./3, 1.],
]

AM = None

def main():
	AM = []
	for i in xrange(len(AL)):
		AM.append([])
		for j in xrange(len(AL[0])):
			AM[i].append(math.sqrt(AL[i][j] * AU[i][j]))

	z1 = firstStep(AL, AM, AU)
	secondStep(AL, AM, AU, z1)
	eigenWeights(AM)

def firstStep(al, am, au):
	n = len(al)

	zl = []
	for i in xrange(n):
		zl.append([])
		for j in xrange(n):
			zl[i].append(LpVariable("zl_{0}_{1}".format(i, j), 0))

	zm = []
	for i in xrange(n):
		zm.append([])
		for j in xrange(n):
			zm[i].append(LpVariable("zm_{0}_{1}".format(i, j), 0))

	zu = []
	for i in xrange(n):
		zu.append([])
		for j in xrange(n):
			zu[i].append(LpVariable("zu_{0}_{1}".format(i, j), 0))

	yl = []
	for i in xrange(n):
		yl.append([])
		for j in xrange(n):
			yl[i].append(LpVariable("yl_{0}_{1}".format(i, j)))

	ym = []
	for i in xrange(n):
		ym.append([])
		for j in xrange(n):
			ym[i].append(LpVariable("ym_{0}_{1}".format(i, j)))

	yu = []
	for i in xrange(n):
		yu.append([])
		for j in xrange(n):
			yu[i].append(LpVariable("yu_{0}_{1}".format(i, j)))

	xl = []
	for i in xrange(n):
		xl.append(LpVariable("xl_{0}".format(i)))

	xm = []
	for i in xrange(n):
		xm.append(LpVariable("xm_{0}".format(i)))

	xu = []
	for i in xrange(n):
		xu.append(LpVariable("xu_{0}".format(i)))

	targetC = []
	for i in xrange(n):
		for j in xrange(i + 1, n):
			targetC.append((zl[i][j], 1))
			targetC.append((zm[i][j], 1))
			targetC.append((zu[i][j], 1))

	problem = LpProblem("First-step", LpMinimize)
	problem.setObjective(LpAffineExpression(targetC))

	for i in xrange(n):
		for j in xrange(n):
			if i != j:
				problem += xl[i] - xu[j] - yl[i][j] == math.log(al[i][j])
				problem += xm[i] - xm[j] - ym[i][j] == math.log(am[i][j])
				problem += xu[i] - xl[j] - yu[i][j] == math.log(au[i][j])

	for i in xrange(n):
		for j in xrange(i + 1, n):
			problem += zl[i][j] - yl[i][j] >= 0
			problem += zm[i][j] - ym[i][j] >= 0
			problem += zu[i][j] - yu[i][j] >= 0

			problem += zl[i][j] - yl[j][i] >= 0
			problem += zm[i][j] - ym[j][i] >= 0
			problem += zu[i][j] - yu[j][i] >= 0

	for i in xrange(n):
		problem += xl[i] - xm[i] <= 0
		problem += xm[i] - xu[i] <= 0

	for i in xrange(n):
		for j in xrange(n):
			problem += yl[i][j] - ym[i][j] <= 0
			problem += ym[i][j] - yu[i][j] <= 0

	problem += xl[0] == 0
	problem += xm[0] == 0
	problem += xu[0] == 0

	problem.writeLP("first_step.lp")

	problem.solve()

	zOpt = 0
	for i in xrange(n):
		for j in xrange(i + 1, n):
			zOpt += value(zl[i][j]) + value(zm[i][j]) + value(zu[i][j])

	return zOpt

def secondStep(al, am, au, zOpt):
	n = len(al)

	zl = []
	for i in xrange(n):
		zl.append([])
		for j in xrange(n):
			zl[i].append(LpVariable("zl_{0}_{1}".format(i, j), 0))

	zm = []
	for i in xrange(n):
		zm.append([])
		for j in xrange(n):
			zm[i].append(LpVariable("zm_{0}_{1}".format(i, j), 0))

	zu = []
	for i in xrange(n):
		zu.append([])
		for j in xrange(n):
			zu[i].append(LpVariable("zu_{0}_{1}".format(i, j), 0))

	yl = []
	for i in xrange(n):
		yl.append([])
		for j in xrange(n):
			yl[i].append(LpVariable("yl_{0}_{1}".format(i, j)))

	ym = []
	for i in xrange(n):
		ym.append([])
		for j in xrange(n):
			ym[i].append(LpVariable("ym_{0}_{1}".format(i, j)))

	yu = []
	for i in xrange(n):
		yu.append([])
		for j in xrange(n):
			yu[i].append(LpVariable("yu_{0}_{1}".format(i, j)))

	xl = []
	for i in xrange(n):
		xl.append(LpVariable("xl_{0}".format(i)))

	xm = []
	for i in xrange(n):
		xm.append(LpVariable("xm_{0}".format(i)))

	xu = []
	for i in xrange(n):
		xu.append(LpVariable("xu_{0}".format(i)))

	zmaxl = LpVariable("zmaxl", 0)
	zmaxm = LpVariable("zmaxm", 0)
	zmaxu = LpVariable("zmaxu", 0)

	targetC = []
	targetC.append((zmaxl, 1))
	targetC.append((zmaxm, 1))
	targetC.append((zmaxu, 1))

	problem = LpProblem("Second-step", LpMinimize)
	problem.setObjective(LpAffineExpression(targetC))

	constrZ = []
	for i in xrange(n):
		for j in xrange(i + 1, n):
			constrZ.append((zl[i][j], 1))
			constrZ.append((zm[i][j], 1))
			constrZ.append((zu[i][j], 1))

	problem += LpConstraint(LpAffineExpression(constrZ), LpConstraintEQ, None, zOpt)

	for i in xrange(n):
		for j in xrange(n):
			if i != j:
				problem += xl[i] - xu[j] - yl[i][j] == math.log(al[i][j])
				problem += xm[i] - xm[j] - ym[i][j] == math.log(am[i][j])
				problem += xu[i] - xl[j] - yu[i][j] == math.log(au[i][j])

	for i in xrange(n):
		for j in xrange(i + 1, n):
			problem += zl[i][j] - yl[i][j] >= 0
			problem += zm[i][j] - ym[i][j] >= 0
			problem += zu[i][j] - yu[i][j] >= 0

			problem += zl[i][j] - yl[j][i] >= 0
			problem += zm[i][j] - ym[j][i] >= 0
			problem += zu[i][j] - yu[j][i] >= 0

			problem += zmaxl - zl[i][j] >= 0
			problem += zmaxm - zm[i][j] >= 0
			problem += zmaxu - zu[i][j] >= 0

	for i in xrange(n):
		problem += xl[i] - xm[i] <= 0
		problem += xm[i] - xu[i] <= 0

	for i in xrange(n):
		for j in xrange(n):
			problem += yl[i][j] - ym[i][j] <= 0
			problem += ym[i][j] - yu[i][j] <= 0

	problem += xl[0] == 0
	problem += xm[0] == 0
	problem += xu[0] == 0

	problem.writeLP("second_step.lp")

	problem.solve()

	wl = [math.exp(value(x)) for x in xl]
	wm = [math.exp(value(x)) for x in xm]
	wu = [math.exp(value(x)) for x in xu]

	wlS = sum(wl)
	wmS = sum(wm)
	wuS = sum(wu)

	for i in xrange(n):
		wl[i], wm[i], wu[i] = wl[i] / wuS, wm[i] / wmS, wu[i] / wlS

	return wl, wm, wu

def eigenWeights(A):
	n = len(A)
	x0 = [1 for _ in A]

	while True:
		x1 = [0 for _ in x0]

		for i in xrange(n):
			for j in xrange(n):
				x1[i] += A[i][j] * x0[j]

		nx1 = sum(abs(x1[i]) for i in xrange(n))
		x1 = [x / nx1 for x in x1]

		e = sum(abs(x1[i] - x0[i]) for i in xrange(n))
		if e < 0.001:
			break

		x0 = x1

	print "We: {0}".format(x1)



if __name__ == '__main__':
	main()
