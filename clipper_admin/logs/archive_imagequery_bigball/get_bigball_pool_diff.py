import os

import sys
os.system("cat " + sys.argv[1]  + " | grep Time | grep c1 | cut -d\" \" -f5 > c1_bigball_100req.log")
os.system("cat " + sys.argv[1]  + " | grep Time | grep pool | cut -d\" \" -f5 > pool_bigball_100req.log")


with open("./c1_bigball_100req.log") as c1_file:
	c1_times = c1_file.readlines()
c1_file.close()

with open("./pool_bigball_100req.log") as pool_file:
	pool_times = pool_file.readlines()
pool_file.close()


c1_time_list = [t.strip() for t in c1_times]
pool_time_list = [t.strip() for t in pool_times]

diff_list = []
for i in range(len(c1_time_list)):
	diff = float( pool_time_list[i]) - float( c1_time_list[i])
	diff_list.append(diff)

diff_sum = 0

for diff in diff_list:
  	diff_sum += diff
print("100 request: Total diff c1 from pool: " + str(diff_sum))


c1_total = 0
for i in c1_time_list:
  	c1_total += float(i)
c1_average = c1_total / len(c1_time_list)
print("100 request: c1 average time in bigBall: " + str(c1_average))

os.system("rm c1_bigball_100req.log pool_bigball_100req.log")





