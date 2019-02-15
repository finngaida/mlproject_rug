rightanswersfile = open("non-motorized-files/test.csv","r")
my_answersfile = open("non-motorized-files/test-outputNiels-defaultmodel.csv","r")
rightanswersdict = {}
myanswersdict = {}

for line in rightanswersfile.readlines():
	elements = line.rstrip("\n").split(",")
	"""
	picture = elements[0]
	vehicle = elements[1]
	x = elements[2]
	y = elements[3]
	width = elements[4]
	height = elements[5]
	"""
	[picture, vehicle, x, y, width, height] = elements
	if picture not in rightanswersdict:
		rightanswersdict[picture] = [[vehicle,x,y,width,height]]
	else:
		rightanswersdict[picture].append([vehicle, x, y, width, height])

for line in my_answersfile.readlines():
	elements = line.rstrip("\n").split(",")
	[picture, vehicle, x, y, width, height] = elements
	if vehicle == "person" or vehicle == "bicycle":
		if picture not in myanswersdict:
			myanswersdict[picture] = [[vehicle, x, y, width, height]]
		else:
			myanswersdict[picture].append([vehicle, x, y, width, height])

print("DIFFERENCES between amount of found bicycles and persons and the actual amount:")
print(len(rightanswersdict))
sumofdiffs = 0
for item in rightanswersdict:
	if item in myanswersdict:
		difference = abs(len(rightanswersdict[item]) - len(myanswersdict[item]))
		print(item, difference)
		sumofdiffs += difference
	else:
		pass

print("total diff", sumofdiffs)
print("amount of files with recognized objects", len(myanswersdict))
print("right amount of files", len(rightanswersdict))
