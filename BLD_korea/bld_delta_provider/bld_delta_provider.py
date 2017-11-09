import datetime as dt
import arcpy
import os

def status(current_time_and_date, content, city = ""):
	print "{}{}".format(content, city)
	log_file.write("{} {}{}".format(current_time_and_date, content, city))

def main():
	current_time_and_date = str(dt.datetime.now())[:19]
	
	# Local variables:
	attribute_template = r"C:\Tools\pyScripts\delta_provider\templates\template.shp"
	spatial_ref = r"C:\Tools\pyScripts\delta_provider\templates\template.prj"
	output_path = r"C:\Tools\pyScripts\delta_output" # common place for delta files for all stages of the process
	log_file = open(r"C:\Tools\pyScripts\delta_provider\{} delta-provider-log.txt".format(current_time_and_date), "w")
	
	#cities = ["busan","changwon_si","daegu","daejeon","gwangju","seongnam_si","seoul","suwon_si","ulsan","yongin_si"]
	cities = ["incheon"]
	current_release = "1709"
	previous_release = "1706"
	
	for city in cities:
		try:
			status(current_time_and_date, "Working on... ", city)
			
			# Create directory
			path = output_path + "\\" + city
		
			if not os.path.exists(path):
				os.makedirs(path)
				
			# Create shapefiles "delta_minus" and "delta_plus"
			arcpy.CreateFeatureclass_management(output_path, "\{}\{}_{}_delta_minus".format(city,city,current_release), "POLYGON", attribute_template, "", "", spatial_ref)
			arcpy.CreateFeatureclass_management(output_path, "\{}\{}_{}_delta_plus".format(city,city,current_release), "POLYGON", attribute_template, "", "", spatial_ref)
			
			# Prepare temp features
			CopiedFeatures1 = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures1_{}".format(city)
			CopiedFeatures2 = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures2_{}".format(city)
			
			# Creating paths to previous and current data
			previous_path = r"C:\city\Building_layer\02_operations\{}_2D_raw_data\{}_{}_raw.shp".format(previous_release,city,previous_release)
			current_path = r"C:\city\Building_layer\02_operations\{}_2D_raw_data\{}_{}_raw.shp".format(current_release,city,current_release)
			
			# Prepare feature layers to process
			arcpy.MakeFeatureLayer_management(previous_path, "previous_lyr")
			arcpy.MakeFeatureLayer_management(current_path, "current_lyr")
			
			status(current_time_and_date, "Creating delta minus files...")
			
			# Separating features to remove
			arcpy.SelectLayerByLocation_management("previous_lyr", "ARE_IDENTICAL_TO", "current_lyr", "", "NEW_SELECTION", "INVERT")
			arcpy.CopyFeatures_management("previous_lyr", CopiedFeatures1)
			arcpy.Append_management(CopiedFeatures1, output_path + "\{}\{}_{}_delta_minus.shp".format(city,city,current_release), "TEST")
			arcpy.SelectLayerByAttribute_management("previous_lyr", "CLEAR_SELECTION")
			
			status(current_time_and_date, "Creating delta plus files...")
			
			# Separating features to add
			arcpy.SelectLayerByLocation_management("current_lyr", "ARE_IDENTICAL_TO", "previous_lyr", "", "NEW_SELECTION", "INVERT")
			arcpy.CopyFeatures_management("current_lyr", CopiedFeatures2)
			arcpy.Append_management(CopiedFeatures2, output_path + "\{}\{}_{}_delta_plus.shp".format(city,city,current_release), "TEST")
		
			# Clean up
			arcpy.Delete_management("previous_lyr")
			arcpy.Delete_management("current_lyr")
			arcpy.Delete_management(CopiedFeatures1)
			arcpy.Delete_management(CopiedFeatures2)
			
			status(current_time_and_date, "FINISHED for ")
			
		except Exception as err:
			status(current_time_and_date, "Exception found in ", city)
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
			continue
		
	log_file.close()
	
main()