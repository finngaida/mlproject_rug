def avg(x,y):
	return (x+y)/2

myoutput = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kittidata\\outputallkitti-for-map.txt","r")
newfile = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kittidata\\bikesconverted.txt","w")
mydict = {}
for line in myoutput.readlines():
	(id,obj,prob,x1,y1,x2,y2) = line.rstrip("\n").split(" ")
	if id not in mydict:
		mydict[id] = [[obj,prob,x1,y1,x2,y2]]
	else:
		mydict[id].append([obj,prob,x1,y1,x2,y2])

for id in mydict:
	picture = mydict[id]
	for item1 in range(len(picture)):
		for item2 in range(len(picture)):
			if item1 != item2:
				obj1 = picture[item1][0]
				prob1 = picture[item1][1]
				personX1 = eval(picture[item1][2])
				personY1 = eval(picture[item1][3])
				personX2 = eval(picture[item1][4])
				personY2 = eval(picture[item1][5])

				obj2 = picture[item2][0]
				prob2 = picture[item2][1]
				bicycleX1 = eval(picture[item2][2])
				bicycleY1 = eval(picture[item2][3])
				bicycleX2 = eval(picture[item2][4])
				bicycleY2 = eval(picture[item2][5])


				if obj1 == "person" and obj2 == "bicycle":
					#look into picture better to check these assumptions:
					#https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip

					if personX1 > bicycleX1 and personX2 < bicycleX2 and personY1 < bicycleY1:
						cyclistX1 = str(bicycleX1)
						cyclistY1 = str(personY1)
						cyclistX2 = str(bicycleX2)
						cyclistY2 = str(bicycleY2)
						print(id, picture[item1], "\n", picture[item2], "\n")
						newfile.write(str(id)+" cyclist "+str(avg(eval(prob1),eval(prob2)))+" "+cyclistX1+" "+cyclistY1+" "+cyclistX2+" "+cyclistY2+"\n")

				else:
					for item in picture:
						line = id+" "+" ".join(item)+"\n"
						if "bicycle" not in line:
							line = line.replace("person","pedestrian")
							newfile.write(line)

def main():
	newfile = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kittidata\\bikesconverted.txt","r")
	outputfile = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kittidata\\bikesconverted-good.txt","w")
	linelist = []
	for line in newfile.readlines():
		if line not in linelist:
			linelist.append(line)
			outputfile.write(line)
main()

