import arcpy

#cities = ["busan","changwon_si","daegu","daejeon","gwangju","seongnam_si","seoul","suwon_si","ulsan","yongin_si"]
cities = ["incheon"]

current_release = "1706"
log_file = open(r"C:\Tools\pyScripts\changes_introducer\log.txt", "w")

def status(content, city = ""):
	print "{} {}".format(content,city)
	log_file.write("{}{}".format(content,city))

for city in cities:

	status("Working on... ",city)
	
	files_to_remove = r"C:\city\Building_layer\02_operations\{}_2D_raw_data\deltas\{}\{}_{}_to_remove.shp".format(current_release,city,city,current_release)
	files_to_add = r"C:\city\Building_layer\02_operations\{}_2D_raw_data\deltas\{}\{}_{}_to_add.shp".format(current_release,city,city,current_release)
	city_to_process = r"C:\city\Building_layer\02_operations\{}_2D_bld\{}\kor_{}_bufo.shp".format(current_release,city,city)
	
	arcpy.MakeFeatureLayer_management(files_to_remove, "Remove")
	arcpy.MakeFeatureLayer_management(files_to_add, "Add")
	arcpy.MakeFeatureLayer_management(city_to_process, "City")
	
	status("Removing delta files... ")
	
	arcpy.SelectLayerByLocation_management("City", "ARE_IDENTICAL_TO", "Remove", "", "NEW_SELECTION")
	arcpy.DeleteRows_management("City")
	
	status("Appending delta files... ")
	
	arcpy.Append_management("Add", city_to_process, "NO_TEST")
	
	arcpy.Delete_management("Remove")
	arcpy.Delete_management("Add")
	arcpy.Delete_management("City")
	
	status("FINISHED FOR ", city)
	
log_file.close()