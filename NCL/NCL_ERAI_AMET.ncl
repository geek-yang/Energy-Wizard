;--- Open input file
dir = "/home/ESLT0068/WorkFlow/Core_Database_AMET_OMET_reanalysis/ERAI/point/"
filename = "model_daily_075_1980_E_point.nc"
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

; get certain variable
q = f->q
u = f->u

printVarSummary(q)
printMinMax(q,0)
print("dimensions of q = " + dimsizes(q))

