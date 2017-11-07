######
#
# bld_extractor_1.1
#
# New features:
#  - loading extents from fixed location
#  - folder creation for new cities added
#  - log_file fixed
#  - "status" function implemented
#
# dupa
######


# Import arcpy module
import arcpy
import os

def status(content, city = ""):
	print "{}{}".format(content,city)
	log_file.write("{}{}\n".format(content,city))

# Local variables:
#CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures"
attribute_template = r"C:\Tools\pyScripts\bld_extractor\templates\template.shp"
spatial_ref = r"C:\Tools\pyScripts\bld_extractor\templates\template.prj"
output_path = r"C:\Tools\pyScripts\bld_extractor\output"
extents_path = r"C:\city\Extents\BLD\2017_06\coverage_buildings.shp"

# Release
release = "1706"

# Set working environment
arcpy.env.workspace = r"C:\city\Building_layer\06_public_sources\kor\2D\kor{}.gdb".format(release)
fcs = arcpy.ListFeatureClasses() # needed???

#cities = ["busan","changwon_si","daegu","daejeon","gwangju","seongnam_si","seoul","suwon_si","ulsan","yongin_si"]
cities = ["sejong_si","chungcheongbuk_do", "chungcheongnam_do", "gangwon_do", "gyeonggi_do", "gyeongsangbuk_do", "gyeongsangnam_do", "jeju_do", "jellanam_do", "jeollabuk_do"]

log_file = open(r"C:\Tools\pyScripts\bld_extractor\log.txt", "w")

try:
	for city in cities:

		status("Working on... ",city)
		
		# Create city folder
		path = output_path + "\\" + city

		if not os.path.exists(path):
			os.makedirs(path)
		
		# Create shapefile
		arcpy.CreateFeatureclass_management(output_path, "\{}\{}_{}_raw".format(city,city,release), "POLYGON", attribute_template, "", "", spatial_ref)
		CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures_{}".format(city)
		CopiedFeaturesExtent = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeaturesExtent_{}".format(city)
		
		# Extent separation
		arcpy.MakeFeatureLayer_management(extents_path, "Extent")
		arcpy.SelectLayerByAttribute_management("Extent", "NEW_SELECTION", """ CITY = '{}' """.format(city))
		arcpy.CopyFeatures_management("Extent", CopiedFeaturesExtent)
		
		# Extent file location
		extent = CopiedFeaturesExtent
		
		fc_Layer = city
	
		for fc in fcs:
			# Process: Make Feature Layer
			arcpy.MakeFeatureLayer_management(fc, fc_Layer)

			# Process: Define Projection
			arcpy.DefineProjection_management(fc_Layer, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
		
			# Process: Select Layer By Location
			arcpy.SelectLayerByLocation_management(fc_Layer, "HAVE_THEIR_CENTER_IN", extent)

			# Process: Copy Features
			arcpy.CopyFeatures_management(fc_Layer, CopiedFeatures)
		
			# Process: Append
			arcpy.Append_management(CopiedFeatures, output_path + "\{}\{}_{}_raw.shp".format(city,city,release), "NO_TEST")
			
			arcpy.Delete_management(fc_Layer)
			arcpy.Delete_management(CopiedFeatures)
			
		arcpy.Delete_management("Extent")
		arcpy.Delete_management(CopiedFeaturesExtent)
		
		status("FINISHED FOR ",city)

except Exception as err:
    print(err.args[0])
	
log_file.close()