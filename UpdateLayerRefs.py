# Name: Update Layer References
#
# Mass update layer references from one database to another in a given set of MXDs. This saves the hassle of manually
# going through each layer in each MXD and revising or fixing its path. Use the JSON file template to configure.
# Then run in Powershell or another command line.
#
# Author: jswagger
#
# Created: 07/31/2017
#
# Example config:
# {
#     "workspace_folder": "C:\\Users\\jswagger\\",
#
#     "in_mxds": ["Example.mxd", "Example2.mxd", "Example3.mxd"],
#
#     "out_mxd": null,
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


def update_mxd(focus_mxd, out_mxd, out_db, out_db_type, out_prefix, mxd_order):
    for lyr in arcpy.mapping.ListLayers(focus_mxd):
        in_fc = lyr.datasetName
#
        in_prefix_processed = lyr.datasetName.replace(lyr.name, "")
        out_fc_sanitized = re.sub(in_prefix_processed, out_prefix, in_fc)
        lyr.replaceDataSource(out_db, out_db_type, out_fc_sanitized, False)
    if out_mxd:
        focus_mxd.saveACopy(out_mxd[mxd_order])
        print "MXD", focus_mxd.filePath, "saved as", out_mxd[mxd_order]
    else:
        focus_mxd.save()
        print "MXD ", focus_mxd.filePath, " has been updated"


def set_out_mxds(config_out_mxd):
    if config_out_mxd:
        processed_out_mxds = []
        for item in config_out_mxd:
            processed_out_mxds.append(item.encode('utf-8'))
    return processed_out_mxds


def process_in_mxds(in_mxds, workspace, out_mxd, out_db, out_db_type, out_prefix):
    for item in in_mxds:
        focus_mxd = arcpy.mapping.MapDocument((workspace + item).encode('utf-8'))
        mxd_order = in_mxds.index(item)
        update_mxd(focus_mxd, out_mxd, out_db, out_db_type, out_prefix, mxd_order)


def get_out_db_type(out_db):
    if out_db.endswith('.sde'):
        db_type = "SDE_WORKSPACE"
    if out_db.endswith('.gdb'):
        db_type = "FGDB_WORKSPACE"
    if db_type is None:
        print "Database type not supported"
    return db_type


def main():
    config_file = read_config_file()
    in_mxds = config_file.get("in_mxds")
    out_mxd = set_out_mxds(config_file.get("out_mxd"))
    out_db = config_file.get("out_db").encode('utf-8')
    out_db_type = get_out_db_type(out_db)
    out_prefix = config_file.get("out_prefix").encode('utf-8')
    workspace = config_file.get("workspace_folder")
    process_in_mxds(in_mxds, workspace, out_mxd, out_db, out_db_type, out_prefix)


main()
