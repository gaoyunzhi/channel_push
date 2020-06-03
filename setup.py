import os
import sys

def kill():
	os.system("ps aux | grep ython | grep mp3_trim | awk '{print $2}' | xargs kill -9")

def setup():
	kill()
	if 'kill' in str(sys.argv):
		return 
	addtional_arg = ' '.join(sys.argv[1:])
	command = 'python3 -u mp3_trim.py %s' % addtional_arg
	if 'debug' in addtional_arg or 'skip' in addtional_arg or 'once' in addtional_arg:
		os.system(command + ' test')
	else:
		os.system('nohup %s &' % command)
		if 'notail' not in addtional_arg:
			os.system('touch nohup.out && tail -F nohup.out')

if __name__ == '__main__':
	setup()