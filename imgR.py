crop_list = []
# these do not change
UPPER = 0
LOWER = 50
origin_crop = 0,1000
number_partition = 1000
# returns the starting position of each segment
partsize = int(origin_crop[1]/number_partition)
rstart = list(range(0,int(origin_crop[1]),partsize))
remainder = (int(origin_crop[1]%number_partition))
print (rstart)

# return the crop list
for partition in range(0, number_partition):
	crop_list.append([rstart[partition], UPPER, rstart[partition]+ partsize, LOWER])

if (remainder):
	crop_list.append([origin_crop[1]-remainder, UPPER, origin_crop[1] , LOWER])
print(crop_list)




	
