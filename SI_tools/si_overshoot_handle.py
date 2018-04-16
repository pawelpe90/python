import os

region = "eur"
release = "2018.03"
previous_release = "2017.12"

overshoot_log_path = r"C:\Users\pruszyns\Desktop\6_Signposts\{}\{}\overshoots".format(release, region)

output = open("{}\{}{}_overshoots.txt".format(overshoot_log_path, region, release), "w")
output2 = open("{}\{}{}_overshoots_new.txt".format(overshoot_log_path, region, release), "w")

container = []

logs = os.listdir(overshoot_log_path)

for element in logs:
    with open("{}\{}".format(overshoot_log_path, element), "r") as f:
        content = f.readlines()
        for item in content:
            if item not in container:
                container.append(item)

for e in container:
    output.write(e)

old = r"C:\Users\pruszyns\Desktop\6_Signposts\{}\{}\overshoots\{}{}_overshoots.txt".format(previous_release, region, region, previous_release)
new = r"C:\Users\pruszyns\Desktop\6_Signposts\{}\{}\overshoots\{}{}_overshoots.txt".format(release, region, region, release)

with open(old, "r") as o:
    old_content = o.readlines()

with open(new, "r") as n:
    new_content = n.readlines()

for element in new_content:
    if element not in old_content:
        output2.write(element)