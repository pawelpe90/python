import datetime as dt
import arcpy
import os


def get_time():
	return str(dt.datetime.now())[:19].replace(":", "-")

log_file = open(r"C:\Users\pruszyns\Desktop\logs\{} bld-prepare-delta-log.txt".format(get_time()), "w")	

def status(content, city = ""):
	time = get_time()
	print "{} {}{}".format(time, content, city)
	log_file.write("{} {}{}\n".format(time, content, city))

def calculator(fc, id_max):
    arcpy.CalculateField_management(fc, "ID", "str(!FID! + 1 + {})".format(id_max), "PYTHON")
    arcpy.CalculateField_management(fc, "GRNDHEIGHT", "-1")
    arcpy.CalculateField_management(fc, "HEIGHT", "-1")	
	
def scope_selector():
    with open(r"C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\scope.txt", "r") as fscope:
        scope = fscope.readlines()
        scope_fix = [element.strip() for element in scope]
		scope_filtered = [i for i in scope_fix if not i.startswith("#")]
    return scope_filtered
	
def main():

	release = "2017_09"
	output_path = r"C:\Users\pruszyns\Desktop\output"
	attribute_template = r"C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_delta_handler\template\kor_city_bufo.shp"
	spatial_ref = r"C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\bld_delta_handler\template\kor_city_bufo.prj"
	
	cities = scope_selector()
	
	for city in cities:
	
		try:
		
			status("Working on... ",city)
			
			
			city_source = r"C:\city\Building_layer\02_operations\{}_delta_integration\{}\integration\kor_{}_bufo.shp".format(release,city,city)
			add_delta_source = r"{}\{}\{}_{}_delta_plus.shp".format(output_path,city,city,release)
			arcpy.CreateFeatureclass_management(output_path, "{}\kor_{}_bufo.shp".format(city,city), "POLYGON", attribute_template, "", "", spatial_ref)
			delta_target = output_path + "\{}\kor_{}_bufo.shp".format(city,city)
			CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures_{}".format(city)
		
			# Creating Feature Layers
			arcpy.MakeFeatureLayer_management(city_source, "source")
			arcpy.MakeFeatureLayer_management(add_delta_source, "add_delta")
			arcpy.MakeFeatureLayer_management(delta_target, "delta_target")
			
			
			status("Getting max id...")
			
			
			# Getting max id value for reattribute
			arcpy.CopyFeatures_management("source", CopiedFeatures)
			rows = arcpy.SearchCursor(CopiedFeatures,fields="ID")
			idcontainer = []
		
			for row in rows:
				idcontainer.append(row.getValue("ID"))
				
			id_max = max(idcontainer)
			
			
			status("Appending...")
			
			
			# Appending source delta to target delta
			arcpy.Append_management("add_delta", "delta_target", "NO_TEST")
			
			
			status("Attributing...")
		
		
			# Attributing target delta
			calculator("delta_target", id_max)
			
			# Cleanup
			arcpy.Delete_management("source")
			arcpy.Delete_management("add_delta")
			arcpy.Delete_management(CopiedFeatures)
			arcpy.Delete_management("delta_target")
			
			
			status("FINISHED adding delta for ", city)

			dir = output_path + r"\{}\bld".format(city)
	
			if not os.path.exists(dir):
				os.makedirs(dir)
			
			
		except Exception as err:
			status("Exception found in ", city)
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
			arcpy.Delete_management("source")
			arcpy.Delete_management("add_delta")
			arcpy.Delete_management(CopiedFeatures)
			arcpy.Delete_management("delta_target")
			continue
			
			
	status("Application finished.")	
	


main()
log_file.close()	