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
import json


def read_config_file():
    with open('update_layer_refs.config.json') as json_data:
        d = json.load(json_data)
        return d


def update_mxd(in_mxd, out_mxd, out_db, out_db_type, in_prefix, out_prefix):
    for lyr in arcpy.mapping.ListLayers(in_mxd):
        in_fc = lyr.datasetName
        out_fc_sanitized = re.sub(in_prefix, out_prefix, in_fc)
        lyr.replaceDataSource(out_db, out_db_type, out_fc_sanitized, False)
    in_mxd.saveACopy(out_mxd)


def main():
    config_file = read_config_file()
    in_mxd = arcpy.mapping.MapDocument(config_file.get("in_mxd").encode('utf-8'))
    out_mxd = config_file.get("out_mxd").encode('utf-8')
    out_db = config_file.get("out_db").encode('utf-8')
    out_db_type = config_file.get("out_db_type").encode('utf-8')
    in_prefix = config_file.get("in_prefix").encode('utf-8')
    out_prefix = config_file.get("out_prefix").encode('utf-8')
    update_mxd(in_mxd, out_mxd, out_db, out_db_type, in_prefix, out_prefix)
    print "New MXD is ready"


main()
