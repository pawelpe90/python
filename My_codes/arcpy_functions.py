# Creating Feature Layers
arcpy.MakeFeatureLayer_management(path_to_file, "fcname")

# Getting count
arcpy.GetCount_management("fcname")

# Copy features
arcpy.CopyFeatures_management("fcname", path_to_file)

# Copy data on disc
Copy_management (in_data, out_data, {data_type})

# Use to search over records values
arcpy.SearchCursor(path_to_file, fields="field1;field2;...")
	> row.getValue("field")
	
# Remove selected polygons
arcpy.DeleteRows_management("fcname")

#Remove feature classes of files
arcpy.Delete_management("fcname" or path_to_file)

# Create shapefile
arcpy.CreateFeatureclass_management(path_to_file, "fcname", "POLYGON", attribute_template, "", "", spatial_ref)

# Add column
arcpy.AddField_management(fc, "ID1", "TEXT", field_length = 7)

# Delete columns
arcpy.DeleteField_management(fc, drop_fields)

# Calculate Field Value
arcpy.CalculateField_management(fc, "field", id1)

# Generate stats
statsFields  = [["field1", "MEAN"], ["field1", "STD"]]
arcpy.Statistics_analysis(source, out_table, statsFields)

# Select features by atribute
arcpy.SelectLayerByAttribute_management ("source", "REMOVE_FROM_SELECTION", """ LMID <> '' """)

# Select features by location
arcpy.SelectLayerByLocation_management("source", "HAVE_THEIR_CENTER_IN", "remove_delta", "", "NEW_SELECTION")

# Append features
Append_management (inputs, target, {schema_type}, {field_mapping}, {subtype})

# Dissolve features
Dissolve_management(in_features, out_feature_class, {dissolve_field;dissolve_field...}, {statistics_fields;statistics_fields...}, {multi_part}, {unsplit_lines})

    Aggregates features based on specified attributes.

# Erase features (substract one from another)
Erase_analysis(in_features, erase_features, out_feature_class, {cluster_tolerance})