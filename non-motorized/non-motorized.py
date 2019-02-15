#data looks like:
#00110592,car,465,111,507,135
#00110592,non-motorized_vehicle,197,187,318,269

#Now we need to generate the label files that Darknet uses. Darknet wants a .txt file for each image with a line for each ground truth object in the image that looks like:
#make file per picture (0011...txt) with:
#<object-class> <x> <y> <width> <height>

import csv

import pickle

def classnumber(veh_class):
	#print(veh_class)
	dictionary = {
	"articulated_truck": 1,
	"bicycle": 2,
	"bus": 3,
	"car": 4,
	"motorcycle": 5,
	"motorized_vehicle": 6,
	"non-motorized_vehicle": 7,
	"pedestrian": 8,
	"pickup_truck": 9,
	"single_unit_truck": 10,
	"work_van": 11
	}

	return str(dictionary[veh_class])

def makedict():
	file = open("data/MIO-TCD-Localization/gt_train.txt","r",encoding="UTF-16")
	filedictionary = {}
	for line in file.readlines():
		params = line.rstrip("\n").split(",")
		picture = params[0]
		type = params[1]

		x1 = eval(params[2])
		y1 = eval(params[3])
		x2 = eval(params[4])
		y2 = eval(params[5])

		width = x2-x1
		height = y2-y1

		xmid = round((x1 + x2)/2 + 1)
		ymid = round((y1 + y2)/2 + 1)

		newline = classnumber(type) + " " + str(xmid) + " " + str(ymid) + " " + str(width) + " " + str(height) + "\n"
		if picture not in filedictionary:
			filedictionary[picture] = [newline]
		else:
			filedictionary[picture].append(newline)

	pickle.dump(filedictionary, open("filedictionary.pickle",'wb'))
	print("Dict made")

def makenonmotorizedfiledict():
	#makedict()
	filedictionary = pickle.load(open("filedictionary.pickle","rb"))

	nonmotorizedfiledict = {}
	for id in filedictionary:
		if "pedestrian" in str(filedictionary[id]):
			if id not in nonmotorizedfiledict:
				nonmotorizedfiledict[id] = filedictionary[id]
		if "bicycle" in str(filedictionary[id]):
			if id not in nonmotorizedfiledict:
				nonmotorizedfiledict[id] = filedictionary[id]

	pickle.dump(nonmotorizedfiledict,open("non-motorizeddict.pickle","wb"))


#SPLIT THE NON-MOTORIZEDDICT IN 2 PARTS:
def splitdict():
	nonmotorizedfiledict = pickle.load(open("non-motorizeddict.pickle", "rb"))
	nonmotorizedtraindict = {}
	nonmotorizedtestdict = {}
	#500 test, 4425 train
	i = 0
	for item in nonmotorizedfiledict:
		if i < 500:
			nonmotorizedtestdict[item] = nonmotorizedfiledict[item]
		else:
			nonmotorizedtraindict[item] = nonmotorizedfiledict[item]
		i = i+1

	print(len(nonmotorizedtestdict))
	print(len(nonmotorizedtraindict))

	pickle.dump(nonmotorizedtestdict, open("non-motorizedtestdict.pickle","wb"))
	pickle.dump(nonmotorizedtraindict, open("non-motorizedtraindict.pickle","wb"))



#DO THIS FOR 90% AND FOR THE LAST 10% SEPERATELY, THE FILES AND THE CSV-FILE (MAKE 2 NON-MOTORIZEDDICTS AND RUN THE 2 FUNCTIONS (COPYFILES AND MAKENONMOTORIZEDTRAINFILE)
def copyfiles(traintestdict,traintest):
	from shutil import copy2
	#nonmotorizedfiledict = pickle.load(open("non-motorizeddict.pickle","rb"))
	location = "G:\Mijn Drive\Studie informatiekunde\master\jaar 2\machine learning\\final project\MIO-TCD-Localization\MIO-TCD-Localization\\train\\"
	goallocation = "G:\Mijn Drive\Studie informatiekunde\master\jaar 2\machine learning\\final project\mlproject_rug\\non-motorized\\non-motorized-files\\"+traintest
	for name in traintestdict:
		filename = name+".jpg"
		copy2(location+filename, goallocation)


def makenonmotorizedfile(traintestdict,traintest):
	filename = traintest+".csv"
	nonmotorizedtraintestfile = open(filename,"w")
	for item in traintestdict:
		for object in traintestdict[item]:
			if "pedestrian" in object or "bicycle" in object:
				line = str(item)+","+ ",".join(object.split()) + "\n"
				nonmotorizedtraintestfile.write(line)


def main():
	#CHOOSE WHAT YOU WANT/NEED
	#CHANGE PATHS

	#makenonmotorizedfiledict()
	#copyfiles()
	#makenonmotorizedtrainfile()
	# splitdict()

	nonmotorizedtestdict = pickle.load(open("non-motorizedtestdict.pickle", "rb"))
	copyfiles(nonmotorizedtestdict,"test")
	makenonmotorizedfile(nonmotorizedtestdict,"test")

	nonmotorizedtraindict = pickle.load(open("non-motorizedtraindict.pickle", "rb"))
	copyfiles(nonmotorizedtraindict,"train")
	makenonmotorizedfile(nonmotorizedtraindict,"train")

main()