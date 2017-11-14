#Script append raw addings from delta to bld format shapefile and reattribute 

import arcpy
import os

def status(content, city = ""):
	print "{}{}".format(content,city)
	log_file.write("{}{}\n".format(content,city))

def calculator(fc, id_max):
    arcpy.CalculateField_management(fc, "ID", "str(!FID! + 1 + {})".format(id_max), "PYTHON")
    arcpy.CalculateField_management(fc, "GRNDHEIGHT", "-1")
    arcpy.CalculateField_management(fc, "HEIGHT", "-1")	
	
log_file = open(r"C:\Tools\pyScripts\delta_handler\addDelta_log.txt", "w")
release = "1709"

#cities = ["changwon_si","daegu","seongnam_si","seoul","suwon_si","yongin_si","busan","chungcheongbuk_do","chungcheongnam_do","daejeon","gyeongsangbuk_do","gyeongsangnam_do","gangwon_do","gyeonggi_do","incheon","jeollabuk_do","jellanam_do","gwangju","sejong_si","ulsan","jeju_do"]
#cities = ["chungcheongbuk_do","chungcheongnam_do","gangwon_do","gyeonggi_do","gyeongsangbuk_do","gyeongsangnam_do","jellanam_do","jeollabuk_do"]
cities = ["seongnam_si","suwon_si","ulsan","yongin_si"]

for city in cities:
	
	status("Working on... ",city)
	
	city_source = r"C:\city\Building_layer\02_operations\1709_delta_integration\{}\integration\kor_{}_bufo.shp".format(city,city)
	add_delta_source = r"C:\city\Building_layer\02_operations\1709_delta_integration\{}\source\deltas\{}_{}_to_add.shp".format(city,city,release)
	add_delta_main = r"C:\city\Building_layer\02_operations\1709_delta_integration\{}\source\deltas\add\kor_{}_bufo.shp".format(city,city)
	CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures_{}".format(city)

	# Creating Feature Layers
	arcpy.MakeFeatureLayer_management(city_source, "source")
	arcpy.MakeFeatureLayer_management(add_delta_source, "add_delta")
	arcpy.MakeFeatureLayer_management(add_delta_main, "delta_target")
	
	status("Getting max id...")
	
	# Getting max id value for reattribute
	arcpy.CopyFeatures_management("source", CopiedFeatures)
	rows = arcpy.SearchCursor(CopiedFeatures,fields="ID")
	idcontainer = []

	for row in rows:
		idcontainer.append(row.getValue("ID"))
		
	id_max = max(idcontainer)
	
	status("Attributing...")
	
	# Appending source delta to target delta
	arcpy.Append_management("add_delta","delta_target","NO_TEST")
	
	# Attributing target delta
	calculator("delta_target", id_max)
	
	
	# Cleanup
	arcpy.Delete_management("source")
	arcpy.Delete_management("add_delta")
	arcpy.Delete_management("delta_target")
	arcpy.Delete_management(CopiedFeatures)
	
	status("FINISHED adding delta for ", city)
	status("\n")
	
log_file.close()	