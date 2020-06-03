import os
import sys

def kill():
	os.system("ps aux | grep ython | grep channel_push | awk '{print $2}' | xargs kill -9")

def setup():
	kill()
	if 'kill' in str(sys.argv):
		return 
	addtional_arg = ' '.join(sys.argv[1:])
	command = 'python3 -u channel_push.py %s' % addtional_arg
	if 'debug' in addtional_arg or 'skip' in addtional_arg or 'once' in addtional_arg:
		os.system(command + ' test')
	else:
		os.system('nohup %s &' % command)
		if 'notail' not in addtional_arg:
			os.system('touch nohup.out && tail -F nohup.out')

if __name__ == '__main__':
	setup()