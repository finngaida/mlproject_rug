#!/usr/bin/env python3
import sys
import argparse

def main(source_file, output_file, **args):
	data_dict = {}
	class_ids = {
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
	with open(output_file,'w+') as output:
		with open(source_file,'r') as f:
			for line in f.readlines():
				image_id, label, x1, y1, x2, y2 = line.rstrip().split(',')
				filename = image_id+'.jpg'
				if(filename in data_dict):
					data_dict[filename]  = data_dict[filename] + ' ' +x1+','+y1+','+x2+','+y2+','+class_ids[label]
				else:
					data_dict[filename] = ' '+ x1+','+y1+','+x2+','+y2+','+class_ids[label]
		for image, objects in data_dict.items():
			output.write(image + objects+'\n')



if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('source_file', metavar='SOURCE')
	parser.add_argument('output_file', metavar='OUTPUT')
	args = vars(parser.parse_args())
	main(**args)