newfile = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kitti\\kitti_non_motorized_clean.txt","w")
file = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kitti\\kitti_non_motorized.txt","r")
for line in file.readlines():
	#line = 006280 Cyclist 0.00 3 -1.83 774.82 172.51 826.46 259.37 1.86 0.60 2.02 4.28 1.86 16.49 -1.58
	items = line.split(" ")
	id = items[0]
	type = items[1]
	x1 = items[5]
	y1 = items[6]
	x2 = items[7]
	y2 = items[8]

	newline = id + "\t" + type + "\t" + x1 + "\t" + x2 + "\t" + y1 + "\t" + y2 + "\n"
	newfile.write(newline)
