;--- Open input file
;dir = "/home/ESLT0068/WorkFlow/Test/era1978_1980/era1979/"
dir = getenv("path")
filename = "model_daily_075_1979_1_u_v.nc"
; loda file
f = addfile(dir + filename,"r")
; get all dimensions names
dnames = getvardims(f)
; get dimension sizes
dsizes = getfiledimsizes(f)
; get variable names
vnames = getfilevarnames(f) 
print(dnames + " : " + dsizes)
print(str_join(vnames,",")) ; Print on one line with commas

g = 9.8071
; get certain variable
v = f->v(0,0,::-1,:)
u = f->u(0,0,::-1,:)
lat = f->latitude
lon = f->longitude

printVarSummary(v)
;printMinMax(v,0)
print("dimensions of v = " + dimsizes(v))

dv = uv2dvF(u,v) ; latitude must ascend
printVarSummary(dv)
print(dv(10:20,120:130))
print("xxxxxxxxxxxxxxxxxxxxxxx")
dvv = uv2dv_cfd(u,v,lat,lon,3)
printVarSummary(dvv)
print(dvv(10:20,120:130))
print("xxxxxxxxxxxxxxxxxxxxxxx")
X = ilapsF(dv,0)
printVarSummary(dv)
print(X(10:20,120:130))
print("xxxxxxxxxxxxxxxxxxxxxxx")
grad_uc = X
grad_vc = X
gradsf(X, grad_uc, grad_vc)
printVarSummary(grad_uc)
print(grad_uc(10:20,120:130))
print("xxxxxxxxxxxxxxxxxxxxxxx")
uc = grad_uc / g
printVarSummary(uc)
print(uc(10:20,120:130))
print("xxxxxxxxxxxxxxxxxxxxxxx")
vc = ilapsF(grad_vc,0); / g + uc
printVarSummary(vc)
print(vc(10:20,120:130))
; ##################################################################
; ############            create netCDF files           ############
; ##################################################################
nlat  = dimsizes(lat)
nlon  = dimsizes(lon)
diro = dir                      ; Output directory
filo = "temp_uvc.nc"             ; Output file
system("/bin/rm -f " + diro + filo)    ; remove if exists
fout  = addfile (diro + filo, "c")  ; open output file
;===================================================================
; explicitly declare file definition mode. Improve efficiency.
;===================================================================
setfileoption(fout,"DefineMode",True)
;===================================================================
; predefine the coordinate variables and their dimensionality
; Note: to get an UNLIMITED record dimension, we set the dimensionality
; to -1 (or the actual size) and set the dimension name to True.
;===================================================================
dimNames = (/"lat", "lon"/)
dimSizes = (/nlat,  nlon/)
dimUnlim = (/False, False/)
filedimdef(fout,dimNames,dimSizes,dimUnlim)
;===================================================================
; predefine the the dimensionality of the variables to be written out
;===================================================================
; Here we are using NCL functions to facilitate defining
; each variable's dimension name(s) and type.
; The following could be replaced with explicit, user defined dimension
; names different from those associated with the variable in memory.
; Say, PS(time,lat,lon) in the NCL script. They could be redefined for the file via:
; filevardef(fout, "PS"   ,typeof(PS) ,(/"TIME","latitude","longitude"/))
;===================================================================
filevardef(fout, "lat"  ,typeof(lat),(/"lat"/))
filevardef(fout, "lon"  ,typeof(lon),(/"lon"/))
filevardef(fout, "uc"   ,typeof(uc) ,(/"lat","lon"/))
filevardef(fout, "vc"   ,typeof(vc) ,(/"lat","lon"/))
;===================================================================
; Copy attributes associated with each variable to the file
; All attributes associated with each variable will be copied.
;====================================================================
;filevarattdef(fout,"uc",uc)     ; copy uc attributes
;filevarattdef(fout,"vc",vc)     ; copy vc attributes
;filevarattdef(fout,"lat",lat)   ; copy lat attributes
;filevarattdef(fout,"lon",lon)   ; copy lon attributes
;lat@long_name = "Latitude"
;lon@long_name = "Longitude"
;uc@long_name = "zonal correct barotropic wind"
;vc@long_name = "meridional correct barotropic wind"

;lat@unit = "degree north"
;lon@unit = "degree east"
;uc@unit = "m/s"
;vc@unit = "m/s"
;===================================================================
; explicitly exit file definition mode. **NOT REQUIRED**
;===================================================================
setfileoption(fout,"DefineMode",False)
;===================================================================
; output only the data values since the dimensionality and such have
; been predefined. The "(/", "/)" syntax tells NCL to only output the
; data values to the predefined locations on the file.
;====================================================================
fout->lat    = (/lat/)
fout->lon    = (/lon/)
fout->uc     = (/uc/)
fout->vc     = (/vc/)
print("create netcdf successfully!")
