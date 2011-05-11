# coding:utf-8
'''
This script generate the settings.py file
'''
import random
import string
letters_and_digits = string.letters + string.digits

from time import time
random.seed(time())

secret_key = "".join([random.choice(letters_and_digits) for x in xrange(32)])
csrf_key = "".join([random.choice(letters_and_digits) for x in xrange(32)])

lines = []
lines.append('# This file is auto-generated! Do not edit or check into git.\n')
lines.append('DEBUG=True\n')
lines.append('SECRET_KEY="%s"\n' % secret_key)
lines.append('CSRF_ENABLED=True\n')
lines.append('CSRF_SESSION_KEY="%s"' % csrf_key)

import os

my_dir = os.path.dirname(os.path.abspath(__file__))
settings_file = open(os.path.join(my_dir, 'portal', 'settings.py'), 'w')
settings_file.writelines(lines)
settings_file.close()
