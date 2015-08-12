import random

def RemoveDuplicate(seq):	#removes duplicates from list
    output = [];
    [output.append(obj) for obj in seq if obj not in output];
    return output;

def genSeq1(n):	#Generate an array that gives a sequence;size of board=n*n
	arrTemp=[];	#temporary array
	x=0;	# x-coordinate
	y=0;	# y-coordinate
	s=1;	# number of squares
	arrSeq=[]; #sequence array
	while x<n or y<n:
		if s==1:	# first square is (0,0)
			arrTemp.append([x,y]);
		else:
			y=random.randint(y,y+1);
			if y>=n-1:
				x=random.randint(x,x+1);
			else:
				x=random.randint(x-1,x+1);
			if x<0 and y<n:
				x=x+1;
				y=y;
				arrTemp.append([x,y]);
			elif x<0 and y>=n:
				x=x+1;
				y=y-1;
				arrTemp.append([x,y]);
			elif x>=n or y>=n:
				if x>=n and y<n:
					x=x-1;
					y=y;
					arrTemp.append([x,y]);	
				elif y>=n and x<n:
					y=y-1;
					x=x;
					arrTemp.append([x,y]);
				elif x>=n and y>=n:
					break;
			elif x==n-1 and y==n-1:
				arrTemp.append([x,y]);
				break;	
			else:
				arrTemp.append([x,y]);	
		s=s+1;
	arrSeq=RemoveDuplicate(arrTemp);
	s=len(arrSeq);
	return arrSeq;

def genSeq2(n):	#Generate an array that gives a sequence;size of board=n*n
	arrTemp=[];	#temporary array
	x=0;	# x-coordinate
	y=0;	# y-coordinate
	s=1;	# number of squares
	arrSeq=[]; #sequence array
	while x<n or y<n:
		if s==1:	# first square is (0,0)
			arrTemp.append([x,y]);
		else:
			x=random.randint(x,x+1);
			y=random.randint(y,y+1);
			if x>=n or y>=n:
				if x>=n and y<n:
					x=x-1;
					y=y;
					arrTemp.append([x,y]);	
				elif y>=n and x<n:
					y=y-1;
					x=x;
					arrTemp.append([x,y]);
				elif x>=n and y>=n:
					break;
			elif x==n-1 and y==n-1:
				arrTemp.append([x,y]);
				break;	
			else:
				arrTemp.append([x,y]);	
		s=s+1;
	arrSeq=RemoveDuplicate(arrTemp);
	s=len(arrSeq);
	return arrSeq;

