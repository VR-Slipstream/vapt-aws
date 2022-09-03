import subprocess as sp
import argparse

parser = argparse.ArgumentParser(description="This is VAPT Project")
parser.add_argument("-d" , type= str,help="Type Domain" , required  = True)
p = parser.parse_args()
subdomains = p.getoutput("subfinder -silent -d "+ p.d)

print(subdomains)

def s3_file():
	f = open("subdomains.txt", "w")
	f.write(subdomains)

print("DONE\nThese are the subdomains\n=========================")

print("=========================")
