import socket
import sys
import re
import concurrent.futures


def IPFileReader():
	try:
		reader = open(sys.argv[1])
		IPList = reader.readlines()
		reader.close()
		IPList = list(map(str.strip, IPList))
		IPList = [eachIPAddr for eachIPAddr in IPList if eachIPAddr != ""]
		return IPList
	except FileNotFoundError:
		sys.exit("No valid IP list file found.")
	except Exception as e:
		sys.exit(f"Something went wrong in IPFileReader function!: {e}")





def IPListSplitter(IPList, partNumber):
	splittedIPListLists = list()
	listLength = len(IPList)
	partSize = listLength // partNumber

	for part in range(1, partNumber+1):
		if part != (partNumber):
			trimmedList = IPList[(partSize*part)-partSize:(partSize*part)]
		else:
			trimmedList = IPList[(partSize*part)-partSize:]
		splittedIPListLists.append(trimmedList)
	return splittedIPListLists





def DigitExtractor(defaultValue, propertyName):
	result = defaultValue
	if result.isdigit() == False:
		sys.exit('defaultValue must be integer.')

	try:
		for i in range(2, len(sys.argv)):
			if "--"+propertyName in sys.argv[i]:
				position = sys.argv[i].find('=')
				result = sys.argv[i][(position+1):]
				if result.isdigit() == False:
					result = defaultValue
				return int(result)
		return int(defaultValue)
	except Exception as e:
		sys.exit(f"Something went wrong in DigitExtractor function!: {e}")





def TimeoutExtractor():
	return DigitExtractor(2, "timeout")





def PortExtractor():
		return DigitExtractor(80, "port")





def ThreadCountExtractor():
	return DigitExtractor(1, "threadCount")





def IPAddrStructureVerifier(IPAddr):
	try:
		regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
		if re.match(regex, IPAddr) == None:
			return False
		else:
			return True
	except Exception as e:
		sys.exit(f"Something went wrong in IPAddrStructureVerifier function!: {e}")





def AvailiblePortFileWriter(IPAddr, port):
	try:
		availibleServices = open('availibleServices -- port '+str(port)+'.txt', 'a')
		availibleServices.write(str(IPAddr)+"\n")
		availibleServices.close()
	except Exception as e:
		print(f"Something went wrong in AvailiblePortFileWriter function!: {e}")





def UnavailiblePortFileWriter(IPAddr, port):
	try:
		# os.mknod('notAvailibleServices.txt')
		notAvailibleServices = open('UnavailibleServices -- port '+str(port)+'.txt', 'a')
		notAvailibleServices.write(str(IPAddr)+"\n")
		notAvailibleServices.close()
	except Exception as e:
		print(f"Something went wrong in AvailibleServicesFile fWriterunction!: {e}")





def IncorrectIPsFileWriter(IPAddr):
	try:
		# os.mknod('UnestablishableIPs.txt')
		UnestablishableIPs = open('IncorrectIPs.txt', 'a')
		UnestablishableIPs.write(str(IPAddr)+"\n")
		UnestablishableIPs.close()
	except Exception as e:
		print(f"Something went wrong in IncorrectIPsFileWriter function!: {e}")





def PortAvailibilityChecker(IPList, port, timeout):

	IPListLength = len(IPList)

	for i in range(IPListLength):
		if IPAddrStructureVerifier(IPList[i]) == True:
			tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			tcp.settimeout(timeout)
			if tcp.connect_ex((IPList[i], port)) == 0:
				AvailiblePortFileWriter(IPList[i], port)
				print(IPList[i] + " is availible.")
			else:
				UnavailiblePortFileWriter(IPList[i], port)
				print(IPList[i] + " is not availible.")
			tcp.close()
		else:
			IncorrectIPsFileWriter(IPList[i])
			print(IPList[i] + " doesn't have the correct structure.")





def main():
	port = PortExtractor()
	timeout = TimeoutExtractor()
	IPList = IPFileReader()
	threadCount = ThreadCountExtractor()
	splittedIPListLists = IPListSplitter(IPList, threadCount) # A list which contains splitted lists of IP Addres.


	print("Timeout: " + str(timeout) + ".")
	print("Port: " + str(port) + ".")
	print("Thread Count: " + str(threadCount) + ".")


	pool = concurrent.futures.ThreadPoolExecutor(max_workers=threadCount)
	for i in range(threadCount):
		pool.submit(PortAvailibilityChecker, splittedIPListLists[i], port, timeout)
	pool.shutdown(wait=True)
	print("Scanning Done!")




main()
