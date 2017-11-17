import datetime as dt
import arcpy
import os


def get_time():
	return str(dt.datetime.now())[:19].replace(":", "-")

log_file = open(r"C:\Users\pruszyns\Desktop\logs\{} bld-remove-delta-log.txt".format(get_time()), "w")	


def status(content, city = ""):
	time = get_time()
	print "{} {}{}".format(time, content, city)
	log_file.write("{} {}{}\n".format(time, content, city))
	
def scope_selector():
    with open(r"C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\scope.txt", "r") as fscope:
        scope = fscope.readlines()
        scope_fix = [element.strip() for element in scope]
		scope_filtered = [i for i in scope_fix if not i.startswith("#")]
    return scope_filtered

def main():

	cities = scope_selector()
	release = "2017_09"
	
	for city in cities:
	
		try:
		
			status("Working on... ",city)
			
			city_source = r"C:\city\Building_layer\02_operations\{}_delta_integration\{}\integration\kor_{}_bufo.shp".format(release,city,city)
			remove_delta_source = r"C:\Users\pruszyns\Desktop\output\{}\{}_{}_delta_minus.shp".format(city,city,release)
		
		
			# Creating Feature Layers
			arcpy.MakeFeatureLayer_management(city_source, "source")
			arcpy.MakeFeatureLayer_management(remove_delta_source, "remove_delta")
			
			
			status("Cleaning delta minus polygons...")
			
			
			# Selecting polygons to remove from the source
			arcpy.SelectLayerByLocation_management("source", "HAVE_THEIR_CENTER_IN", "remove_delta", "", "NEW_SELECTION")
			
			
			# Unselecting records with LMID filled
			arcpy.SelectLayerByAttribute_management ("source", "REMOVE_FROM_SELECTION", """ LMID <> '' """)
			selected_count = arcpy.GetCount_management("source")
			
			
			status("Number of records that will be removed: ", selected_count)
					
					
			# Removing polygons from the source		
			arcpy.DeleteRows_management("source")
			
			
			# Cleanup
			arcpy.Delete_management("source")
			arcpy.Delete_management("remove_delta")
			
			
			status("FINISHED removing delta for ", city)
			
			
		except Exception as err:
			status("Exception found in ", city)
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
			arcpy.Delete_management("source")
			arcpy.Delete_management("remove_delta")
			continue
			
			
	status("Application finished.")

main()
log_file.close()	