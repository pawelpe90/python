# Creating Feature Layers
arcpy.MakeFeatureLayer_management(path_to_file, "fcname")

# Getting count
arcpy.GetCount_management("fcname")

# Copy features
arcpy.CopyFeatures_management("fcname", path_to_file)

# Use to search over records values
arcpy.SearchCursor(path_to_file, fields="field1;field2;...")
	> row.getValue("field")
	
# Remove selected polygons
arcpy.DeleteRows_management("fcname")

#Remove feature classes of files
arcpy.Delete_management("fcname" or path_to_file)

# Create shapefile
arcpy.CreateFeatureclass_management(path_to_file, "fcname", "POLYGON", attribute_template, "", "", spatial_ref)