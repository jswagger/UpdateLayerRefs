# UpdateLayerRefs
Mass update layer references from one database to another in a given set of MXDs. This saves the hassle of manually going through each layer in each MXD and revising or fixing its path. Use the JSON file template to configure. Then run in Powershell or another command line.

To overwrite an existing MXD, rather than saving a new one, simply set the "out mxd" property to null.
Load up multiple MXDs to update in the "in mxds" parameter, separated by a comma.

Future improvements planned:

Support unknown input prefixes

Support file geodatabase connections

Support multiple output connections

Create an ArcToolbox with an easy-to-use tool within ArcMap
