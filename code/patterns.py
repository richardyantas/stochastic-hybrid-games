def query(X): 
	if (44<= X.T and X.T <= 44.1) and (0.1<= X.V and X.V <= 0.11):
		return [[1], [1,4], [1,4,5], [0,1], [0,1,5], [0,0,1]]
	print("Not Found") 
	return [[-1,-1,-1]]