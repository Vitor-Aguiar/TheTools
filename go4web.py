import requests
import os
import socket



host_files = 'hosts.txt'
rootdir = './recon/'
workdir = './recon/hosts/'
aquatone_work_dir = rootdir+'aquatone-output/'
aquatone_urls = aquatone_work_dir+'aquatone_urls.txt'
web_recon_work_dir = rootdir+'/Web-Recon-Directory-Discovery/'


common_wordlist = '/usr/share/dirb/wordlists/common.txt'
big_wordlist = '/usr/share/dirb/wordlists/big.txt'
medium_wordlist = '/Wordlists/dirbuster/wordlists/directory-list-2.3-medium.txt'


aquatone_path = "/aquatone/aquatone"

hosts_temp = open(host_files).readlines()


def validate_hosts(hosts_temp):
	hosts_real = []
	print('Validating hosts in file...')
	for host_temp in [i.strip() for i in hosts_temp]:
		try:
			if socket.getaddrinfo(host_temp,80):
				hosts_real.append(host_temp)
		except:
			print('['+host_temp+'] - Not a valid hostname or not resolvable.')
	print('[Done validating..]')
	print('#########################################')
	print('List of hosts available:')
	for host in hosts_real:
		print(host)
	return hosts_real

def create_dirs(hosts):
	print('Creating directory structure..')
	os.system('mkdir '+rootdir)
	os.system('mkdir '+workdir)
	os.system('mkdir '+web_recon_work_dir)
	os.system('mkdir '+aquatone_work_dir)
	for host in hosts:
		print('Creating \''+host+'\' folder.')
		os.system('mkdir '+workdir+host.strip())
		os.system('mkdir '+workdir+host.strip()+'/web')
		os.system('mkdir '+workdir+host.strip()+'/nmap')
	print('[Done creating directory structure]')


def gofindports(hosts):
	# Ports from Aquatone list
	small_ports = [80,443]
	medium_ports = [80,443,8000,8080,8443]
	large_ports = [80,81,443,591,2082,2087,2095,2096,3000,8000,8001,8008,8080,8083,8443,8834,8888]
	xlarge_ports = [80,81,300,443,591,593,832,981,1010,1311,2082,2087,2095,2096,2480,3000,3128,3333,4243,4567,4711,4712,4993,5000,5104,5108,5800,6543,7000,7396,7474,8000,8001,8008,8014,8042,8069,8080,8081,8088,8090,8091,8118,8123,8172,8222,8243,8280,8281,8333,8443,8500,8834,8880,8888,8983,9000,9043,9060,9080,9090,9091,9200,9443,9800,9981,12443,16080,18091,18092,20720,28017]
	print('Finding ports...')
	for host in hosts:
		nmap_command = 'nmap -Pn -p '+','.join([str(i) for i in xlarge_ports])+' -sV -sT --open -oA '+workdir+'/'+host+'/nmap/'+host+'-xlargeports '+host
		os.system(nmap_command)

	print('[Done finding ports]')


def goenumaquatone(hosts):
#	for host in hosts:
#		aquatone_command = "cat "+workdir+"/"+host+"/nmap/"+host+"-xlargeports.xml | "+aquatone_path+" -nmap"
	aquatone_command = "cat hosts.txt | "+aquatone_path+" -out "+aquatone_work_dir+" -ports xlarge"
	os.system(aquatone_command)
	os.system("cat "+aquatone_urls+" | sort -u >> hosts_urls.txt")

def urltofilename(url):

	url_file_name = url.replace('https://','').replace('http://','').replace('/','-')

	return url_file_name


def gofinddirsinitial(urls):


	for url in [i.strip() for i in urls]:

		#url = url123
		urloutfile = urltofilename(url)

		#nmap_file_xml = open(workdir+'/'+host+'/nmap/'+host+'-xlargeports '+host+'.xml').read()
		#print nmap_file

		gobuster_command_common = 'gobuster dir -e -x html,txt,php,asp,aspx -a "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" -w '+common_wordlist+' -o '+web_recon_work_dir+urloutfile+'-common.txt'+' -u '+url

		gobuster_command_big = 'gobuster dir -e -x html,txt,php,asp,aspx -a "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0" -w '+big_wordlist+' -o '+web_recon_work_dir+urloutfile+'-big.txt'+' -u '+url
		os.system(gobuster_command_common)
		os.system(gobuster_command_big)





##############################
print('#########################################')
hosts = validate_hosts(hosts_temp)
print('#########################################')
create_dirs(hosts)
print('#########################################')
gofindports(hosts)
print('#########################################')
goenumaquatone(hosts)
print('#########################################')

hosts2 = open('hosts_urls.txt').readlines()

print('URL Enum Done ++++++++++++++++++++++++++')
print('Printing URLs:')
print('---------------------------------------')
for host in hosts2:
	print(host)
print('---------------------------------------')
print('#########################################')
gofinddirsinitial(hosts2)
print('#########################################')
