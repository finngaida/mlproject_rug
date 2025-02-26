#data looks like:
#00110592,car,465,111,507,135
#00110592,non-motorized_vehicle,197,187,318,269

#Now we need to generate the label files that Darknet uses. Darknet wants a .txt file for each image with a line for each ground truth object in the image that looks like:
#make file per picture (0011...txt) with:
#<object-class> <x> <y> <width> <height>

import csv

#DIT HEEFT LENNART AL GEMAAKT, IK MOET IETS ANDERS DOEN, VRAGEN
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

def main():
	#makedict()
	filedictionary = pickle.load(open("filedictionary.pickle","rb"))
	for picture in filedictionary:
		filename = picture+".txt"
		file = open("yolodarknetdata/"+filename, "w")
		for item in filedictionary[picture]:
			if item != filedictionary[picture][-1]:
				file.write(item+"\n")
			else:
				file.write(item)

		file.close()

main()