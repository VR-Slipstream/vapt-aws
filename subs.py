import subprocess as sp

url = 'tidepool.org'

subdomains = sp.getoutput("subfinder -d " + url + " -silent")

print("DONE\nThese are the subdomains\n=========================")
print(subdomains)
print("=========================")
