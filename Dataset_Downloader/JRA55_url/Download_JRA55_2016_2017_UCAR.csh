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
# Replace xxxxxx with your rda.ucar.edu password on the next uncommented line
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
  echo "You need to set your password before you can continue - see the documentation in the script"
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
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016010100_2016011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016010100_2016011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016010100_2016011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016010100_2016011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016010100_2016011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016011100_2016012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016011100_2016012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016011100_2016012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016011100_2016012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016011100_2016012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016012100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016012100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016012100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016012100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016012100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016020100_2016021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016020100_2016021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016020100_2016021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016020100_2016021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016020100_2016021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016021100_2016022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016021100_2016022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016021100_2016022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016021100_2016022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016021100_2016022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016022100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016022100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016022100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016022100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016022100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016030100_2016031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016030100_2016031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016030100_2016031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016030100_2016031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016030100_2016031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016031100_2016032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016031100_2016032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016031100_2016032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016031100_2016032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016031100_2016032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016032100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016032100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016032100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016032100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016032100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016040100_2016041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016040100_2016041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016040100_2016041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016040100_2016041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016040100_2016041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016041100_2016042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016041100_2016042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016041100_2016042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016041100_2016042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016041100_2016042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016042100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016042100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016042100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016042100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016042100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016050100_2016051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016050100_2016051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016050100_2016051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016050100_2016051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016050100_2016051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016051100_2016052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016051100_2016052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016051100_2016052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016051100_2016052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016051100_2016052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016052100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016052100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016052100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016052100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016052100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016060100_2016061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016060100_2016061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016060100_2016061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016060100_2016061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016060100_2016061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016061100_2016062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016061100_2016062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016061100_2016062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016061100_2016062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016061100_2016062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016062100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016062100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016062100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016062100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016062100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016070100_2016071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016070100_2016071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016070100_2016071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016070100_2016071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016070100_2016071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016071100_2016072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016071100_2016072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016071100_2016072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016071100_2016072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016071100_2016072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016072100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016072100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016072100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016072100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016072100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016080100_2016081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016080100_2016081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016080100_2016081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016080100_2016081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016080100_2016081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016081100_2016082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016081100_2016082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016081100_2016082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016081100_2016082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016081100_2016082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016082100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016082100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016082100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016082100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016082100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016090100_2016091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016090100_2016091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016090100_2016091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016090100_2016091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016090100_2016091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016091100_2016092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016091100_2016092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016091100_2016092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016091100_2016092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016091100_2016092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016092100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016092100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016092100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016092100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016092100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016100100_2016101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016100100_2016101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016100100_2016101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016100100_2016101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016100100_2016101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016101100_2016102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016101100_2016102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016101100_2016102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016101100_2016102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016101100_2016102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016102100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016102100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016102100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016102100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016102100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016110100_2016111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016110100_2016111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016110100_2016111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016110100_2016111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016110100_2016111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016111100_2016112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016111100_2016112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016111100_2016112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016111100_2016112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016111100_2016112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016112100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016112100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016112100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016112100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016112100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016120100_2016121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016120100_2016121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016120100_2016121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016120100_2016121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016120100_2016121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016121100_2016122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016121100_2016122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016121100_2016122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016121100_2016122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016121100_2016122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.007_hgt.reg_tl319.2016122100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.011_tmp.reg_tl319.2016122100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.033_ugrd.reg_tl319.2016122100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.034_vgrd.reg_tl319.2016122100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2016/anl_mdl.051_spfh.reg_tl319.2016122100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017010100_2017011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017010100_2017011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017010100_2017011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017010100_2017011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017010100_2017011018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017011100_2017012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017011100_2017012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017011100_2017012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017011100_2017012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017011100_2017012018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017012100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017012100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017012100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017012100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017012100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017020100_2017021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017020100_2017021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017020100_2017021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017020100_2017021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017020100_2017021018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017021100_2017022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017021100_2017022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017021100_2017022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017021100_2017022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017021100_2017022018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017022100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017022100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017022100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017022100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017022100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017030100_2017031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017030100_2017031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017030100_2017031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017030100_2017031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017030100_2017031018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017031100_2017032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017031100_2017032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017031100_2017032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017031100_2017032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017031100_2017032018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017032100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017032100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017032100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017032100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017032100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017040100_2017041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017040100_2017041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017040100_2017041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017040100_2017041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017040100_2017041018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017041100_2017042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017041100_2017042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017041100_2017042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017041100_2017042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017041100_2017042018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017042100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017042100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017042100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017042100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017042100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017050100_2017051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017050100_2017051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017050100_2017051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017050100_2017051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017050100_2017051018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017051100_2017052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017051100_2017052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017051100_2017052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017051100_2017052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017051100_2017052018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017052100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017052100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017052100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017052100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017052100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017060100_2017061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017060100_2017061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017060100_2017061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017060100_2017061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017060100_2017061018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017061100_2017062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017061100_2017062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017061100_2017062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017061100_2017062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017061100_2017062018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017062100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017062100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017062100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017062100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017062100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017070100_2017071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017070100_2017071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017070100_2017071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017070100_2017071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017070100_2017071018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017071100_2017072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017071100_2017072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017071100_2017072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017071100_2017072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017071100_2017072018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017072100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017072100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017072100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017072100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017072100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017080100_2017081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017080100_2017081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017080100_2017081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017080100_2017081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017080100_2017081018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017081100_2017082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017081100_2017082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017081100_2017082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017081100_2017082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017081100_2017082018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017082100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017082100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017082100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017082100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017082100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017090100_2017091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017090100_2017091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017090100_2017091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017090100_2017091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017090100_2017091018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017091100_2017092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017091100_2017092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017091100_2017092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017091100_2017092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017091100_2017092018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017092100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017092100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017092100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017092100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017092100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017100100_2017101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017100100_2017101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017100100_2017101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017100100_2017101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017100100_2017101018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017101100_2017102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017101100_2017102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017101100_2017102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017101100_2017102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017101100_2017102018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017102100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017102100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017102100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017102100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017102100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017110100_2017111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017110100_2017111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017110100_2017111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017110100_2017111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017110100_2017111018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017111100_2017112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017111100_2017112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017111100_2017112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017111100_2017112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017111100_2017112018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017112100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017112100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017112100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017112100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017112100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017120100_2017121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017120100_2017121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017120100_2017121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017120100_2017121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017120100_2017121018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017121100_2017122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017121100_2017122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017121100_2017122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017121100_2017122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017121100_2017122018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.007_hgt.reg_tl319.2017122100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.011_tmp.reg_tl319.2017122100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.033_ugrd.reg_tl319.2017122100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.034_vgrd.reg_tl319.2017122100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_mdl/2017/anl_mdl.051_spfh.reg_tl319.2017122100_2017123118
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
