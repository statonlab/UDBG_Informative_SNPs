def process_gt(str1):
	global total_depth
	global loci
	if str1 != '.':
		newstr = str1.split(":")[0]
		dp = str1.split(":")[1]
		if newstr == '0/0/0':
			newstr = "r"
		elif newstr == '0/0/1':
			newstr = "h"
		elif newstr == '0/1/1':
			newstr = "h"
		elif newstr == '1/1/1':
			newstr = "a"
		else:
			newstr = "0"
	else:
		newstr = '.'
		dp = 0
	#print("dp:"+str(dp))
	depth_fh.write(str(dp)+'\n')
	total_depth += int(dp)
	loci += 1
	return(newstr)

def compare_gt(str1, str2):
	if str1 != '.' and str2 != '.' and str1 != str2:
		return True
	else:
		return False

loci = 0
total_depth = 0
informative = 0
not_informative = 0
too_many_alleles = 0

loc2to3 = 0 #TG to TD
loc2to4 = 0 #TG to TE
loc2to5 = 0 #TG to MV
loc2to6 = 0 #TG to CH
loc2to7 = 0 #TG to TW

loc3to4 = 0 #TD to TE
loc3to5 = 0 #TD to MV
loc3to6 = 0 #TD to CH
loc3to7 = 0 #TD to TW

loc4to5 = 0 #TE to MV
loc4to6 = 0 #TE to CH
loc4to7 = 0 #TE to TW

loc5to6 = 0 #MV to CH
loc5to7 = 0 #MV to TW

loc6to7 = 0 #CH to TW

#with open('tmp', 'rU') as f:
#with open('15_3n_informativeSNPs.tsv', 'rU') as f:
depth_fh = open('depth.txt', 'w')

with open('15_3n_freebayes.vcf', 'rU') as f:
	for line in f:
		if not line.startswith('#'):
			list = line.split()
			tg2 = process_gt(list[9])
			td3 = process_gt(list[10])
			te4 = process_gt(list[11])
			mv5 = process_gt(list[12])
			ch6 = process_gt(list[13])
			tw7 = process_gt(list[14])

			## genotypes will come back
			## . for no call
			## r for homozygous ref
			## a for homozygous alt
			## h for het
			## 0 for more than two alleles (ie need to discard)
			#print(line)
			#print('TG: ' + tg2)
			#print('TD: ' + td3)
			#print('TE: ' + te4)
			#print('MV: ' + mv5)
			#print('CH: ' + ch6)
			#print('TW: ' + tw7)

			combined = tg2+td3+te4+mv5+ch6+tw7
			periods = combined.count('.')
			als = combined.count('a')
			rs = combined.count('r')
			hs = combined.count('h')
			zeros = combined.count('0')

			if zeros > 0:
				# we cant use this one
				too_many_alleles = too_many_alleles + 1
				#print('too many alleles')
			elif (als > 0 and rs > 0) or (rs > 0 and hs > 0) or (als > 0 and hs >0):
				informative = informative + 1
				print(line)
				print('TG: ' + tg2)
				print('TD: ' + td3)
				print('TE: ' + te4)
				print('MV: ' + mv5)
				print('CH: ' + ch6)
				print('TW: ' + tw7)
				print("informative")

				if compare_gt(tg2, td3):
					loc2to3 += 1
					print("informative TG2 to TD3")
				if compare_gt(tg2, te4):
					loc2to4 += 1
					print("informative TG2 to TE4")
				if compare_gt(tg2, mv5):
					loc2to5 += 1
					print("informative TG2 to MV5")
				if compare_gt(tg2, ch6):
					loc2to6 += 1
					print("informative TG2 to CH6")
				if compare_gt(tg2, tw7):
					loc2to7 += 1
					print("informative TG2 to TW7")

				if compare_gt(td3, te4):
					loc3to4 += 1
					print("informative TD3 to TE4")
				if compare_gt(td3, mv5):
					loc3to5 += 1
					print("informative TD3 to MV5")
				if compare_gt(td3, ch6):
					loc3to6 += 1
					print("informative TD3 to CH6")
				if compare_gt(td3, tw7):
					loc3to7 += 1
					print("informative TD3 to TW7")

				if compare_gt(te4, mv5):
					loc4to5 += 1
					print("informative TE4 to MV5")
				if compare_gt(te4, ch6):
					loc4to6 += 1
					print("informative TE4 to CH6")
				if compare_gt(te4, tw7):
					loc4to7 += 1
					print("informative TE4 to TW7")

				if compare_gt(mv5, ch6):
					loc5to6 += 1
					print("informative MV5 to CH6")
				if compare_gt(mv5, tw7):
					loc5to7 += 1
					print("informative MV5 to TW7")

				if compare_gt(ch6, tw7):
					loc6to7 += 1
					print("informative CH6 to TW7")

			else:
				not_informative = not_informative + 1
				#print("not informative")


			print('--')


print('too many alleles: ' + str(too_many_alleles))
print('not informative: ' + str(not_informative))
print('informative: ' + str(informative))

print("informative TG2 to TD3: " + str(loc2to3))
print("informative TG2 to TE4: " + str(loc2to4))
print("informative TG2 to MV5: " + str(loc2to5))
print("informative TG2 to CH6: " + str(loc2to6))
print("informative TG2 to TW7: " + str(loc2to7))

print("informative TD3 to TE4: " + str(loc3to4))
print("informative TD3 to MV5: " + str(loc3to5))
print("informative TD3 to CH6: " + str(loc3to6))
print("informative TD3 to TW7: " + str(loc3to7))

print("informative TE4 to MV5: " + str(loc4to5))
print("informative TE4 to CH6: " + str(loc4to6))
print("informative TE4 to TW7: " + str(loc4to7))

print("informative MV5 to CH6: " + str(loc5to6))
print("informative MV5 to TW7: " + str(loc5to7))

print("informative CH6 to TW7: " + str(loc6to7))

print("total depth: " + str(total_depth))
print("loci: " + str(loci))
print("average depth per locus per cultivar:" + str(total_depth/loci))
