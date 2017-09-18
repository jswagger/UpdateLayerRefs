# UpdateLayerRefs
Mass update layer references from one database to another in a given set of MXDs. This saves the hassle of manually going through each layer in each MXD and revising or fixing its path. Use the JSON file template to configure. Then run in Powershell or another command line.

To overwrite an existing MXD, rather than saving a new one, simply set the "out mxd" property to null.
Load up multiple MXDs to update in the "in mxds" parameter, separated by a comma.


## Instructions:

#### 1. Fill out JSON config file:


    in_mxds: load up the names of your input MXD's


    out_mxd: If you are fixing links, just leave the out_mxd list null, otherwise match the same order of the in_mxds for each name you want to save


    out_db: The full path to the SDE connection file.

       
    out_prefix: Includes database name and username used in SDE connection (Look at layer sources in an mxd referencing SDE for an example


#### 2. Run in powershell or command prompt: 

       python UpdateLayerRefs.py --config "update_layer_refs.config.json"



  ## Future improvements planned:

    Support multiple output connections
    
    Support FGDB to SDE

    Create an ArcToolbox with an easy-to-use tool within ArcMap
