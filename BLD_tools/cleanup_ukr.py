import arcpy
import os

cities = os.listdir(r"D:\14_buildings_layer\analysis\ukraine\1803\01_accepted\eur\ukr")
drop_fields = ["Shape_Leng", "Shape_Le_1", "Shape_Area"]


for city in cities:
	try:
	
		print "Working on... {}".format(city)
		
		fc = r"D:\14_buildings_layer\analysis\ukraine\1803\01_accepted\eur\ukr\{}\ukr_{}_bufo.shp".format(city,city)
		
		arcpy.DeleteField_management(fc, drop_fields)
		
		print "Finished for {}!".format(city)
		
	except:
		print "Something wrong for {}".format(city)
		continue