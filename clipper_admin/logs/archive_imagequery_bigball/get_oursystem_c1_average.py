


with open("./c1_oursystem_100req.log") as c1_file:
        c1_times = c1_file.readlines()
c1_file.close()
# print(c1_times)

total = 0
for t in c1_times:
    total += float(t)

print("Total: " + str(total))

print("c1 Average time on our system: " + str(total/len(c1_times)))
