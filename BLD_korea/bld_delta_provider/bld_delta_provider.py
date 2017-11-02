# Import arcpy module
import arcpy
import os

def status(content, city = ""):
	print "{}{}".format(content,city)
	log_file.write("{}{}".format(content,city))

# Local variables:
attribute_template = r"C:\Tools\pyScripts\delta_provider\templates\template.shp"
spatial_ref = r"C:\Tools\pyScripts\delta_provider\templates\template.prj"
output_path = r"C:\Tools\pyScripts\delta_provider\output"
log_file = open(r"C:\Tools\pyScripts\delta_provider\log.txt", "w")

#cities = ["busan","changwon_si","daegu","daejeon","gwangju","seongnam_si","seoul","suwon_si","ulsan","yongin_si"]
cities = ["incheon"]
current_release = "1706"
previous_release = "1702"

for city in cities:

	status("Working on... ",city)
	
	# Create directory
	path = output_path + "\\" + city

	if not os.path.exists(path):
		os.makedirs(path)
		
	# Create shapefiles "to_remove" and "to_add"
	arcpy.CreateFeatureclass_management(output_path, "\{}\{}_{}_to_remove".format(city,city,current_release), "POLYGON", attribute_template, "", "", spatial_ref)
	arcpy.CreateFeatureclass_management(output_path, "\{}\{}_{}_to_add".format(city,city,current_release), "POLYGON", attribute_template, "", "", spatial_ref)
	
	# Prepare temp features
	CopiedFeatures1 = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures1_{}".format(city)
	CopiedFeatures2 = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures2_{}".format(city)
	
	# Creating paths to previous and current data
	previous_path = r"C:\city\Building_layer\02_operations\{}_2D_raw_data\{}_{}_raw.shp".format(previous_release,city,previous_release)
	current_path = r"C:\city\Building_layer\02_operations\{}_2D_raw_data\{}_{}_raw.shp".format(current_release,city,current_release)
	
	# Prepare feature layers to process
	arcpy.MakeFeatureLayer_management(previous_path, "previous_lyr")
	arcpy.MakeFeatureLayer_management(current_path, "current_lyr")
	
	status("Creating delta files to remove...")
	
	# Separating features to remove
	arcpy.SelectLayerByLocation_management("previous_lyr", "ARE_IDENTICAL_TO", "current_lyr", "", "NEW_SELECTION", "INVERT")
	arcpy.CopyFeatures_management("previous_lyr", CopiedFeatures1)
	arcpy.Append_management(CopiedFeatures1, output_path + "\{}\{}_{}_to_remove.shp".format(city,city,current_release), "TEST")
	
	status("Creating delta files to add...")
	
	# Separating features to add
	arcpy.SelectLayerByLocation_management("current_lyr", "ARE_IDENTICAL_TO", "previous_lyr", "", "NEW_SELECTION", "INVERT")
	arcpy.CopyFeatures_management("current_lyr", CopiedFeatures2)
	arcpy.Append_management(CopiedFeatures2, output_path + "\{}\{}_{}_to_remove.shp".format(city,city,current_release), "TEST")

	# Clean up
	arcpy.Delete_management("previous_lyr")
	arcpy.Delete_management("current_lyr")
	arcpy.Delete_management(CopiedFeatures1)
	arcpy.Delete_management(CopiedFeatures2)
	
	status("FINISHED for ")
	
log_file.close()