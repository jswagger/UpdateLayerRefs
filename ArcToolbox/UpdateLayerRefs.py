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
#     "out_mxds": null,
#
#     "out_db": "C:\\SdeConnections\\gistest.sde",
#
#     "out_prefix": "OUT_GISTEST.GISTEST_CREATOR."
# }


import arcpy
import re


def update_mxd(focus_mxd, out_suffix, out_db, out_db_type, out_prefix):
    for lyr in arcpy.mapping.ListLayers(focus_mxd):
        in_fc = lyr.datasetName
        in_prefix_processed = lyr.datasetName.rsplit('.', 1)[0] + '.'
        out_fc_sanitized = re.sub(in_prefix_processed, out_prefix, in_fc)
        lyr.replaceDataSource(out_db, out_db_type, out_fc_sanitized, False)
    if out_suffix:
        focus_mxd.saveACopy(focus_mxd.title + out_suffix)
        print "MXD", focus_mxd.filePath, "saved as", out_suffix
    else:
        focus_mxd.save()
        print "MXD ", focus_mxd.filePath, " has been updated"


def process_in_mxds(in_mxds, workspace, out_mxd, out_db, out_db_type, out_prefix):
    for item in in_mxds:
        focus_mxd = arcpy.mapping.MapDocument((workspace + item).encode('utf-8'))
        update_mxd(focus_mxd, out_mxd, out_db, out_db_type, out_prefix)


def get_out_db_type(out_db):
    if out_db.endswith('.sde'):
        return "SDE_WORKSPACE"
    if out_db.endswith('.gdb'):
        return "FILEGDB_WORKSPACE"
    else:
        print "Database type not supported"


def main():
    in_mxds = arcpy.GetParameterAsText(0)
    out_suffix = arcpy.GetParameterAsText(1)
    out_db = arcpy.GetParameterAsText(2).encode('utf-8')
    out_db_type = get_out_db_type(out_db)
    out_prefix = arcpy.GetParameterAsText(3).encode('utf-8')
    workspace = arcpy.GetParameterAsText(4)
    process_in_mxds(in_mxds, workspace, out_suffix, out_db, out_db_type, out_prefix)


main()
