import os
from os.path import exists
from mxdextract import *
import shutil

def main():
    mxd_dir = r'D:\gis\MXDfolder'

    extens = ['shp','shx','dbf','prj','xml','sbn','sbx','cpg']
    mxdf = scanfiles(mxd_dir, 'MXD')
    outd = os.path.join(mxd_dir, 'shapefiles')
    os.mkdir(outd)
    for mxd in mxdf:
        bn = os.path.basename(mxd).split('.')[0]
        projdir = os.path.join(mxd_dir, outd, bn)
        os.mkdir(projdir)
        shapes = scanmxd(mxd)
        for shp in shapes:
            if shp[1] == True:
                dn = os.path.dirname(shp[2])
                bn = os.path.basename(shp[2]).split('.')[0]
                for ext in extens:
                    sf = os.path.join(dn, bn + '.' + ext)
                    outf = os.path.join(projdir, bn + '.' + ext)
                    fe = exists(sf)
                    if fe:
                        print(bn + '.' + ext)
                        shutil.copyfile(sf, outf)


def scanfiles(folder, extension):
    files = []
    filesout = []
    for (dirpath, dirnames, filenames) in os.walk(folder):
        files.extend(filenames)
        break
    for each in files:
        basename = os.path.basename(each)
        sp = basename.split('.')
        if sp[1].upper() == extension.upper() and len(sp) == 2:
            cp = os.path.join(folder, each)
            filesout.append(cp)
    return filesout


if __name__ == "__main__":
    main()
