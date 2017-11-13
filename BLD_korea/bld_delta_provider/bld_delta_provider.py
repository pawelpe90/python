import datetime as dt
import arcpy
import os


def get_time():
	return str(dt.datetime.now())[:19].replace(":", "-")

log_file = open(r"C:\Users\pruszyns\Desktop\logs\{} delta-provider-log.txt".format(get_time()), "w")	
	
def status(time, content, city = ""):
	time = get_time()
	print "{} {}{}".format(time, content, city)
	log_file.write("{} {}{}\n".format(time, content, city))

def main():
	
	source_path = "C:\Tools\pyScripts\delta_provider"
	
	# Local variables:
	attribute_template = r"{}\templates\template.shp".format(source_path)
	spatial_ref = r"{}\templates\template.prj".format(source_path)
	output_path = r"C:\Users\pruszyns\Desktop\output" # common place for delta files for all stages of the process
	
	
	#cities = ["busan","changwon_si","daegu","daejeon","gwangju","seongnam_si","seoul","suwon_si","ulsan","yongin_si"]
	cities = ["incheon"]
	current_release = "2017_09"
	previous_release = "2017_06"
	
	for city in cities:
		current_time_and_date = str(dt.datetime.now())[:19].replace(":", "-")
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
			previous_path = r"C:\city\Building_layer\07_raw_data\{}\{}\{}_{}_raw.shp".format(previous_release,city,city,previous_release)
			current_path = r"C:\city\Building_layer\07_raw_data\{}\{}\{}_{}_raw.shp".format(current_release,city,city,current_release)
			
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
			
			status(current_time_and_date, "FINISHED for ", city)
			
		except Exception as err:
			status(current_time_and_date, "Exception found in ", city)
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
			arcpy.Delete_management("previous_lyr")
			arcpy.Delete_management("current_lyr")
			arcpy.Delete_management(CopiedFeatures1)
			arcpy.Delete_management(CopiedFeatures2)
			continue
		
	status(current_time_and_date, "Application finished.")
	
main()
log_file.close()