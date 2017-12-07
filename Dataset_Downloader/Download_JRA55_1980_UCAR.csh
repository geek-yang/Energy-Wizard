#! /bin/csh -f
#
# c-shell script to download selected files from rda.ucar.edu using Wget
# NOTE: if you want to run under a different shell, make sure you change
#       the 'set' commands according to your shell's syntax
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
# Experienced Wget Users: add additional command-line flags here
#   Use the -r (--recursive) option with care
#   Do NOT use the -b (--background) option - simultaneous file downloads
#       can cause your data access to be blocked
set opts = "-N"
#
# Replace "xxxxxx" with your rda.ucar.edu password on the next uncommented line
# IMPORTANT NOTE:  If your password uses a special character that has special
#                  meaning to csh, you should escape it with a backslash
#                  Example:  set passwd = "my\!password"
set passwd = 'xxxxxx'
set num_chars = `echo "$passwd" |awk '{print length($0)}'`
if ($num_chars == 0) then
  echo "You need to set your password before you can continue"
  echo "  see the documentation in the script"
  exit
endif
@ num = 1
set newpass = ""
while ($num <= $num_chars)
  set c = `echo "$passwd" |cut -b{$num}-{$num}`
  if ("$c" == "&") then
    set c = "%26";
  else
    if ("$c" == "?") then
      set c = "%3F"
    else
      if ("$c" == "=") then
        set c = "%3D"
      endif
    endif
  endif
  set newpass = "$newpass$c"
  @ num ++
end
set passwd = "$newpass"
#
set cert_opt = ""
# If you get a certificate verification error (version 1.10 or higher),
# uncomment the following line:
#set cert_opt = "--no-check-certificate"
#
if ("$passwd" == "xxxxxx") then
  echo "You need to set your password before you can continue"
  echo "  see the documentation in the script"
  exit
endif
#
# authenticate - NOTE: You should only execute this command ONE TIME.
# Executing this command for every data file you download may cause
# your download privileges to be suspended.
wget $cert_opt -O auth_status.rda.ucar.edu --save-cookies auth.rda.ucar.edu.$$ --post-data="email=y.liu@esciencecenter.nl&passwd=$passwd&action=login" https://rda.ucar.edu/cgi-bin/login
#
# download the file(s)
# NOTE:  if you get 403 Forbidden errors when downloading the data files, check
#        the contents of the file 'auth_status.rda.ucar.edu'
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980010100_1980011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980010100_1980011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980010100_1980011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980010100_1980011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980010100_1980011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980011100_1980012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980011100_1980012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980011100_1980012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980011100_1980012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980011100_1980012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980012100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980012100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980012100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980012100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980012100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980020100_1980021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980020100_1980021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980020100_1980021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980020100_1980021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980020100_1980021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980021100_1980022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980021100_1980022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980021100_1980022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980021100_1980022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980021100_1980022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980022100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980022100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980022100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980022100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980022100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980030100_1980031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980030100_1980031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980030100_1980031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980030100_1980031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980030100_1980031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980031100_1980032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980031100_1980032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980031100_1980032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980031100_1980032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980031100_1980032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980032100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980032100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980032100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980032100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980032100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980040100_1980041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980040100_1980041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980040100_1980041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980040100_1980041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980040100_1980041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980041100_1980042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980041100_1980042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980041100_1980042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980041100_1980042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980041100_1980042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980042100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980042100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980042100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980042100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980042100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980050100_1980051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980050100_1980051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980050100_1980051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980050100_1980051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980050100_1980051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980051100_1980052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980051100_1980052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980051100_1980052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980051100_1980052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980051100_1980052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980052100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980052100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980052100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980052100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980052100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980060100_1980061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980060100_1980061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980060100_1980061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980060100_1980061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980060100_1980061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980061100_1980062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980061100_1980062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980061100_1980062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980061100_1980062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980061100_1980062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980062100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980062100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980062100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980062100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980062100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980070100_1980071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980070100_1980071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980070100_1980071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980070100_1980071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980070100_1980071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980071100_1980072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980071100_1980072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980071100_1980072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980071100_1980072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980071100_1980072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980072100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980072100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980072100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980072100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980072100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980080100_1980081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980080100_1980081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980080100_1980081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980080100_1980081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980080100_1980081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980081100_1980082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980081100_1980082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980081100_1980082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980081100_1980082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980081100_1980082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980082100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980082100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980082100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980082100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980082100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980090100_1980091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980090100_1980091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980090100_1980091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980090100_1980091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980090100_1980091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980091100_1980092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980091100_1980092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980091100_1980092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980091100_1980092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980091100_1980092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980092100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980092100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980092100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980092100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980092100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980100100_1980101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980100100_1980101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980100100_1980101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980100100_1980101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980100100_1980101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980101100_1980102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980101100_1980102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980101100_1980102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980101100_1980102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980101100_1980102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980102100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980102100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980102100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980102100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980102100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980110100_1980111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980110100_1980111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980110100_1980111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980110100_1980111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980110100_1980111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980111100_1980112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980111100_1980112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980111100_1980112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980111100_1980112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980111100_1980112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980112100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980112100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980112100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980112100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980112100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980120100_1980121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980120100_1980121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980120100_1980121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980120100_1980121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980120100_1980121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980121100_1980122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980121100_1980122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980121100_1980122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980121100_1980122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980121100_1980122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.007_hgt.reg_tl319.1980122100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.011_tmp.reg_tl319.1980122100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.033_ugrd.reg_tl319.1980122100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.034_vgrd.reg_tl319.1980122100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/1980/anl_mdl.051_spfh.reg_tl319.1980122100_1980123118
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
