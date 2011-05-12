import sys
import os
from optparse import OptionParser

root_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(root_dir, 'lib')
sys.path.insert(0, lib_dir)

from portal.app import create_app

if __name__ == '__main__':
    app = create_app()
    parser = OptionParser()
    parser.add_option("-d", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="activate the flask debugger")
    (options, args) = parser.parse_args()
    app.debug = options.debug
    app.run()
