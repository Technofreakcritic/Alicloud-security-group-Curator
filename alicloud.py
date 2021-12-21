import os
import subprocess

# 1. Get List of Region Id
# 2. Search for SecurityGroupIds
# 3. Check the SecurityGroup Description


#Aliyun Get Regions
cmd ="aliyun ecs DescribeRegions | grep RegionId | cut -d ' ' -f2"

aliyun_get_regions = os.popen(cmd).read()

#Region List Formatting
aliyun_get_regions = aliyun_get_regions.replace("\"","")
aliyun_region_list = list(aliyun_get_regions.split("\n"))

#Print List of Regions
print("No. of regions found: "+str(len(aliyun_region_list)))
print("List of Regions: \n")
print(*aliyun_region_list,sep = "\n")

#Empty placeholders
aliyun_security_group_list=[]
aliyun_regions_holder=[]

print("\n\n")

for i in aliyun_region_list:
	# print(i)
	cmd = "aliyun ecs DescribeSecurityGroups --RegionId "+i+" | grep SecurityGroupId "
	print(cmd)
	aliyun_security_cmd = os.popen(cmd).read()

	SecurityGroup_holder = aliyun_security_cmd.split("\"SecurityGroupId\":")
	if(SecurityGroup_holder==['']):
		print("Nah Fam \n")
	else:
		print("Got some sec Stuff",SecurityGroup_holder)
		aliyun_security_group_list.append(aliyun_security_cmd.split("\"SecurityGroupId\":"))
		aliyun_regions_holder.append(i)


print("Total Groups: ",len(aliyun_security_group_list))
print("List of Regions that have Security Groups \n",aliyun_regions_holder)
print("\n\n List of Security Groups")
print(aliyun_security_group_list)


result ={}

def extract_grouping_list(a):
	res = []
	for i in range(1,len(a)):
		firstIndex = a[i].find('\"')
		secondIndex = a[i].find('\"',firstIndex+1)
		t = a[i][firstIndex+1 : secondIndex]
		res.append(t)
		# print(res)

	return res

for a in range(len(aliyun_regions_holder)):
	result[aliyun_regions_holder[a]] = extract_grouping_list(aliyun_security_group_list[a])

print(result)

print("\n\n List of possible queries to run : \n")
for key in result:
    # print(key, '->', result[key])
    for b in result[key]:
        # print(key, '->', b)
        statment = "aliyun ecs DescribeSecurityGroupAttribute --Direction ingress  --RegionId "+key+" --SecurityGroupId "+b
        print(statment)
