import os
PREFIX = 'config_'
POSTFIX = '.txt'

for file in os.listdir('configs'):
    if not file.startswith(PREFIX) or not file.endswith(POSTFIX): continue
    config_name = file[len(PREFIX):-len(POSTFIX)]
    with open('inputdisplay_%s.bat' % config_name, 'w+') as f:
        f.write(r'bin\inputdisplay configs\config_%s.txt' % config_name)
        f.write('\npause')
