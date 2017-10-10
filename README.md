# Energy-Wizard
This is a toolkit specifically for working with atmospheric and oceanic reanalysis products. The aim is to quantify the meridional energy transport in the atmosphere (AMET) and ocean (OMET). This toolkit contains a list of codes to deal with the state of the art atmospheric & oceanic reanalysis dataset:
<br />
<br />
Atmosphere\
ERA-Interim   (ECMWF           EU)<br />
MERRA2        (NASA            US)<br />
JRA55         (JMA             JP)<br />
NCEP R2       (NCEP/NCAR       US)<br />

Ocean<br />
ORAS4         (ECMWF           EU)<br />
GLORYS2V4     (Mercator Ocean  Fr)<br />
SODA          (TAMU & UM       US)<br />

The codes can be categorized by functions:<br />
1. Data handling (incl. downloading from online database, preprocessing, etc.)<br />
2. Post-processing and analysis<br />

This tool is capable of batch work. It is written for super-computer and cloud.<br />

Structure of toolkit:<br />

/Dataset_Downloader<br />
Download and manage dataset from server.<br />

/Meridional_Energy_Transport<br />
Calculate Meridional Energy Transport from Atmospheric or Oceanic reanalysis data.<br />

/Postprocessing<br />
Postprocess the result (AMET & OMET) and analyze the result<br />

/Test<br />
Conceptual algorithm and functions to deal with certain problems.<br />

