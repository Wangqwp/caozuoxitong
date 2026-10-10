import subprocess, os
os.chdir(r'C:\Users\86138\Desktop\caozuoxitong')
local = subprocess.check_output(['git','rev-parse','main']).decode().strip()
remote = subprocess.check_output(['git','ls-remote','origin','main']).decode().strip().split('\t')[0]
print('local :', local)
print('remote:', remote)
print('match :', local == remote)
