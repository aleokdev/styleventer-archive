ascii =[0 ,12 ,-2 ,2 ,26 ,-10 ,6 ,-5 ,2 ,7 ,-24 ,2 ,-42 ,32 ,-5 ,-18 ,1 ,29 ,-48 ,17 ]
def f (**O0O0O00O0OOO00000 ):
	return O0O0O00O0OOO00000 [chr(0x78)]==O0O0O00O0OOO00000 [chr(0x79)]
def f2 (OO0OO00OOOO00O0OO ,O0OO0O0O00O0OOO0O ,c =0 ,d ="a"):
	if (OO0OO00OOOO00O0OO ==0 and len (O0OO0O0O00O0OOO0O )!=20 ):
		return False
	if (len (O0OO0O0O00O0OOO0O )==0 ):
		if (c ==1490 ):
			return True
		else :
			return False
	if (d !=chr(97)):
		if (ascii [-OO0OO00OOOO00O0OO ]!=ord (O0OO0O0O00O0OOO0O [-1 ])-d ):
			return False
	if ((OO0OO00OOOO00O0OO -10 )%5 ==0 and OO0OO00OOOO00O0OO >8 ):
		if not f (x =O0OO0O0O00O0OOO0O [-1 ],y =chr(0x2d)):
			return False
	elif f (x =O0OO0O0O00O0OOO0O [-1 ],y =chr(0x2d)):
		return False
	return f2 (OO0OO00OOOO00O0OO +1 ,O0OO0O0O00O0OOO0O [:-1 ],c =c +ord (O0OO0O0O00O0OOO0O [-1 ]),d =ord (O0OO0O0O00O0OOO0O [-1 ]))
if __name__ =="__main__":
	print ("Input the solution:")
	if f2 (0 ,input ()):
		print ("Correct!")
	else :
		print ("Wrong flag!")