import glob
import os

pkg_version = os.environ['PKG_VERSION']

win_template = """
@echo off
python {pyfile} %*
"""

if os.name == 'nt':
    prefix = os.environ['LIBRARY_PREFIX']
    for f in glob.glob(os.path.join(prefix, 'lib', 'emscripten-' + pkg_version, '*.py')):
        # get binary
        bin_name = f[:-3] + '.bat'  # cut .py
        print("Linking up ", bin_name)
        if os.path.exists(bin_name):
            fname = os.path.basename(bin_name)
            dest_file = os.path.join(prefix, 'bin', fname)
            with open(dest_file, 'w') as fo:
                fo.write(win_template.format(pyfile=f))
else:
    prefix = os.environ['PREFIX']
    for f in glob.glob(os.path.join(prefix, 'lib', 'emscripten-' + pkg_version, '*.py')):
        # get binary
        bin_name = f[:-3]  # cut .py
        print("Linking up ", bin_name)
        fname = os.path.basename(bin_name)
        dest_file = os.path.join(prefix, 'bin', fname)
        if os.path.exists(bin_name) and not os.path.exists(dest_file):
            os.symlink(f, dest_file)
        
        # fix FileNotFoundError: [Errno 2] No such file or directory: 'lib/emscripten-4.0.*/emar'
        if not os.path.exists(bin_name):
            os.symlink(f, bin_name)
