# Import arcpy module
import arcpy

def status(content, city = ""):
	print "{}{}".format(content,city)
	log_file.write("{}{}\n".format(content,city))

log_file = open(r"C:\Tools\pyScripts\self_intersect\log.txt", "w")
input_dir = r"C:\Tools\pyScripts\self_intersect\input"
output_dir = r"C:\Tools\pyScripts\self_intersect\output"

cities = ["changwon_si","daegu","seongnam_si","yongin_si","daejeon","incheon","gwangju","ulsan","seoul","busan","suwon_si"]

for city in cities:

	status("Working on... ",city)
	
	source_path = input_dir + "\{}\kor_{}_bufo.shp".format(city,city)
	output_path = output_dir + "\{}_intersect.shp".format(city)
	
	arcpy.MakeFeatureLayer_management(source_path, "Source")
	arcpy.Intersect_analysis("Source",output_path)
	
	arcpy.Delete_management("Source")
	
	status("FINISHED ",city)

log_file.close()	