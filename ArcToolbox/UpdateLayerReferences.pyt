import arcpy
import re


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [UpdateLayerRefs]


class UpdateLayerRefs(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Update Layer References"
        self.description = "Mass update layer references from one database to another in multiple mxds."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_mxds = arcpy.Parameter(
            displayName="in_mxds",
            name="in_mxds",
            datatype="DEFile",
            parameterType="Required",
            direction="Input",
            multiValue=True
        )
        out_mxds = arcpy.Parameter(
            displayName="out_mxds",
            name="out_mxds",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=False
        )
        out_db = arcpy.Parameter(
            displayName="out_db",
            name="out_db",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        out_prefix = arcpy.Parameter(
            displayName="out_prefix",
            name="out_prefix",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        workspace = arcpy.Parameter(
            displayName="workspace",
            name="workspace",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        params = [in_mxds, out_mxds, out_db, out_prefix, workspace]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):

        def update_mxd(focus_mxd, out_mxd, out_db, out_db_type, out_prefix, mxd_order):
            for lyr in arcpy.mapping.ListLayers(focus_mxd):
                in_fc = lyr.datasetName
                in_prefix_processed = lyr.datasetName.rsplit('.', 1)[0] + '.'
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
                arcpy.AddMessage("Made it to item")
                arcpy.AddMessage(item)
                focus_mxd = arcpy.mapping.MapDocument(item)
                mxd_order = in_mxds.index(item)
                update_mxd(focus_mxd, out_mxd, out_db, out_db_type, out_prefix, mxd_order)

        def main():
            in_mxds = parameters[0]
            out_mxd = set_out_mxds(parameters[1].valueAsText)
            out_db = parameters[2].valueAsText.encode('utf-8')
            out_db_type = get_out_db_type(parameters[2].valueAsText)
            out_prefix = parameters[3].valueAsText.encode('utf-8')
            workspace = parameters[4].valueAsText
            process_in_mxds(in_mxds, workspace, out_mxd, out_db, out_db_type, out_prefix)


        main()

def get_out_db_type(out_db):
    if out_db.endswith('.sde'):
        return "SDE_WORKSPACE"
    if out_db.endswith('.gdb'):
        return "FILEGDB_WORKSPACE"
    else:
        print "Database type not supported"


        def get_out_db_type(out_db):
            if out_db.endswith('.sde'):
                return "SDE_WORKSPACE"
            if out_db.endswith('.gdb'):
                return "FILEGDB_WORKSPACE"
            else:
                print "Database type not supported"




        return
