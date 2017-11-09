import arcpy
import os

def status(content, city = ""):
	print "{}{}".format(content,city)
	log_file.write("{}{}\n".format(content,city))

log_file = open(r"C:\Tools\pyScripts\delta_handler\log.txt", "w")	
	
#cities = ["changwon_si","daegu","seongnam_si","seoul","suwon_si","yongin_si","busan","chungcheongbuk_do","chungcheongnam_do","daejeon","gyeongsangbuk_do","gyeongsangnam_do","gangwon_do","gyeonggi_do","incheon","jeollabuk_do","jellanam_do","gwangju","sejong_si","ulsan","jeju_do"]
cities = ["chungcheongbuk_do","chungcheongnam_do","gangwon_do","gyeonggi_do","gyeongsangbuk_do","gyeongsangnam_do","jellanam_do","jeollabuk_do"]
release = "1709"

for city in cities:

	status("Working on... ",city)
	
	city_source = r"C:\city\Building_layer\02_operations\1709_delta_integration\{}\integration\kor_{}_bufo.shp".format(city,city)
	remove_delta_source = r"C:\city\Building_layer\02_operations\1709_delta_integration\{}\source\deltas\{}_{}_to_remove.shp".format(city,city,release)
	CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures_{}".format(city)

	# Creating Feature Layers
	arcpy.MakeFeatureLayer_management(city_source, "source")
	arcpy.MakeFeatureLayer_management(remove_delta_source, "remove_delta")
	
	# Getting count of polygons to be removed
	removals_count = arcpy.GetCount_management("remove_delta")
	status("Delta removals count: ", removals_count)
	
	
	status("Removing delta polygons...")	
	
	# Selecting polygons to remove from the source
	arcpy.SelectLayerByLocation_management("source", "INTERSECT", "remove_delta", "", "NEW_SELECTION")
	selected_count = arcpy.GetCount_management("source")
	
	
	status("Polygons selected count: ", selected_count)
	
	# Checking selected source polygons contain LMID attribute filled
	arcpy.CopyFeatures_management("source", CopiedFeatures)
	rows = arcpy.SearchCursor(CopiedFeatures,fields="LMID;ID")

	
	for row in rows:
		if row.getValue("LMID") != " ":
			id = row.getValue("ID")
			status("3dlm polygons detected!! ", id)

			
	# Removing polygons from the source		
	arcpy.DeleteRows_management("source")
	
	# Cleanup
	arcpy.Delete_management("source")
	arcpy.Delete_management("remove_delta")
	arcpy.Delete_management(CopiedFeatures)
	
	status("FINISHED removing delta for ", city)
	
log_file.close()	