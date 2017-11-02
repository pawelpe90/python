#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      pruszyns
#
# Created:     13/09/2017
# Copyright:   (c) pruszyns 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

log_file = open(r"C:\Users\pruszyns\Desktop\testing\log.txt", "w")
output_file = open(r"C:\Users\pruszyns\Desktop\testing\output.txt", "w")
output_file.write("CityName,TotalPolyCount,2dCount,acmlod1Count,acmCount,3dlmRelatedTotal,3dlm2dRelated,3dlmACMlod1Related,3dlmACMRelated,3dlmIntegrated\n")

def status(content, city = ""):
	print "{} {}".format(content,city)
	log_file.write("{}{}\n".format(content,city))

def clean_up(lyr):
    arcpy.Delete_management(lyr)

def main():

    cities = ["ottawa"]

    try:
        for city in cities:

            status("Working on... ",city)

            CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures{}".format(city)
            city_path = r"C:\Users\pruszyns\Desktop\testing\{}\can_{}_bufo.shp".format(city,city)
            arcpy.MakeFeatureLayer_management(city_path, "City")

            #Counting total polygon number
            total_count = arcpy.GetCount_management("City")

            #Counting 2D polygon number
            arcpy.SelectLayerByAttribute_management("City","NEW_SELECTION", """ ID like '______3_________' """)
            count_2d = arcpy.GetCount_management("City")

            #Counting acmlod1 polygon number
            arcpy.SelectLayerByAttribute_management("City","NEW_SELECTION", """ ID like '______2_________' """)
            count_acmlod1 = arcpy.GetCount_management("City")

            #Counting acm polygon number
            arcpy.SelectLayerByAttribute_management("City","NEW_SELECTION", """ ID like '______1_________' """)
            count_acm = arcpy.GetCount_management("City")

            #Counting total 3dlm related polygon number
            arcpy.SelectLayerByAttribute_management("City","NEW_SELECTION", """ LMID <> '' """)
            total_3dlm_related = arcpy.GetCount_management("City")

            #Counting 3dlm integrated
            arcpy.CopyFeatures_management("City", CopiedFeatures)
            rows = arcpy.SearchCursor(CopiedFeatures,fields="LMID")
            container3dlm = []

            for row in rows:
                container3dlm.append(row.getValue("LMID"))

            count_3dlm = len(set(container3dlm))

            #Counting 2d 3dlm related polygons
            arcpy.SelectLayerByAttribute_management("City","NEW_SELECTION", """ LMID <> '' AND ID like '______3_________' """)
            count_3dlm_2d = arcpy.GetCount_management("City")

            #Counting acmlod1 3dlm related polygons
            arcpy.SelectLayerByAttribute_management("City","NEW_SELECTION", """ LMID <> '' AND ID like '______2_________' """)
            count_3dlm_acmlod1 = arcpy.GetCount_management("City")

            #Counting acm 3dlm related polygons
            arcpy.SelectLayerByAttribute_management("City","NEW_SELECTION", """ LMID <> '' AND ID like '______1_________' """)
            count_3dlm_acm = arcpy.GetCount_management("City")

            output_file.write("{},{},{},{},{},{},{},{},{},{}\n".format(city,total_count,count_2d,count_acmlod1,count_acm,total_3dlm_related,count_3dlm_2d,count_3dlm_acmlod1,count_3dlm_acm,count_3dlm))

            #Clean up
            clean_up("City")
            clean_up(CopiedFeatures)

            status("FINISHED FOR ", city)

            log_file.close()
            output_file.close()

    except Exception as err:
        print(err.args[0])
        clean_up("City")
        clean_up(CopiedFeatures)

main()











