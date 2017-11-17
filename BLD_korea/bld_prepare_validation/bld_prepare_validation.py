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
				
			bld = city_dir + r"\bld"
			
			if not os.path.exists(bld):
				os.makedirs(bld)
				
			lm = city_dir + r"\3dlm"
			
			if not os.path.exists(lm):
				os.makedirs(lm)
				
			extents = city_dir + r"\extents"
			
			if not os.path.exists(extents):
				os.makedirs(extents)
			
			
			status("Copying 3dlm...")
			
			
			lm_source_dir = r"C:\city\Extents\3DLM\kor\{}".format(lm_release)
			
			elements = os.listdir(lm_source_dir)
			
			for element in elements:
				if not os.path.exists(lm + "\{}".format(element)):
					shutil.copy(lm_source_dir + "\{}".format(element), lm)
				else:
					status("File already exist: ",element)
				
			
			status("Copying buildings layer...")
			
			
			bld_source_dir = r"C:\city\Building_layer\02_operations\{}_delta_integration\{}\integration".format(release,city)
			
			elements = os.listdir(bld_source_dir)
			
			for element in elements:
				if not os.path.exists(bld + "\{}".format(element)):
					shutil.copy(bld_source_dir + "\{}".format(element), bld)
				else:
					status("File already exist: ",element)
			
			
			status("Copying extents...")
			
			
			product_types = ["ACM","ACMLOD1","BLD"]
			
			for product in product_types:
			
				extents_source_dir = r"C:\city\Extents\{}\{}".format(product,lm_release)
				
				elements = os.listdir(extents_source_dir)
				
				if not os.path.exists(extents + r"\{}".format(product)):
					os.makedirs(extents + r"\{}".format(product))
				
				for element in elements:
					try:
						if not os.path.exists(extents + "\{}\{}".format(product, element)):
							shutil.copy(extents_source_dir + "\{}".format(element), extents + r"\{}".format(product))
						else:
							status("File already exist: ",element)
					except Exception as err:
						status("Exception:" ,str(err))
						continue
				
			
		except Exception as err:
		
			status("Exception found in ", city)
			status("Exception:" ,str(err))
			log_file.write(str(err.args[0]))
			print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"

			continue
			
			
	status("Application finished.")
		
		
main()
log_file.close()