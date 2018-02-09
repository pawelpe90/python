import datetime as dt
import arcpy
import os


def get_time():
    return str(dt.datetime.now())[:19].replace(":", "-")


log_file = open(r"C:\Users\pruszyns\Desktop\logs\{} bld-extractor-log.txt".format(get_time()), "w")


def status(content, city=""):
    time = get_time()
    print "{} {}{}".format(time, content, city)
    log_file.write("{} {}{}\n".format(time, content, city))


def scope_selector():
    with open(r"C:\Users\pruszyns\Desktop\python-repo\python\BLD_korea\scope.txt", "r") as fscope:
        scope = fscope.readlines()
        scope_fix = [element.strip() for element in scope]

        return [i for i in scope_fix if not i.startswith("#")]


def main():
    release = "2017_09"

    # Local variables:
    # CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures"
    attribute_template = r"C:\Tools\pyScripts\bld_extractor\templates\template.shp"
    spatial_ref = r"C:\Tools\pyScripts\bld_extractor\templates\template.prj"
    output_path = r"C:\city\Building_layer\07_raw_data\{}".format(release)
    extents_path = r"C:\city\Extents\BLD\{}\coverage_buildings.shp".format(release)

    # Set working environment
    arcpy.env.workspace = r"C:\city\Building_layer\06_public_sources\kor{}.gdb".format(release)
    fcs = arcpy.ListFeatureClasses()

    cities = scope_selector()

    for city in cities:

        try:

            # Checking if file already exists
            shape_path = r"{}\{}\{}_{}_raw.shp".format(output_path, city, city, release)

            if os.path.exists(shape_path):
                status("Raw files already exist for ", city)
                continue

            status("Working on... ", city)

            # Create city folder
            path = output_path + "\\" + city

            if not os.path.exists(path):
                os.makedirs(path)

            # Create shapefile
            arcpy.CreateFeatureclass_management(output_path, "{}\{}_{}_raw".format(city, city, release), "POLYGON",
                                                attribute_template, "", "", spatial_ref)
            CopiedFeatures = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeatures_{}".format(city)
            CopiedFeaturesExtent = "C:\\Users\\pruszyns\\Documents\\ArcGIS\\Default.gdb\\CopiedFeaturesExtent_{}".format(
                city)

            # Extent separation
            arcpy.MakeFeatureLayer_management(extents_path, "Extent")
            arcpy.SelectLayerByAttribute_management("Extent", "NEW_SELECTION", """ CITY = '{}' """.format(city))
            arcpy.CopyFeatures_management("Extent", CopiedFeaturesExtent)

            # Extent file location
            extent = CopiedFeaturesExtent

            fc_Layer = city

            status("Building city...")

            for fc in fcs:
                # Process: Make Feature Layer
                arcpy.MakeFeatureLayer_management(fc, fc_Layer)

                # Process: Define Projection
                arcpy.DefineProjection_management(fc_Layer,
                                                  "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")

                # Process: Select Layer By Location
                arcpy.SelectLayerByLocation_management(fc_Layer, "HAVE_THEIR_CENTER_IN", extent)

                # Process: Copy Features
                arcpy.CopyFeatures_management(fc_Layer, CopiedFeatures)

                # Process: Append
                arcpy.Append_management(CopiedFeatures, output_path + "\{}\{}_{}_raw.shp".format(city, city, release),
                                        "NO_TEST")

                arcpy.Delete_management(fc_Layer)
                arcpy.Delete_management(CopiedFeatures)

            arcpy.Delete_management("Extent")
            arcpy.Delete_management(CopiedFeaturesExtent)

            status("FINISHED FOR ", city)

        except Exception as err:
            status("Exception found in ", city)
            log_file.write(str(err.args[0]))
            print "\nScript will continue with the next city. Check logfile to find more details about exception.\n"
            arcpy.Delete_management("Extent")
            arcpy.Delete_management(CopiedFeatures)
            continue

    status("Application finished.")


main()
log_file.close()
