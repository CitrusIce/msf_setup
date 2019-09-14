import subprocess, os, sys
cmd = "echo asdfasd".split()

p = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     shell=True)

for line in iter(p.stdout.readline, b''):
    print(line.decode('GBK'))