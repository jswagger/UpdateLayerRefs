#
#
#
# Name: Update Layer References
#
# Purpose: Mass update layer references from one database to another. This saves the hassle of manually going through
# each layer and revising its path. Use a JSON file to configure to a new database, as well as save a new copy of your
# MXD.
#
# Author: jswagger
#
# Created: 07/31/2017
#
# Example config:
# {
#     "in_mxd": "C:\\Users\\jswagger\\Example.mxd",
#
#     "out_mxd": "C:\\Users\\jswagger\\ExampleUpdated.mxd",
#
#     "out_db": "C:\\SdeConnections\\gistest.sde",
#
#     "out_db_type": "SDE_WORKSPACE",
#
#     "in_prefix": "SANDBOX.GISTEST_CREATOR",
#
#     "out_prefix": "OUT_GISTEST.LSCGISTEST_CREATOR"
#
# }




import arcpy
import re
import json


def read_config_file():
    with open('update_layer_refs.config.json') as json_data:
        d = json.load(json_data)
        return d


def update_mxd(focus_mxd, out_mxd, out_db, out_db_type, in_prefix, out_prefix):
    for lyr in arcpy.mapping.ListLayers(focus_mxd):
        in_fc = lyr.datasetName
        out_fc_sanitized = re.sub(in_prefix, out_prefix, in_fc)
        lyr.replaceDataSource(out_db, out_db_type, out_fc_sanitized, False)
    if out_mxd:
        focus_mxd.saveACopy(out_mxd)
        print "New MXD is ready"
    else:
        focus_mxd.save()
        print "MXD ", focus_mxd.filePath, " has been updated"


def set_out_mxds(config_out_mxd):
    if config_out_mxd:
        config_out_mxd.encode('utf-8')
    return config_out_mxd


def process_in_mxds(in_mxds, workspace, out_mxd, out_db, out_db_type, in_prefix, out_prefix):
    for item in in_mxds:
        focus_mxd = arcpy.mapping.MapDocument((workspace + item).encode('utf-8'))
        update_mxd(focus_mxd, out_mxd, out_db, out_db_type, in_prefix, out_prefix)


def main():
    config_file = read_config_file()
    in_mxds = config_file.get("in_mxds")
    out_mxd = set_out_mxds(config_file.get("out_mxd"))
    out_db = config_file.get("out_db").encode('utf-8')
    out_db_type = config_file.get("out_db_type").encode('utf-8')
    in_prefix = config_file.get("in_prefix").encode('utf-8')
    out_prefix = config_file.get("out_prefix").encode('utf-8')
    workspace = config_file.get("workspace_folder")
    process_in_mxds(in_mxds, workspace, out_mxd, out_db, out_db_type, in_prefix, out_prefix)



main()
