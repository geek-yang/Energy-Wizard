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
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979010100_1979013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979010100_1979013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979010100_1979013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979010100_1979013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979010100_1979013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979020100_1979022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979020100_1979022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979020100_1979022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979020100_1979022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979020100_1979022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979030100_1979033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979030100_1979033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979030100_1979033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979030100_1979033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979030100_1979033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979040100_1979043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979040100_1979043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979040100_1979043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979040100_1979043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979040100_1979043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979050100_1979053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979050100_1979053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979050100_1979053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979050100_1979053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979050100_1979053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979060100_1979063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979060100_1979063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979060100_1979063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979060100_1979063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979060100_1979063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979070100_1979073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979070100_1979073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979070100_1979073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979070100_1979073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979070100_1979073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979080100_1979083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979080100_1979083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979080100_1979083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979080100_1979083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979080100_1979083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979090100_1979093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979090100_1979093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979090100_1979093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979090100_1979093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979090100_1979093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979100100_1979103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979100100_1979103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979100100_1979103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979100100_1979103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979100100_1979103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979110100_1979113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979110100_1979113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979110100_1979113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979110100_1979113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979110100_1979113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.007_hgt.1979120100_1979123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.011_tmp.1979120100_1979123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.033_ugrd.1979120100_1979123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.034_vgrd.1979120100_1979123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1979/anl_p125.051_spfh.1979120100_1979123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980010100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980010100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980010100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980010100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980010100_1980013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980020100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980020100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980020100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980020100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980020100_1980022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980030100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980030100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980030100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980030100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980030100_1980033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980040100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980040100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980040100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980040100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980040100_1980043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980050100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980050100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980050100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980050100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980050100_1980053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980060100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980060100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980060100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980060100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980060100_1980063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980070100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980070100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980070100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980070100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980070100_1980073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980080100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980080100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980080100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980080100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980080100_1980083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980090100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980090100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980090100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980090100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980090100_1980093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980100100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980100100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980100100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980100100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980100100_1980103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980110100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980110100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980110100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980110100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980110100_1980113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.007_hgt.1980120100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.011_tmp.1980120100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.033_ugrd.1980120100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.034_vgrd.1980120100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1980/anl_p125.051_spfh.1980120100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981010100_1981013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981010100_1981013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981010100_1981013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981010100_1981013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981010100_1981013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981020100_1981022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981020100_1981022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981020100_1981022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981020100_1981022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981020100_1981022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981030100_1981033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981030100_1981033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981030100_1981033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981030100_1981033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981030100_1981033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981040100_1981043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981040100_1981043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981040100_1981043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981040100_1981043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981040100_1981043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981050100_1981053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981050100_1981053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981050100_1981053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981050100_1981053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981050100_1981053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981060100_1981063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981060100_1981063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981060100_1981063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981060100_1981063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981060100_1981063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981070100_1981073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981070100_1981073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981070100_1981073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981070100_1981073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981070100_1981073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981080100_1981083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981080100_1981083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981080100_1981083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981080100_1981083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981080100_1981083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981090100_1981093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981090100_1981093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981090100_1981093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981090100_1981093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981090100_1981093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981100100_1981103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981100100_1981103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981100100_1981103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981100100_1981103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981100100_1981103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981110100_1981113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981110100_1981113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981110100_1981113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981110100_1981113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981110100_1981113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.007_hgt.1981120100_1981123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.011_tmp.1981120100_1981123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.033_ugrd.1981120100_1981123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.034_vgrd.1981120100_1981123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1981/anl_p125.051_spfh.1981120100_1981123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982010100_1982013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982010100_1982013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982010100_1982013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982010100_1982013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982010100_1982013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982020100_1982022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982020100_1982022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982020100_1982022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982020100_1982022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982020100_1982022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982030100_1982033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982030100_1982033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982030100_1982033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982030100_1982033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982030100_1982033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982040100_1982043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982040100_1982043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982040100_1982043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982040100_1982043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982040100_1982043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982050100_1982053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982050100_1982053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982050100_1982053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982050100_1982053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982050100_1982053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982060100_1982063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982060100_1982063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982060100_1982063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982060100_1982063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982060100_1982063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982070100_1982073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982070100_1982073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982070100_1982073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982070100_1982073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982070100_1982073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982080100_1982083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982080100_1982083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982080100_1982083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982080100_1982083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982080100_1982083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982090100_1982093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982090100_1982093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982090100_1982093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982090100_1982093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982090100_1982093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982100100_1982103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982100100_1982103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982100100_1982103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982100100_1982103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982100100_1982103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982110100_1982113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982110100_1982113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982110100_1982113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982110100_1982113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982110100_1982113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.007_hgt.1982120100_1982123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.011_tmp.1982120100_1982123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.033_ugrd.1982120100_1982123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.034_vgrd.1982120100_1982123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1982/anl_p125.051_spfh.1982120100_1982123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983010100_1983013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983010100_1983013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983010100_1983013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983010100_1983013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983010100_1983013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983020100_1983022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983020100_1983022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983020100_1983022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983020100_1983022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983020100_1983022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983030100_1983033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983030100_1983033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983030100_1983033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983030100_1983033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983030100_1983033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983040100_1983043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983040100_1983043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983040100_1983043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983040100_1983043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983040100_1983043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983050100_1983053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983050100_1983053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983050100_1983053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983050100_1983053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983050100_1983053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983060100_1983063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983060100_1983063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983060100_1983063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983060100_1983063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983060100_1983063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983070100_1983073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983070100_1983073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983070100_1983073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983070100_1983073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983070100_1983073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983080100_1983083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983080100_1983083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983080100_1983083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983080100_1983083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983080100_1983083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983090100_1983093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983090100_1983093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983090100_1983093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983090100_1983093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983090100_1983093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983100100_1983103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983100100_1983103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983100100_1983103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983100100_1983103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983100100_1983103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983110100_1983113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983110100_1983113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983110100_1983113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983110100_1983113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983110100_1983113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.007_hgt.1983120100_1983123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.011_tmp.1983120100_1983123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.033_ugrd.1983120100_1983123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.034_vgrd.1983120100_1983123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1983/anl_p125.051_spfh.1983120100_1983123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984010100_1984013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984010100_1984013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984010100_1984013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984010100_1984013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984010100_1984013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984020100_1984022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984020100_1984022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984020100_1984022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984020100_1984022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984020100_1984022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984030100_1984033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984030100_1984033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984030100_1984033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984030100_1984033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984030100_1984033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984040100_1984043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984040100_1984043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984040100_1984043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984040100_1984043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984040100_1984043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984050100_1984053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984050100_1984053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984050100_1984053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984050100_1984053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984050100_1984053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984060100_1984063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984060100_1984063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984060100_1984063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984060100_1984063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984060100_1984063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984070100_1984073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984070100_1984073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984070100_1984073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984070100_1984073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984070100_1984073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984080100_1984083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984080100_1984083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984080100_1984083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984080100_1984083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984080100_1984083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984090100_1984093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984090100_1984093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984090100_1984093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984090100_1984093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984090100_1984093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984100100_1984103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984100100_1984103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984100100_1984103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984100100_1984103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984100100_1984103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984110100_1984113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984110100_1984113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984110100_1984113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984110100_1984113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984110100_1984113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.007_hgt.1984120100_1984123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.011_tmp.1984120100_1984123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.033_ugrd.1984120100_1984123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.034_vgrd.1984120100_1984123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1984/anl_p125.051_spfh.1984120100_1984123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985010100_1985013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985010100_1985013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985010100_1985013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985010100_1985013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985010100_1985013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985020100_1985022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985020100_1985022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985020100_1985022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985020100_1985022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985020100_1985022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985030100_1985033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985030100_1985033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985030100_1985033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985030100_1985033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985030100_1985033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985040100_1985043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985040100_1985043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985040100_1985043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985040100_1985043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985040100_1985043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985050100_1985053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985050100_1985053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985050100_1985053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985050100_1985053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985050100_1985053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985060100_1985063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985060100_1985063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985060100_1985063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985060100_1985063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985060100_1985063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985070100_1985073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985070100_1985073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985070100_1985073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985070100_1985073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985070100_1985073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985080100_1985083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985080100_1985083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985080100_1985083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985080100_1985083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985080100_1985083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985090100_1985093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985090100_1985093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985090100_1985093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985090100_1985093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985090100_1985093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985100100_1985103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985100100_1985103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985100100_1985103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985100100_1985103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985100100_1985103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985110100_1985113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985110100_1985113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985110100_1985113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985110100_1985113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985110100_1985113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.007_hgt.1985120100_1985123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.011_tmp.1985120100_1985123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.033_ugrd.1985120100_1985123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.034_vgrd.1985120100_1985123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1985/anl_p125.051_spfh.1985120100_1985123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986010100_1986013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986010100_1986013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986010100_1986013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986010100_1986013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986010100_1986013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986020100_1986022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986020100_1986022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986020100_1986022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986020100_1986022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986020100_1986022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986030100_1986033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986030100_1986033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986030100_1986033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986030100_1986033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986030100_1986033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986040100_1986043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986040100_1986043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986040100_1986043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986040100_1986043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986040100_1986043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986050100_1986053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986050100_1986053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986050100_1986053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986050100_1986053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986050100_1986053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986060100_1986063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986060100_1986063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986060100_1986063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986060100_1986063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986060100_1986063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986070100_1986073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986070100_1986073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986070100_1986073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986070100_1986073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986070100_1986073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986080100_1986083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986080100_1986083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986080100_1986083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986080100_1986083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986080100_1986083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986090100_1986093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986090100_1986093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986090100_1986093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986090100_1986093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986090100_1986093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986100100_1986103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986100100_1986103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986100100_1986103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986100100_1986103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986100100_1986103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986110100_1986113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986110100_1986113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986110100_1986113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986110100_1986113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986110100_1986113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.007_hgt.1986120100_1986123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.011_tmp.1986120100_1986123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.033_ugrd.1986120100_1986123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.034_vgrd.1986120100_1986123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1986/anl_p125.051_spfh.1986120100_1986123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987010100_1987013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987010100_1987013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987010100_1987013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987010100_1987013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987010100_1987013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987020100_1987022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987020100_1987022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987020100_1987022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987020100_1987022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987020100_1987022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987030100_1987033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987030100_1987033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987030100_1987033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987030100_1987033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987030100_1987033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987040100_1987043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987040100_1987043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987040100_1987043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987040100_1987043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987040100_1987043018
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
