from subprocess import call

print('Making client executable.')
result = call('chmod +x Client/lumaclient.py')
print('Result: '+str(result))
print('Making server executable.')
result = call('chmod +x Server/lumaserver.py')
print('Result: '+str(result))