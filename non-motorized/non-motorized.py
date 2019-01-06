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


def copyfiles():
	from shutil import copy2
	nonmotorizedfiledict = pickle.load(open("non-motorizeddict.pickle","rb"))
	location = "G:\Mijn Drive\Studie informatiekunde\master\jaar 2\machine learning\\final project\MIO-TCD-Localization\MIO-TCD-Localization\\train\\"
	for name in nonmotorizedfiledict:
		filename = name+".jpg"
		copy2(location+filename, "G:\Mijn Drive\Studie informatiekunde\master\jaar 2\machine learning\\final project\mlproject_rug\\non-motorized-files")


def makenonmotorizedtrainfile():
	nonmotorizedfiledict = pickle.load(open("non-motorized/non-motorizeddict.pickle", "rb"))
	nonmotorizedtrainfile = open("gt_train_non_motorized.csv","w")
	for item in nonmotorizedfiledict:
		for object in nonmotorizedfiledict[item]:
			if "pedestrian" in object or "bicycle" in object:
				line = str(item)+","+ ",".join(object.split()) + "\n"
				nonmotorizedtrainfile.write(line)


def main():
	#CHOOSE WHAT YOU WANT/NEED
	#CHANGE PATHS

	#makenonmotorizedfiledict()
	copyfiles()
	#makenonmotorizedtrainfile()
main()