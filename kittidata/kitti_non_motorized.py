import os
newfile = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kitti\\kitti_non_motorized.txt","w")
file = open("G:\\Mijn Drive\\Studie informatiekunde\\master\\jaar 2\\machine learning\\final project\\mlproject_rug\\kitti\\allkittidata.txt","r")
for line in file.readlines():
	if "Pedestrian" in line or "Cyclist" in line:
		newfile.write(line)


