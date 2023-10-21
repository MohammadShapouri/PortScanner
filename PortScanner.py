import socket
import sys
import time
import re


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





def DigitExtractor(defaultValue, propertyName):
	result = defaultValue
	try:
		for i in range(2, len(sys.argv)):
			if "--"+propertyName in sys.argv[i]:
				position = sys.argv[i].find('=')
				result = sys.argv[i][(position+1):]
				if result.isdigit() == False:
					result = defaultValue
		return int(result)
	except Exception as e:
		sys.exit(f"Something went wrong in DigitExtractor function!: {e}")





def TimeoutExtractor():
	return DigitExtractor(2, "timeout")





def PortExtractor():
		return DigitExtractor(80, "port")





def IPAddrStructureVerifier(IPAddr):
	try:
		regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
		if re.match(regex, IPAddr) == None:
			return False
		else:
			return True
	except Exception as e:
		sys.exit(f"Something went wrong in IPAddrStructureVerifier function!: {e}")





def AvailibleServicesFileWriter(IPAddr, port):
	try:
		availibleServices = open('availibleServices'+str(port)+'.txt', 'a')
		availibleServices.write(str(IPAddr)+"\n")
		availibleServices.close()
	except Exception as e:
		print(f"Something went wrong in AvailibleServicesFileWriter function!: {e}")





def UnavailibleServicesFileWriter(IPAddr, port):
	try:
		# os.mknod('notAvailibleServices.txt')
		notAvailibleServices = open('UnavailibleServices'+str(port)+'.txt', 'a')
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





def PortAvailibilityChecker():
	port = PortExtractor()
	IPList = IPFileReader()
	headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

	IPListLength = len(IPList)
	IPsWithAvailibleSeviceCounter = 0
	IPsWithUnavailibleSeviceCounter = 0
	invalidIPCounter = 0

	print("Port: " + str(port) + "\n"
		"Timeout: " + str(TimeoutExtractor()) + " Seconds \n")

	for i in range(IPListLength):
		if IPAddrStructureVerifier(IPList[i]) == True:
			tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			tcp.settimeout(TimeoutExtractor())
			if tcp.connect_ex((IPList[i], port)) == 0:
				AvailibleServicesFileWriter(IPList[i], port)
				IPsWithAvailibleSeviceCounter += 1
				print(str((i*100)//IPListLength) + " % Done." + IPList[i] + " is availible.")
			else:
				UnavailibleServicesFileWriter(IPList[i], port)
				IPsWithUnavailibleSeviceCounter += 1
				print(str((i*100)//IPListLength) + " % Done." + IPList[i] + " is not availible.")
			tcp.close()
		else:
			IncorrectIPsFileWriter(IPList[i])
			invalidIPCounter += 1
			print(str((i*100)//IPListLength) + " % Done." + IPList[i] + " doesn't have the correct structure.")





PortAvailibilityChecker()