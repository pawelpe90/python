import datetime as dt
import arcpy
from arcpy import env
import os
import glob

env.workspace = r"D:\14_buildings_layer\analysis\ukraine\python\extent_fixer"
env.overwriteOutput = True

def get_time():
    return str(dt.datetime.now())[:19].replace(":", "-")

log_file = open(r"D:\14_buildings_layer\analysis\ukraine\python\extent_fixer\{} extent-fixer-log.txt".format(get_time()), "w")
    
def status(content, city = ""):
    time = get_time()
    print "{} {}{}".format(time, content, city)
    log_file.write("{} {}{}\n".format(time, content, city))
    
def scope_selector():
    with open(r"D:\14_buildings_layer\analysis\ukraine\python\extent_fixer\scope.txt", "r") as fscope:
        scope = fscope.readlines()
        scope_fix = [element.strip() for element in scope]
        scope_filtered = [i for i in scope_fix if not i.startswith("#")]
    return scope_filtered
    
def cleaner(CopiedFeatures,CopiedFeaturesDis,CopiedFeaturesAdjacent,Erase,CopiedFeaturesOutside):
    arcpy.Delete_management("input_source")
    arcpy.Delete_management("extent_source")
    arcpy.Delete_management("target_source")
    arcpy.Delete_management("coverage_buildings")
    arcpy.Delete_management(CopiedFeatures)
    arcpy.Delete_management(CopiedFeaturesDis)
    arcpy.Delete_management(CopiedFeaturesAdjacent)
    arcpy.Delete_management(CopiedFeaturesOutside)
    arcpy.Delete_management(Erase)
    
def main():

    cities = scope_selector()
    
    for city in cities:
        try:
            input_raw = glob.glob(r"D:\14_buildings_layer\analysis\ukraine\python\extent_fixer\logs\*{}\*\2017_12_07*\ExtentCheck_20_1.shp".format(city))
            input = input_raw[0]
            extent = r"D:\14_buildings_layer\analysis\ukraine\python\extent_fixer\coverage_buildings.shp"
            
            # Temp files preparation
            CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures_{}".format(city)
            CopiedFeaturesDis = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeaturesDis_{}".format(city)
            CopiedFeaturesAdjacent = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeaturesAdjacent_{}".format(city)
            CopiedFeaturesOutside = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeaturesOutside_{}".format(city)
            Erase = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\Erase_{}".format(city)
            
            # Temp layers preparation
            arcpy.MakeFeatureLayer_management(input, "input_source")
            arcpy.MakeFeatureLayer_management(extent, "extent_source")
            
            # Separate city's extent
            arcpy.SelectLayerByAttribute_management ("extent_source", "NEW_SELECTION", """ CITY = '{}' """.format(city))
            arcpy.CopyFeatures_management("extent_source", CopiedFeatures)
            arcpy.MakeFeatureLayer_management(CopiedFeatures, "target_source")
            
            # Getting citiy's attrubute values
            rows = arcpy.SearchCursor(CopiedFeatures, fields="Country;UTM;Region;CITY;TYPE;AREA")
            
            for row in rows:
                country = row.getValue("Country")
                utm = row.getValue("UTM")
                region = row.getValue("Region")
                city_name = row.getValue("CITY")
                type = row.getValue("TYPE")
                area = row.getValue("AREA")
            
            # Appending logged extent polygons to target city
            arcpy.Append_management ("input_source", CopiedFeatures, "NO_TEST")
            
            # Attrubution newly added records
            arcpy.CalculateField_management(CopiedFeatures, "Country", repr(country), "PYTHON_9.3")
            arcpy.CalculateField_management(CopiedFeatures, "UTM", repr(utm), "PYTHON_9.3")
            arcpy.CalculateField_management(CopiedFeatures, "Region", repr(region), "PYTHON_9.3")
            arcpy.CalculateField_management(CopiedFeatures, "CITY", repr(city_name), "PYTHON_9.3")
            arcpy.CalculateField_management(CopiedFeatures, "TYPE", repr(type), "PYTHON_9.3")
            arcpy.CalculateField_management(CopiedFeatures, "AREA", repr(area), "PYTHON_9.3")
            
            # Dissolving (city's extent and appended records)
            arcpy.Dissolve_management(CopiedFeatures, CopiedFeaturesDis, ["Country","UTM","Region","CITY","TYPE","AREA"])
            
            arcpy.MakeFeatureLayer_management(CopiedFeaturesDis, "dissolved")
            
            # Selecting adjacent polygons
            arcpy.SelectLayerByLocation_management("extent_source", "INTERSECT", "dissolved", "", "NEW_SELECTION")
            arcpy.SelectLayerByAttribute_management("extent_source", "REMOVE_FROM_SELECTION", """ CITY = '{}' """.format(city))
            
            # Adjacent polygons as a separate file
            arcpy.CopyFeatures_management("extent_source", CopiedFeaturesAdjacent)
            
            # Substracting dissolved city from adjacent polygons
            arcpy.Erase_analysis(CopiedFeaturesAdjacent, CopiedFeaturesDis, Erase)
            
            # Separating remianing polygons (neither target city, nor adjacent)
            arcpy.SelectLayerByLocation_management("extent_source", "INTERSECT", "dissolved", "", "SWITCH_SELECTION")
            arcpy.SelectLayerByAttribute_management("extent_source", "REMOVE_FROM_SELECTION", """ CITY = '{}' """.format(city))
            
            # Remaining polygons as a separate file
            arcpy.CopyFeatures_management("extent_source", CopiedFeaturesOutside)
            
            # Appending ALL elements into one extent file
            arcpy.Append_management ([Erase,CopiedFeaturesDis], CopiedFeaturesOutside, "NO_TEST")
            
            arcpy.MakeFeatureLayer_management(CopiedFeaturesOutside, "coverage_buildings")
            
            # Overwriting input source
            arcpy.CopyFeatures_management("coverage_buildings", r"D:\14_buildings_layer\analysis\ukraine\python\extent_fixer\coverage_buildings.shp")
            
            status("FINISHED for ", city)
            
            # Clean up
            cleaner(CopiedFeatures,CopiedFeaturesDis,CopiedFeaturesAdjacent,Erase,CopiedFeaturesOutside)
            
        except Exception as err:
            status("Exception found in ", city)
            log_file.write(str(err.args[0]))
            print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
            cleaner(CopiedFeatures,CopiedFeaturesDis,CopiedFeaturesAdjacent,Erase,CopiedFeaturesOutside)
            continue
        
    status("Application finished.")
    
main()
log_file.close()