#
#
#
#
#
#
#
#

import arcpy
import re

def update_mxd(in_mxd, out_mxd, out_db, out_db_type, in_prefix, out_prefix):
    for lyr in arcpy.mapping.ListLayers(in_mxd):
        in_fc = lyr.datasetName
        out_fc_sanitized = re.sub(in_prefix, out_prefix, in_fc)
        lyr.replaceDataSource(out_db, out_db_type, out_fc_sanitized, False)
    in_mxd.saveACopy(out_mxd)

def main():
    in_mxd = ""
    out_mxd = ""
    out_db = ""
    out_db_type = ""
    in_prefix = ""
    out_prefix = ""
    update_mxd(in_mxd, out_mxd, out_db, out_db_type, in_prefix, out_prefix)
    print "New MXD is ready"


main()
