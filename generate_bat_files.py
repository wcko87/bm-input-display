import os
PREFIX = 'profile_'
POSTFIX = '.txt'

for file in os.listdir('profiles'):
    if not file.startswith(PREFIX) or not file.endswith(POSTFIX): continue
    config_name = file[len(PREFIX):-len(POSTFIX)]
    with open('inputdisplay_%s.bat' % config_name, 'w+') as f:
        f.write(r'bin\inputdisplay profiles\%s%s%s' % (PREFIX, config_name, POSTFIX))
        f.write('\npause')
