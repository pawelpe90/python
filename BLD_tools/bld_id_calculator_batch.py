import arcpy

def adder(fc):
    arcpy.AddField_management(fc, "ID1", "TEXT", field_length = 7)
    arcpy.AddField_management(fc, "ID2", "DOUBLE", field_length = 9)

def calculator(fc, id1):
    arcpy.CalculateField_management(fc, "ID1", id1)
    arcpy.CalculateField_management(fc, "ID2", "100000000 + [OBJECTID]")
    arcpy.CalculateField_management(fc, "ID", "!ID1! + str(!ID2!)", "PYTHON")
    arcpy.CalculateField_management(fc, "GRNDHEIGHT", "-1")
    arcpy.CalculateField_management(fc, "HEIGHT", "-1")

def cleaner(fc, drop_fields):
    arcpy.DeleteField_management(fc, drop_fields)

def messager():
    msgCount = arcpy.GetMessageCount()
    message = (arcpy.GetMessage(msgCount-1)).split(" ")
    if message[0] == "Succeeded":
        print "Process finished successfully for " + str(fc) + "!"
    else:
        print "Something went wrong!"

def main():
    arcpy.env.workspace = "C:\\Users\\pruszyns\\Desktop\\python in arc map\\test.gdb"

    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:
        id1_a = str(raw_input("ISO Country Code (3 digits) for: " + str(fc)))
        id1_b = str(raw_input("City Code (3 digits) for: " + str(fc)))
        id1_c = str(raw_input("Source Identifier (1,2 or 3) for: " + str(fc)))

        id1 = id1_a + id1_b + id1_c

        drop_fields = ["ID1", "ID2"]
        adder(fc)
        calculator(fc,id1)
        cleaner(fc,drop_fields)
        messager()

main()


