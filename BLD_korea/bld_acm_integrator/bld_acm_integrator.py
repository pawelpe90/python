# Import arcpy module
import arcpy
import os

def status(content, city = ""):
	print "{}{}".format(content,city)
	log_file.write("{}{}\n".format(content,city))

# Local variables	
input_path = r"C:\Tools\pyScripts\bld_acm_integrator\input"
output_path = r"C:\Tools\pyScripts\bld_acm_integrator\output"
log_file = open(r"C:\Tools\pyScripts\bld_acm_integrator\log.txt", "w")
extents_path = r"C:\city\Extents\ACM\2017_06\coverage_acm.shp"

# Release
release = "1706"

cities = ["busan","seoul"]

for city in cities:
	
	status("Working on... ",city)
	
	# Create city folder
	path = output_path + "\\" + city

	if not os.path.exists(path):
		os.makedirs(path)
	
	# Create temp shapefile
	CopiedFeaturesExtent = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeaturesExtent_{}".format(city)
	
	# Extent separation
	arcpy.MakeFeatureLayer_management(extents_path, "Extent")
	arcpy.SelectLayerByAttribute_management("Extent", "NEW_SELECTION", """ CITY = '{}' """.format(city))
	arcpy.CopyFeatures_management("Extent", CopiedFeaturesExtent)
	
	# Extent file location
	extent = CopiedFeaturesExtent
	
	input_city_path = input_path + "\{}\{}_{}_raw.shp".format(city,city,release)
	output_city_path = output_path + "\{}\{}_{}_raw.shp".format(city,city,release)
	
	# Copy input data
	arcpy.Copy_management(input_city_path,output_city_path)
	
	arcpy.MakeFeatureLayer_management(output_city_path, "City")
	
	arcpy.SelectLayerByLocation_management("City", "COMPLETELY_WITHIN", extent, "", "NEW_SELECTION")
	arcpy.DeleteRows_management("City")
	
	arcpy.Delete_management("City")
	arcpy.Delete_management("Extent")
	arcpy.Delete_management(CopiedFeaturesExtent)	
	
	status("FINISHED FOR ", city)
	
log_file.close()