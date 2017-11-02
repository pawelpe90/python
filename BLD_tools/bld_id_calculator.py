#Script allows to calculate ID for single city in BLD format.
#Total number of polygons < 1M.

import arcpy
from Tkinter import Tk
from tkFileDialog import askopenfilename

def input_taker():
    while True:
        id1 = str(raw_input("ISOCountryCode, CityCode, SourceID (eg. 8881113): "))
        if len(id1) == 7:
            return id1
            break
        else:
            print "Invalid pattern!"

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

def messager(fc):
    msgCount = arcpy.GetMessageCount()
    message = (arcpy.GetMessage(msgCount-1)).split(" ")
    if message[0] == "Succeeded":
        print "Process finished successfully for " + fc[-17:] + "!"
    else:
        print "Something went wrong!"

def main():
    drop_fields = ["ID1", "ID2"]
    opts = {}
    opts['filetypes'] = [('Shape files','.shp')]

    Tk().withdraw()
    fc = askopenfilename(**opts)

    id1 = input_taker()
    adder(fc)
    calculator(fc,id1)
    cleaner(fc,drop_fields)
    messager(fc)

main()