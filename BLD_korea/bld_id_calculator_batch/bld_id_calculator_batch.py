import arcpy
import json
import os

log_file = open(r"C:\Tools\pyScripts\bld_id_calculator_batch\log.txt", "w")
template = r"C:\Tools\pyScripts\bld_id_calculator_batch\template\kor_city_bufo.shp"
spatial_template = r"C:\Tools\pyScripts\bld_id_calculator_batch\template\kor_city_bufo.prj"
input_dir = r"C:\Tools\pyScripts\bld_id_calculator_batch\input"
output_dir = r"C:\Tools\pyScripts\bld_id_calculator_batch\output"
display_db_path = r"C:\Tools\pyScripts\bld_id_calculator_batch\display_db_korea.json"

def status(content, city = ""):
	print "{}{}".format(content,city)
	log_file.write("{}{}\n".format(content,city))

def concat(list):
	result = ""
	for line in list:
		result += line
	return result

def load_data(display_db_path):
	with open(display_db_path, "r") as f:
		body = concat(f.readlines())
		display = json.loads(body)
		return display

def search(display,value):
    for record in display:
        if record["CityName"] == value:
            return record["Numeric codes (ACM)"]
			
def adder(fc):
	arcpy.AddField_management(fc, "ID1", "TEXT", field_length = 7)
	arcpy.AddField_management(fc, "ID2", "DOUBLE", field_length = 9)

def calculator(fc, id1):
    arcpy.CalculateField_management(fc, "ID1", id1)
    arcpy.CalculateField_management(fc, "ID2", "100000000 + ([FID] + 1)")
    arcpy.CalculateField_management(fc, "ID", "!ID1! + str(!ID2!)", "PYTHON")
    arcpy.CalculateField_management(fc, "GRNDHEIGHT", "-1")
    arcpy.CalculateField_management(fc, "HEIGHT", "-1")

def cleaner(fc, drop_fields):
	arcpy.DeleteField_management(fc, drop_fields)

def messager(city):
	msgCount = arcpy.GetMessageCount()
	message = (arcpy.GetMessage(msgCount-1)).split(" ")
	if message[0] == "Succeeded":
		print "Process finished successfully for " + str(city) + "!"
	else:
		print "Something went wrong!"
		
def main():
	
	cities = ["changwon_si","daegu","daejeon","seoul","gwangju","incheon","busan","chungcheongbuk_do","chungcheongnam_do","jeju_do","seongnam_si","gyeongsangbuk_do","gyeongsangnam_do","gangwon_do","gyeonggi_do","suwon_si","jeollabuk_do","jellanam_do","ulsan","sejong_si","yongin_si"]
	
	for city in cities:
	
		status("Working on... ",city)
		
		# Create city folder
		path = output_dir + "\\" + city

		if not os.path.exists(path):
			os.makedirs(path)
	
		# Create empty file in bld format
		arcpy.CreateFeatureclass_management(output_dir + "\{}\\".format(city), "kor_{}_bufo".format(city), "POLYGON", template, "", "", spatial_template)
		
		raw_city_path = input_dir + "\{}\{}_1706_raw.shp".format(city,city)
		city_path = output_dir + "\{}\kor_{}_bufo.shp".format(city,city)
		
		arcpy.Append_management(raw_city_path, city_path, "NO_TEST")
	
		arcpy.MakeFeatureLayer_management(city_path, "City")
		
		country_code = "410"
		source_code = "3"
		display = load_data(display_db_path)
		city_code = search(display,city)
		city_code = "000" + str(city_code)
		id1 = country_code + city_code[-3:] + source_code

		drop_fields = ["ID1", "ID2"]
		adder("City")
		calculator("City",id1)
		cleaner("City",drop_fields)
		#messager()
		
		arcpy.Delete_management("City")
		
		status("FINISHED FOR ", city)
	
	log_file.close()
	
main()


