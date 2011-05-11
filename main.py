import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(root_dir, 'lib')
sys.path.insert(0, lib_dir)

from portal.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
