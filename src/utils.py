def store_results(result, filename):
	with open(filename, 'w') as f:
		for i, row in enumerate(result):
			for j, col in enumerate(row):
				if j==0:
					f.write("%d\n" % i)
					f.write("**%s**\n" % col)
				else:
					f.write("%s\n" % col)
			f.write("\n")
