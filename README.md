# UpdateLayerRefs
Mass update layer references from one database to another in a given MXD. This saves the hassle of manually going through each layer and revising its path. Use a JSON file to configure to a new database, as well as save a new copy of your MXD.

To overwrite an existing MXD, rather than saving a new one, simply set the "out mxd" property to null.

Future improvements planned:
Allow users to pass in multiple mxds as an tuple,
Support unknown input prefixes,
Create an ArcToolbox with an easy-to-use tool within ArcMap
