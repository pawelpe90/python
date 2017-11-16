import datetime as dt
import os
import shutil


def get_time():
	return str(dt.datetime.now())[:19].replace(":", "-")

log_file = open(r"C:\Users\pruszyns\Desktop\logs\{} bld-prepare-validation-log.txt".format(get_time()), "w")	


def status(content, city = ""):
	time = get_time()
	print "{} {}{}".format(time, content, city)
	log_file.write("{} {}{}\n".format(time, content, city))
	
	
def main():
	
	validation_path = r"C:\city\Building_layer\02_operations\XX_validation"
	lm_release = "2017_12"
	release = "2017_09"
	cities = ["incheon"]
	
	for city in cities:
	
		try:
			
			status("Creating validation directories for ", city)
			
			
			city_dir = validation_path + "\{}".format(city)
			
			if not os.path.exists(city_dir):
				os.makedirs(city_dir)
				
			bld = city_dir + "\bld"
			
			if not os.path.exists(bld):
				os.makedirs(bld)
				
			lm = city_dir + "\3dlm"
			
			if not os.path.exists(lm):
				os.makedirs(lm)
			
			
			status("Copying 3dlm...")
			
			
			lm_source_dir = r"C:\city\Extents\3DLM\kor\{}".format(lm_release)
			
			elements = os.listdir(lm_source_dir)
			
			for element in elements:
				shutil.copy(lm_source_dir + "\{}".format(element), lm)
				
			
			status("Copying buildings layer...")
			
			
			bld_source_dir = r"C:\city\Building_layer\02_operations\{}_delta_integration\{}\integration".format(release,city)
			
			elements = os.listdir(bld_source_dir)
			
			for element in elements:
				shutil.copy(bld_source_dir + "\{}".format(element), bld)
			
			
		except Exception as err:
		
			status("Exception found in ", city)
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
			
			continue
			
			
	status("Application finished.")
		
		
main()
log_file.close()