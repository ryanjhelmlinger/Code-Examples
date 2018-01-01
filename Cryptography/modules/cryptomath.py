def gcd(x,y):
	for i in range(1,min(x,y)): 
		if x%i==0 and y%i==0: solution = i
	return solution

def lcm(x,y):
	for i in range(max(x,y),x*y+1):
		if i%x==0 and i%y==0: return i

def mod_inverse(a,m):
	for i in range(m):
		if a*i%m==1: return i

def lin_solve(a,b,c,m):
	inverse = mod_inverse(a,m)
	if inverse==None: return None
	return inverse*(c-b)

def lin_sys_solve(a,b,c,d,e,f,m):
	x = lin_solve(a-d,0,c-f,m)
	if x==None:	return None
	y = (c%m)-a*x
	return (x,y)

def lin_inverse(a,b,m):
	return ()