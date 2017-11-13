import datetime as dt
import arcpy
import os


def get_time():
	return str(dt.datetime.now())[:19].replace(":", "-")

log_file = open(r"C:\Users\pruszyns\Desktop\logs\{} delta-cleaner-log.txt".format(get_time()), "w")
	
def status(time, content, city = ""):
	time = get_time()
	print "{} {}{}".format(time, content, city)
	log_file.write("{} {}{}\n".format(time, content, city))
	
def main():
	
	# cities = ["seoul","busan","changwon_si","daegu","daejeon","gwangju","incheon","seongnam_si","suwon_si","ulsan","yongin_si"]
	cities = ["incheon"]
	current_release = "2017_09"

	for city in cities:
		try:
			status(get_time(),"Working on... ",city)
			
			if city in ("seoul","busan"):
				extent_path = r"C:\city\Extents\ACM\{}\coverage_ACM.shp".format(current_release)
			elif city in ("changwon_si","daegu","daejeon","gwangju","incheon","seongnam_si","suwon_si","ulsan","yongin_si"):
				extent_path = r"C:\city\Extents\ACMLOD1\{}\coverage_acmlod1.shp".format(current_release)
			else:
				continue
			
			CopiedFeaturesExtent = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeaturesExtent_{}".format(city)
			
			# Extent separation
			arcpy.MakeFeatureLayer_management(extent_path, "Extent")
			arcpy.SelectLayerByAttribute_management("Extent", "NEW_SELECTION", """ CITY = '{}' """.format(city))
			arcpy.CopyFeatures_management("Extent", CopiedFeaturesExtent)
			
			extent = CopiedFeaturesExtent
			
			delta_plus_path = r"C:\Users\pruszyns\Desktop\output\{}\{}_{}_delta_plus.shp".format(city,city,current_release)
			delta_minus_path = r"C:\Users\pruszyns\Desktop\output\{}\{}_{}_delta_minus.shp".format(city,city,current_release)
			
			arcpy.MakeFeatureLayer_management(delta_plus_path, "delta_plus")
			arcpy.MakeFeatureLayer_management(delta_minus_path, "delta_minus")
			
			status(get_time(), "Cleaning delta plus files...")
			
			# Cleaning delta plus files
			arcpy.SelectLayerByLocation_management("delta_plus", "INTERSECT", extent)
			arcpy.DeleteRows_management("delta_plus")
			
			status(get_time(), "Cleaning delta minus files...")
			
			# Cleaning delta minus files
			arcpy.SelectLayerByLocation_management("delta_minus", "INTERSECT", extent)
			arcpy.DeleteRows_management("delta_minus")
			
			# Clean up
			arcpy.Delete_management("delta_plus")
			arcpy.Delete_management("delta_minus")
			arcpy.Delete_management(CopiedFeaturesExtent)

			status(get_time(), "FINISHED for ", city)
			
		except Exception as err:
			status(get_time(), "Exception found in ", city)
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
			arcpy.Delete_management("delta_plus")
			arcpy.Delete_management("delta_minus")
			arcpy.Delete_management(CopiedFeaturesExtent)
			continue
		
	status(get_time(), "Application finished.")
	
main()
log_file.close()