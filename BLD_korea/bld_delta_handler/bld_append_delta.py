import datetime as dt
import arcpy
import os

def get_time():
	return str(dt.datetime.now())[:19].replace(":", "-")

log_file = open(r"C:\Users\pruszyns\Desktop\logs\{} bld-append-delta-log.txt".format(get_time()), "w")	

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

	release = "2017_09"
	output_path = r"C:\Users\pruszyns\Desktop\output"
	
	cities = scope_selector()
		
	for city in cities:
	
		try:
		
			status("Working on... ",city)
			
			
			files_to_add = output_path + r"\{}\bld\kor_{}_bufo.shp".format(city,city)
			city_to_process = r"C:\city\Building_layer\02_operations\{}_delta_integration\{}\integration\kor_{}_bufo.shp".format(release,city,city)
			
			arcpy.MakeFeatureLayer_management(files_to_add, "Add")
			arcpy.MakeFeatureLayer_management(city_to_process, "City")
			
			
			status("Appending delta files... ")
			
			
			arcpy.Append_management("Add", "City", "TEST")
			
			arcpy.Delete_management("Add")
			arcpy.Delete_management("City")
			
			
			status("FINISHED FOR ", city)
			
			
		except Exception as err:
		
			status("Exception found in ", city)
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
			arcpy.Delete_management("Add")
			arcpy.Delete_management("City")
			
			continue
			
			
	status("Application finished.")
	
	
main()			
log_file.close()