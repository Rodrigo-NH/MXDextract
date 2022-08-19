import binascii, os

# Using arcpy
# https://gis.stackexchange.com/questions/30630/crawling-directory-and-listing-all-datasources-using-arcpy
# C:\Program Files (x86)\ArcGIS\Desktop10.5\arcpy\arcpy

def main():
    mxd = r'D:\somemxd.mxd'
    shapes = scanmxd(mxd)
    for shape in shapes:
        print(shape)


def scanmxd(mxd):
    file = open(mxd, "rb")
    table = []
    byte = file.read(1)
    while byte:
        hx = str(binascii.hexlify(byte).upper()).split("'")[1]
        table.append(hx)
        byte = file.read(1)

    mainidx = []
    indexm = '8AD011BEC700805F7C4268'
    pp = 0
    startb = 0
    while pp is not None:
        pp = crawler(table,11,indexm,startb)
        if pp is not None:
            mainidx.append(pp)
            startb = pp+11

    chkduplicates = []
    filelist = []
    for id in mainidx:
        pointer = id + 21
        ee = extractp(table, pointer)
        fo = bytes.fromhex(ee[0]).decode('cp1252')  # layer name
        pointer = ee[1] + 54
        ls = table[pointer:pointer+2]
        la = [ls[0]+ls[1]][0]  # layer is active
        if la == '0000':
            la = False
        elif la == 'FFFF':
            la = True
        else:
            la = None
        nm = '1942CAD111AA7C00'
        pointer = crawler(table, 8, nm, pointer)
        if pointer is not None and la is not None:
            pointer = pointer + 23
            sn = extractp(table, pointer)
            sn = bytes.fromhex(sn[0]).decode('cp1252')  # shape name
            pointer = pointer+len(sn)*2
            nm = '355A71E3D111AA'  # validity check (directory marker)
            pointeri = pointer
            pointer = crawler(table, 7, nm, pointer)
            pointerf = pointer
            pointer += 24
            fn = extractp(table, pointer)
            fn = bytes.fromhex(fn[0]).decode('cp1252')
            if pointerf-pointeri == 88:
                tc = fo+sn+fn
                if tc not in chkduplicates:
                    chkduplicates.append(tc)
                    filelist.append([fo,la,os.path.join(fn, sn + '.shp')])
    return filelist


def extractp(table, pointer):
    bc = ''
    val = ''
    while bc != '0000':
        cb = table[pointer:pointer + 1][0]
        tc = table[pointer:pointer + 2]
        bc = tc[0] + tc[1]
        if cb != '00':
            val = val + cb
        pointer += 1
    return [ val, pointer ]


def crawler(table, blocksize, marker, start):
    pointer = start
    strip = ''
    re = None
    while re != '':
        ln = table[pointer:pointer+blocksize]
        pointer += 1
        re = strip.join(ln)
        if re == marker:
            return pointer-1


if __name__ == "__main__":
    main()