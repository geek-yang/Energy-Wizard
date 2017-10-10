# Energy-Wizard
This is a toolkit specifically for working with atmospheric and oceanic reanalysis products. The aim is to quantify the meridional energy transport in the atmosphere (AMET) and ocean (OMET). This toolkit contains a list of codes to deal with the state of the art atmospheric & oceanic reanalysis dataset:

Atmosphere
ERA-Interim   (ECMWF           EU)
MERRA2        (NASA            US)
JRA55         (JMA             JP)
NCEPR2        (NCEP/NCAR       US)

Ocean
ORAS4         (ECMWF           EU)
GLORYS2V4     (Mercator Ocean  Fr)
SODA          (TAMU & UM       US)

The codes can be categorized by functions:
1. Data handling (incl. downloading from online database, preprocessing, etc.)
2. Post-processing and analysis

This tool is capable of batch work. It is written for super-computer and cloud.

Structure of toolkit:
/Downloader
Download and manage dataset from server.
/
