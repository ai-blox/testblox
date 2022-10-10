import subprocess

df = subprocess.check_output("lsusb")
print df
