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
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012050100_2012053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012050100_2012053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012050100_2012053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012050100_2012053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012050100_2012053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012060100_2012063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012060100_2012063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012060100_2012063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012060100_2012063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012060100_2012063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012070100_2012073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012070100_2012073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012070100_2012073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012070100_2012073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012070100_2012073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012080100_2012083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012080100_2012083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012080100_2012083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012080100_2012083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012080100_2012083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012090100_2012093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012090100_2012093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012090100_2012093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012090100_2012093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012090100_2012093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012100100_2012103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012100100_2012103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012100100_2012103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012100100_2012103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012100100_2012103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012110100_2012113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012110100_2012113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012110100_2012113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012110100_2012113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012110100_2012113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.007_hgt.2012120100_2012123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.011_tmp.2012120100_2012123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.033_ugrd.2012120100_2012123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.034_vgrd.2012120100_2012123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2012/anl_p125.051_spfh.2012120100_2012123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013010100_2013013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013010100_2013013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013010100_2013013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013010100_2013013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013010100_2013013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013020100_2013022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013020100_2013022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013020100_2013022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013020100_2013022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013020100_2013022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013030100_2013033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013030100_2013033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013030100_2013033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013030100_2013033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013030100_2013033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013040100_2013043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013040100_2013043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013040100_2013043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013040100_2013043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013040100_2013043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013050100_2013053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013050100_2013053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013050100_2013053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013050100_2013053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013050100_2013053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013060100_2013063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013060100_2013063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013060100_2013063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013060100_2013063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013060100_2013063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013070100_2013073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013070100_2013073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013070100_2013073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013070100_2013073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013070100_2013073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013080100_2013083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013080100_2013083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013080100_2013083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013080100_2013083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013080100_2013083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013090100_2013093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013090100_2013093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013090100_2013093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013090100_2013093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013090100_2013093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013100100_2013103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013100100_2013103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013100100_2013103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013100100_2013103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013100100_2013103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013110100_2013113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013110100_2013113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013110100_2013113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013110100_2013113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013110100_2013113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.007_hgt.2013120100_2013123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.011_tmp.2013120100_2013123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.033_ugrd.2013120100_2013123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.034_vgrd.2013120100_2013123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2013/anl_p125.051_spfh.2013120100_2013123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014010100_2014013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014010100_2014013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014010100_2014013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014010100_2014013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014010100_2014013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014020100_2014022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014020100_2014022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014020100_2014022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014020100_2014022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014020100_2014022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014030100_2014033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014030100_2014033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014030100_2014033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014030100_2014033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014030100_2014033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014040100_2014043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014040100_2014043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014040100_2014043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014040100_2014043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014040100_2014043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014050100_2014053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014050100_2014053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014050100_2014053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014050100_2014053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014050100_2014053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014060100_2014063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014060100_2014063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014060100_2014063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014060100_2014063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014060100_2014063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014070100_2014073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014070100_2014073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014070100_2014073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014070100_2014073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014070100_2014073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014080100_2014083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014080100_2014083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014080100_2014083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014080100_2014083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014080100_2014083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014090100_2014093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014090100_2014093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014090100_2014093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014090100_2014093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014090100_2014093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014100100_2014103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014100100_2014103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014100100_2014103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014100100_2014103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014100100_2014103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014110100_2014113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014110100_2014113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014110100_2014113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014110100_2014113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014110100_2014113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.007_hgt.2014120100_2014123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.011_tmp.2014120100_2014123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.033_ugrd.2014120100_2014123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.034_vgrd.2014120100_2014123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2014/anl_p125.051_spfh.2014120100_2014123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015010100_2015013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015010100_2015013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015010100_2015013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015010100_2015013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015010100_2015013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015020100_2015022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015020100_2015022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015020100_2015022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015020100_2015022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015020100_2015022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015030100_2015033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015030100_2015033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015030100_2015033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015030100_2015033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015030100_2015033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015040100_2015043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015040100_2015043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015040100_2015043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015040100_2015043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015040100_2015043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015050100_2015053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015050100_2015053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015050100_2015053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015050100_2015053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015050100_2015053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015060100_2015063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015060100_2015063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015060100_2015063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015060100_2015063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015060100_2015063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015070100_2015073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015070100_2015073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015070100_2015073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015070100_2015073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015070100_2015073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015080100_2015083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015080100_2015083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015080100_2015083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015080100_2015083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015080100_2015083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015090100_2015093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015090100_2015093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015090100_2015093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015090100_2015093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015090100_2015093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015100100_2015103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015100100_2015103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015100100_2015103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015100100_2015103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015100100_2015103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015110100_2015113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015110100_2015113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015110100_2015113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015110100_2015113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015110100_2015113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.007_hgt.2015120100_2015123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.011_tmp.2015120100_2015123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.033_ugrd.2015120100_2015123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.034_vgrd.2015120100_2015123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2015/anl_p125.051_spfh.2015120100_2015123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016010100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016010100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016010100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016010100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016010100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016020100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016020100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016020100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016020100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016020100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016030100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016030100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016030100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016030100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016030100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016040100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016040100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016040100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016040100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016040100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016050100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016050100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016050100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016050100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016050100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016060100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016060100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016060100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016060100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016060100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016070100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016070100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016070100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016070100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016070100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016080100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016080100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016080100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016080100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016080100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016090100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016090100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016090100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016090100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016090100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016100100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016100100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016100100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016100100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016100100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016110100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016110100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016110100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016110100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016110100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.007_hgt.2016120100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.011_tmp.2016120100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.033_ugrd.2016120100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.034_vgrd.2016120100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2016/anl_p125.051_spfh.2016120100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017010100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017010100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017010100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017010100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017010100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017020100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017020100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017020100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017020100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017020100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017030100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017030100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017030100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017030100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017030100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017040100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017040100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017040100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017040100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017040100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017050100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017050100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017050100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017050100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017050100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017060100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017060100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017060100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017060100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017060100_2017063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017070100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017070100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017070100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017070100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017070100_2017073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017080100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017080100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017080100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017080100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017080100_2017083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017090100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017090100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017090100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017090100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017090100_2017093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017100100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017100100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017100100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017100100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017100100_2017103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017110100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017110100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017110100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017110100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017110100_2017113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.007_hgt.2017120100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.011_tmp.2017120100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.033_ugrd.2017120100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.034_vgrd.2017120100_2017123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/2017/anl_p125.051_spfh.2017120100_2017123118
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
