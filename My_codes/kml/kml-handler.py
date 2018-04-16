from lxml import etree as ET

tree = ET.parse('doc.kml')
root = tree.getroot()

print(root.getchildren()[0].getchildren())

#cosmodromes = [n for names in root.findall("name")]

#print(cosmodromes)