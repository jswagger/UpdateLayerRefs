# UpdateLayerRefs
Mass update layer references from one database to another in a given set of MXDs. This saves the hassle of manually going through each layer in each MXD and revising or fixing its path. Use the JSON file template to configure. Then run in Powershell or another command line.

To overwrite an existing MXD, rather than saving a new one, simply set the "out mxd" property to null.
Load up multiple MXDs to update in the "in mxds" parameter, separated by a comma.


Instructions:

1. Fill out JSON config file:


in_mxds: load up the names of your input MXD's


out_mxd: If you are fixing links, just leave the out_mxd list null, otherwise match the same order of the in_mxds for each name you want to save


out_db: The full path to the SDE connection file.


out_db_type: Just "SDE_WORKSPACE" for now. File geodatabase will be supported soon.


in_prefix: This is the prefix containing the connection name preceding the actual feature class name. (i.e. feature class "Road" would be (SDE Connection).Road  Note: This will be phased out on the next build.


out_prefix: Same type as in_prefix, but will be the new target out database connection



2. Run in powershell or command prompt: 

python UpdateLayerRefs.py --config "update_layer_refs.config.json"



  Future improvements planned:

    Support unknown input prefixes

    Support file geodatabase connections

    Support multiple output connections

    Create an ArcToolbox with an easy-to-use tool within ArcMap
