#name_for_userid = {
#    382: "Alice",
#    590: "Bob",
#    951: "Dilbert",
#}
#
#def greeting(userid):
#    return "Hi %s!" % name_for_userid.get(userid, "there")
#
#print greeting(382)
#print(greeting(333333))
import os

dir = r"D:\8_2DCM\1803_test_oce\1709\shp\2dcm\nzl\nw1"

def funct(dir):
    for root,dirs,filenames in os.walk(dir):
            for file in filenames:
                    if file.endswith("dbd.shp"):
                            print root + "\\" + file

def funct_test(dir):
    for root,dirs,filenames in os.walk(dir):
            print "This is root:", root
            print "These are dirs:", dirs
            print "These are filenames:", filenames
            print("\n")

funct(dir)