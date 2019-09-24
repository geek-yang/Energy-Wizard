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
set passwd = 'Bach1685'
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
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995090100_1995093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995090100_1995093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995090100_1995093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995090100_1995093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995090100_1995093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995100100_1995103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995100100_1995103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995100100_1995103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995100100_1995103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995100100_1995103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995110100_1995113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995110100_1995113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995110100_1995113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995110100_1995113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995110100_1995113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995120100_1995123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995120100_1995123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995120100_1995123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995120100_1995123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995120100_1995123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996010100_1996013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996010100_1996013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996010100_1996013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996010100_1996013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996010100_1996013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996020100_1996022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996020100_1996022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996020100_1996022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996020100_1996022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996020100_1996022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996030100_1996033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996030100_1996033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996030100_1996033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996030100_1996033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996030100_1996033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996040100_1996043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996040100_1996043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996040100_1996043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996040100_1996043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996040100_1996043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996050100_1996053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996050100_1996053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996050100_1996053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996050100_1996053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996050100_1996053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996060100_1996063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996060100_1996063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996060100_1996063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996060100_1996063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996060100_1996063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996070100_1996073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996070100_1996073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996070100_1996073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996070100_1996073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996070100_1996073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996080100_1996083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996080100_1996083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996080100_1996083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996080100_1996083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996080100_1996083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996090100_1996093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996090100_1996093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996090100_1996093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996090100_1996093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996090100_1996093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996100100_1996103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996100100_1996103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996100100_1996103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996100100_1996103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996100100_1996103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996110100_1996113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996110100_1996113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996110100_1996113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996110100_1996113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996110100_1996113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.007_hgt.1996120100_1996123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.011_tmp.1996120100_1996123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.033_ugrd.1996120100_1996123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.034_vgrd.1996120100_1996123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1996/anl_p125.051_spfh.1996120100_1996123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997010100_1997013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997010100_1997013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997010100_1997013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997010100_1997013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997010100_1997013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997020100_1997022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997020100_1997022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997020100_1997022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997020100_1997022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997020100_1997022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997030100_1997033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997030100_1997033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997030100_1997033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997030100_1997033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997030100_1997033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997040100_1997043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997040100_1997043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997040100_1997043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997040100_1997043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997040100_1997043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997050100_1997053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997050100_1997053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997050100_1997053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997050100_1997053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997050100_1997053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997060100_1997063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997060100_1997063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997060100_1997063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997060100_1997063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997060100_1997063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997070100_1997073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997070100_1997073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997070100_1997073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997070100_1997073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997070100_1997073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997080100_1997083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997080100_1997083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997080100_1997083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997080100_1997083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997080100_1997083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997090100_1997093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997090100_1997093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997090100_1997093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997090100_1997093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997090100_1997093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997100100_1997103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997100100_1997103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997100100_1997103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997100100_1997103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997100100_1997103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997110100_1997113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997110100_1997113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997110100_1997113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997110100_1997113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997110100_1997113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.007_hgt.1997120100_1997123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.011_tmp.1997120100_1997123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.033_ugrd.1997120100_1997123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.034_vgrd.1997120100_1997123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1997/anl_p125.051_spfh.1997120100_1997123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998010100_1998013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998010100_1998013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998010100_1998013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998010100_1998013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998010100_1998013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998020100_1998022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998020100_1998022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998020100_1998022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998020100_1998022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998020100_1998022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998030100_1998033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998030100_1998033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998030100_1998033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998030100_1998033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998030100_1998033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998040100_1998043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998040100_1998043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998040100_1998043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998040100_1998043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998040100_1998043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998050100_1998053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998050100_1998053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998050100_1998053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998050100_1998053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998050100_1998053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998060100_1998063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998060100_1998063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998060100_1998063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998060100_1998063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998060100_1998063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998070100_1998073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998070100_1998073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998070100_1998073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998070100_1998073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998070100_1998073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998080100_1998083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998080100_1998083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998080100_1998083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998080100_1998083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998080100_1998083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998090100_1998093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998090100_1998093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998090100_1998093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998090100_1998093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998090100_1998093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998100100_1998103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998100100_1998103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998100100_1998103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998100100_1998103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998100100_1998103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998110100_1998113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998110100_1998113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998110100_1998113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998110100_1998113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998110100_1998113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.007_hgt.1998120100_1998123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.011_tmp.1998120100_1998123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.033_ugrd.1998120100_1998123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.034_vgrd.1998120100_1998123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1998/anl_p125.051_spfh.1998120100_1998123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999010100_1999013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999010100_1999013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999010100_1999013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999010100_1999013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999010100_1999013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999020100_1999022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999020100_1999022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999020100_1999022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999020100_1999022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999020100_1999022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999030100_1999033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999030100_1999033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999030100_1999033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999030100_1999033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999030100_1999033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999040100_1999043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999040100_1999043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999040100_1999043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999040100_1999043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999040100_1999043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999050100_1999053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999050100_1999053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999050100_1999053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999050100_1999053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999050100_1999053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999060100_1999063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999060100_1999063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999060100_1999063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999060100_1999063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999060100_1999063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999070100_1999073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999070100_1999073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999070100_1999073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999070100_1999073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999070100_1999073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999080100_1999083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999080100_1999083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999080100_1999083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999080100_1999083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999080100_1999083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999090100_1999093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999090100_1999093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999090100_1999093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999090100_1999093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999090100_1999093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999100100_1999103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999100100_1999103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999100100_1999103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999100100_1999103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999100100_1999103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999110100_1999113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999110100_1999113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999110100_1999113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999110100_1999113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999110100_1999113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.007_hgt.1999120100_1999123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.011_tmp.1999120100_1999123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.033_ugrd.1999120100_1999123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.034_vgrd.1999120100_1999123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1999/anl_p125.051_spfh.1999120100_1999123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000010100_2000013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000010100_2000013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000010100_2000013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000010100_2000013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000010100_2000013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000020100_2000022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000020100_2000022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000020100_2000022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000020100_2000022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000020100_2000022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000030100_2000033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000030100_2000033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000030100_2000033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000030100_2000033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000030100_2000033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000040100_2000043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000040100_2000043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000040100_2000043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000040100_2000043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000040100_2000043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000050100_2000053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000050100_2000053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000050100_2000053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000050100_2000053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000050100_2000053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000060100_2000063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000060100_2000063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000060100_2000063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000060100_2000063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000060100_2000063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000070100_2000073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000070100_2000073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000070100_2000073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000070100_2000073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000070100_2000073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000080100_2000083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000080100_2000083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000080100_2000083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000080100_2000083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000080100_2000083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000090100_2000093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000090100_2000093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000090100_2000093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000090100_2000093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000090100_2000093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000100100_2000103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000100100_2000103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000100100_2000103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000100100_2000103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000100100_2000103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000110100_2000113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000110100_2000113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000110100_2000113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000110100_2000113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000110100_2000113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.007_hgt.2000120100_2000123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.011_tmp.2000120100_2000123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.033_ugrd.2000120100_2000123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.034_vgrd.2000120100_2000123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2000/anl_p125.051_spfh.2000120100_2000123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001010100_2001013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001010100_2001013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001010100_2001013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001010100_2001013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001010100_2001013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001020100_2001022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001020100_2001022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001020100_2001022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001020100_2001022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001020100_2001022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001030100_2001033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001030100_2001033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001030100_2001033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001030100_2001033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001030100_2001033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001040100_2001043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001040100_2001043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001040100_2001043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001040100_2001043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001040100_2001043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001050100_2001053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001050100_2001053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001050100_2001053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001050100_2001053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001050100_2001053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001060100_2001063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001060100_2001063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001060100_2001063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001060100_2001063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001060100_2001063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001070100_2001073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001070100_2001073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001070100_2001073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001070100_2001073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001070100_2001073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001080100_2001083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001080100_2001083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001080100_2001083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001080100_2001083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001080100_2001083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001090100_2001093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001090100_2001093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001090100_2001093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001090100_2001093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001090100_2001093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001100100_2001103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001100100_2001103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001100100_2001103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001100100_2001103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001100100_2001103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001110100_2001113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001110100_2001113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001110100_2001113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001110100_2001113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001110100_2001113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.007_hgt.2001120100_2001123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.011_tmp.2001120100_2001123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.033_ugrd.2001120100_2001123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.034_vgrd.2001120100_2001123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2001/anl_p125.051_spfh.2001120100_2001123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002010100_2002013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002010100_2002013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002010100_2002013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002010100_2002013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002010100_2002013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002020100_2002022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002020100_2002022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002020100_2002022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002020100_2002022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002020100_2002022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002030100_2002033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002030100_2002033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002030100_2002033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002030100_2002033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002030100_2002033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002040100_2002043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002040100_2002043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002040100_2002043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002040100_2002043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002040100_2002043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002050100_2002053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002050100_2002053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002050100_2002053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002050100_2002053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002050100_2002053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002060100_2002063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002060100_2002063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002060100_2002063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002060100_2002063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002060100_2002063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002070100_2002073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002070100_2002073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002070100_2002073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002070100_2002073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002070100_2002073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002080100_2002083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002080100_2002083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002080100_2002083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002080100_2002083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002080100_2002083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002090100_2002093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002090100_2002093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002090100_2002093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002090100_2002093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002090100_2002093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002100100_2002103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002100100_2002103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002100100_2002103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002100100_2002103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002100100_2002103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002110100_2002113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002110100_2002113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002110100_2002113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002110100_2002113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002110100_2002113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.007_hgt.2002120100_2002123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.011_tmp.2002120100_2002123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.033_ugrd.2002120100_2002123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.034_vgrd.2002120100_2002123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2002/anl_p125.051_spfh.2002120100_2002123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003010100_2003013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003010100_2003013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003010100_2003013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003010100_2003013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003010100_2003013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003020100_2003022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003020100_2003022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003020100_2003022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003020100_2003022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003020100_2003022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003030100_2003033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003030100_2003033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003030100_2003033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003030100_2003033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003030100_2003033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003040100_2003043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003040100_2003043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003040100_2003043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003040100_2003043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003040100_2003043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003050100_2003053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003050100_2003053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003050100_2003053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003050100_2003053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003050100_2003053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003060100_2003063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003060100_2003063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003060100_2003063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003060100_2003063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003060100_2003063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003070100_2003073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003070100_2003073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003070100_2003073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003070100_2003073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003070100_2003073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003080100_2003083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003080100_2003083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003080100_2003083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003080100_2003083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003080100_2003083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003090100_2003093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003090100_2003093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003090100_2003093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003090100_2003093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003090100_2003093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003100100_2003103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003100100_2003103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003100100_2003103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003100100_2003103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003100100_2003103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003110100_2003113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003110100_2003113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003110100_2003113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003110100_2003113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003110100_2003113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.007_hgt.2003120100_2003123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.011_tmp.2003120100_2003123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.033_ugrd.2003120100_2003123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.034_vgrd.2003120100_2003123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2003/anl_p125.051_spfh.2003120100_2003123118
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
