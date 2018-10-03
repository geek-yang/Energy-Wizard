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
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1978/fcst_phy2m.121_lhtfl.reg_tl319.197801_197812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1978/fcst_phy2m.122_shtfl.reg_tl319.197801_197812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1978/fcst_phy2m.204_dswrf.reg_tl319.197801_197812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1978/fcst_phy2m.205_dlwrf.reg_tl319.197801_197812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1978/fcst_phy2m.211_uswrf.reg_tl319.197801_197812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1978/fcst_phy2m.212_ulwrf.reg_tl319.197801_197812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1979/fcst_phy2m.121_lhtfl.reg_tl319.197901_197912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1979/fcst_phy2m.122_shtfl.reg_tl319.197901_197912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1979/fcst_phy2m.204_dswrf.reg_tl319.197901_197912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1979/fcst_phy2m.205_dlwrf.reg_tl319.197901_197912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1979/fcst_phy2m.211_uswrf.reg_tl319.197901_197912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1979/fcst_phy2m.212_ulwrf.reg_tl319.197901_197912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1980/fcst_phy2m.121_lhtfl.reg_tl319.198001_198012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1980/fcst_phy2m.122_shtfl.reg_tl319.198001_198012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1980/fcst_phy2m.204_dswrf.reg_tl319.198001_198012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1980/fcst_phy2m.205_dlwrf.reg_tl319.198001_198012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1980/fcst_phy2m.211_uswrf.reg_tl319.198001_198012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1980/fcst_phy2m.212_ulwrf.reg_tl319.198001_198012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1981/fcst_phy2m.121_lhtfl.reg_tl319.198101_198112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1981/fcst_phy2m.122_shtfl.reg_tl319.198101_198112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1981/fcst_phy2m.204_dswrf.reg_tl319.198101_198112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1981/fcst_phy2m.205_dlwrf.reg_tl319.198101_198112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1981/fcst_phy2m.211_uswrf.reg_tl319.198101_198112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1981/fcst_phy2m.212_ulwrf.reg_tl319.198101_198112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1982/fcst_phy2m.121_lhtfl.reg_tl319.198201_198212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1982/fcst_phy2m.122_shtfl.reg_tl319.198201_198212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1982/fcst_phy2m.204_dswrf.reg_tl319.198201_198212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1982/fcst_phy2m.205_dlwrf.reg_tl319.198201_198212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1982/fcst_phy2m.211_uswrf.reg_tl319.198201_198212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1982/fcst_phy2m.212_ulwrf.reg_tl319.198201_198212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1983/fcst_phy2m.121_lhtfl.reg_tl319.198301_198312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1983/fcst_phy2m.122_shtfl.reg_tl319.198301_198312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1983/fcst_phy2m.204_dswrf.reg_tl319.198301_198312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1983/fcst_phy2m.205_dlwrf.reg_tl319.198301_198312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1983/fcst_phy2m.211_uswrf.reg_tl319.198301_198312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1983/fcst_phy2m.212_ulwrf.reg_tl319.198301_198312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1984/fcst_phy2m.121_lhtfl.reg_tl319.198401_198412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1984/fcst_phy2m.122_shtfl.reg_tl319.198401_198412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1984/fcst_phy2m.204_dswrf.reg_tl319.198401_198412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1984/fcst_phy2m.205_dlwrf.reg_tl319.198401_198412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1984/fcst_phy2m.211_uswrf.reg_tl319.198401_198412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1984/fcst_phy2m.212_ulwrf.reg_tl319.198401_198412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1985/fcst_phy2m.121_lhtfl.reg_tl319.198501_198512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1985/fcst_phy2m.122_shtfl.reg_tl319.198501_198512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1985/fcst_phy2m.204_dswrf.reg_tl319.198501_198512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1985/fcst_phy2m.205_dlwrf.reg_tl319.198501_198512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1985/fcst_phy2m.211_uswrf.reg_tl319.198501_198512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1985/fcst_phy2m.212_ulwrf.reg_tl319.198501_198512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1986/fcst_phy2m.121_lhtfl.reg_tl319.198601_198612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1986/fcst_phy2m.122_shtfl.reg_tl319.198601_198612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1986/fcst_phy2m.204_dswrf.reg_tl319.198601_198612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1986/fcst_phy2m.205_dlwrf.reg_tl319.198601_198612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1986/fcst_phy2m.211_uswrf.reg_tl319.198601_198612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1986/fcst_phy2m.212_ulwrf.reg_tl319.198601_198612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1987/fcst_phy2m.121_lhtfl.reg_tl319.198701_198712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1987/fcst_phy2m.122_shtfl.reg_tl319.198701_198712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1987/fcst_phy2m.204_dswrf.reg_tl319.198701_198712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1987/fcst_phy2m.205_dlwrf.reg_tl319.198701_198712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1987/fcst_phy2m.211_uswrf.reg_tl319.198701_198712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1987/fcst_phy2m.212_ulwrf.reg_tl319.198701_198712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1988/fcst_phy2m.121_lhtfl.reg_tl319.198801_198812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1988/fcst_phy2m.122_shtfl.reg_tl319.198801_198812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1988/fcst_phy2m.204_dswrf.reg_tl319.198801_198812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1988/fcst_phy2m.205_dlwrf.reg_tl319.198801_198812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1988/fcst_phy2m.211_uswrf.reg_tl319.198801_198812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1988/fcst_phy2m.212_ulwrf.reg_tl319.198801_198812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1989/fcst_phy2m.121_lhtfl.reg_tl319.198901_198912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1989/fcst_phy2m.122_shtfl.reg_tl319.198901_198912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1989/fcst_phy2m.204_dswrf.reg_tl319.198901_198912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1989/fcst_phy2m.205_dlwrf.reg_tl319.198901_198912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1989/fcst_phy2m.211_uswrf.reg_tl319.198901_198912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1989/fcst_phy2m.212_ulwrf.reg_tl319.198901_198912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1990/fcst_phy2m.121_lhtfl.reg_tl319.199001_199012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1990/fcst_phy2m.122_shtfl.reg_tl319.199001_199012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1990/fcst_phy2m.204_dswrf.reg_tl319.199001_199012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1990/fcst_phy2m.205_dlwrf.reg_tl319.199001_199012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1990/fcst_phy2m.211_uswrf.reg_tl319.199001_199012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1990/fcst_phy2m.212_ulwrf.reg_tl319.199001_199012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1991/fcst_phy2m.121_lhtfl.reg_tl319.199101_199112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1991/fcst_phy2m.122_shtfl.reg_tl319.199101_199112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1991/fcst_phy2m.204_dswrf.reg_tl319.199101_199112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1991/fcst_phy2m.205_dlwrf.reg_tl319.199101_199112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1991/fcst_phy2m.211_uswrf.reg_tl319.199101_199112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1991/fcst_phy2m.212_ulwrf.reg_tl319.199101_199112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1992/fcst_phy2m.121_lhtfl.reg_tl319.199201_199212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1992/fcst_phy2m.122_shtfl.reg_tl319.199201_199212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1992/fcst_phy2m.204_dswrf.reg_tl319.199201_199212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1992/fcst_phy2m.205_dlwrf.reg_tl319.199201_199212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1992/fcst_phy2m.211_uswrf.reg_tl319.199201_199212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1992/fcst_phy2m.212_ulwrf.reg_tl319.199201_199212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1993/fcst_phy2m.121_lhtfl.reg_tl319.199301_199312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1993/fcst_phy2m.122_shtfl.reg_tl319.199301_199312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1993/fcst_phy2m.204_dswrf.reg_tl319.199301_199312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1993/fcst_phy2m.205_dlwrf.reg_tl319.199301_199312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1993/fcst_phy2m.211_uswrf.reg_tl319.199301_199312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1993/fcst_phy2m.212_ulwrf.reg_tl319.199301_199312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1994/fcst_phy2m.121_lhtfl.reg_tl319.199401_199412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1994/fcst_phy2m.122_shtfl.reg_tl319.199401_199412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1994/fcst_phy2m.204_dswrf.reg_tl319.199401_199412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1994/fcst_phy2m.205_dlwrf.reg_tl319.199401_199412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1994/fcst_phy2m.211_uswrf.reg_tl319.199401_199412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1994/fcst_phy2m.212_ulwrf.reg_tl319.199401_199412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1995/fcst_phy2m.121_lhtfl.reg_tl319.199501_199512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1995/fcst_phy2m.122_shtfl.reg_tl319.199501_199512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1995/fcst_phy2m.204_dswrf.reg_tl319.199501_199512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1995/fcst_phy2m.205_dlwrf.reg_tl319.199501_199512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1995/fcst_phy2m.211_uswrf.reg_tl319.199501_199512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1995/fcst_phy2m.212_ulwrf.reg_tl319.199501_199512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1996/fcst_phy2m.121_lhtfl.reg_tl319.199601_199612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1996/fcst_phy2m.122_shtfl.reg_tl319.199601_199612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1996/fcst_phy2m.204_dswrf.reg_tl319.199601_199612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1996/fcst_phy2m.205_dlwrf.reg_tl319.199601_199612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1996/fcst_phy2m.211_uswrf.reg_tl319.199601_199612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1996/fcst_phy2m.212_ulwrf.reg_tl319.199601_199612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1997/fcst_phy2m.121_lhtfl.reg_tl319.199701_199712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1997/fcst_phy2m.122_shtfl.reg_tl319.199701_199712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1997/fcst_phy2m.204_dswrf.reg_tl319.199701_199712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1997/fcst_phy2m.205_dlwrf.reg_tl319.199701_199712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1997/fcst_phy2m.211_uswrf.reg_tl319.199701_199712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1997/fcst_phy2m.212_ulwrf.reg_tl319.199701_199712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1998/fcst_phy2m.121_lhtfl.reg_tl319.199801_199812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1998/fcst_phy2m.122_shtfl.reg_tl319.199801_199812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1998/fcst_phy2m.204_dswrf.reg_tl319.199801_199812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1998/fcst_phy2m.205_dlwrf.reg_tl319.199801_199812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1998/fcst_phy2m.211_uswrf.reg_tl319.199801_199812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1998/fcst_phy2m.212_ulwrf.reg_tl319.199801_199812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1999/fcst_phy2m.121_lhtfl.reg_tl319.199901_199912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1999/fcst_phy2m.122_shtfl.reg_tl319.199901_199912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1999/fcst_phy2m.204_dswrf.reg_tl319.199901_199912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1999/fcst_phy2m.205_dlwrf.reg_tl319.199901_199912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1999/fcst_phy2m.211_uswrf.reg_tl319.199901_199912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/1999/fcst_phy2m.212_ulwrf.reg_tl319.199901_199912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2000/fcst_phy2m.121_lhtfl.reg_tl319.200001_200012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2000/fcst_phy2m.122_shtfl.reg_tl319.200001_200012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2000/fcst_phy2m.204_dswrf.reg_tl319.200001_200012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2000/fcst_phy2m.205_dlwrf.reg_tl319.200001_200012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2000/fcst_phy2m.211_uswrf.reg_tl319.200001_200012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2000/fcst_phy2m.212_ulwrf.reg_tl319.200001_200012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2001/fcst_phy2m.121_lhtfl.reg_tl319.200101_200112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2001/fcst_phy2m.122_shtfl.reg_tl319.200101_200112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2001/fcst_phy2m.204_dswrf.reg_tl319.200101_200112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2001/fcst_phy2m.205_dlwrf.reg_tl319.200101_200112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2001/fcst_phy2m.211_uswrf.reg_tl319.200101_200112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2001/fcst_phy2m.212_ulwrf.reg_tl319.200101_200112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2002/fcst_phy2m.121_lhtfl.reg_tl319.200201_200212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2002/fcst_phy2m.122_shtfl.reg_tl319.200201_200212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2002/fcst_phy2m.204_dswrf.reg_tl319.200201_200212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2002/fcst_phy2m.205_dlwrf.reg_tl319.200201_200212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2002/fcst_phy2m.211_uswrf.reg_tl319.200201_200212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2002/fcst_phy2m.212_ulwrf.reg_tl319.200201_200212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2003/fcst_phy2m.121_lhtfl.reg_tl319.200301_200312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2003/fcst_phy2m.122_shtfl.reg_tl319.200301_200312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2003/fcst_phy2m.204_dswrf.reg_tl319.200301_200312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2003/fcst_phy2m.205_dlwrf.reg_tl319.200301_200312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2003/fcst_phy2m.211_uswrf.reg_tl319.200301_200312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2003/fcst_phy2m.212_ulwrf.reg_tl319.200301_200312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2004/fcst_phy2m.121_lhtfl.reg_tl319.200401_200412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2004/fcst_phy2m.122_shtfl.reg_tl319.200401_200412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2004/fcst_phy2m.204_dswrf.reg_tl319.200401_200412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2004/fcst_phy2m.205_dlwrf.reg_tl319.200401_200412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2004/fcst_phy2m.211_uswrf.reg_tl319.200401_200412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2004/fcst_phy2m.212_ulwrf.reg_tl319.200401_200412
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2005/fcst_phy2m.121_lhtfl.reg_tl319.200501_200512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2005/fcst_phy2m.122_shtfl.reg_tl319.200501_200512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2005/fcst_phy2m.204_dswrf.reg_tl319.200501_200512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2005/fcst_phy2m.205_dlwrf.reg_tl319.200501_200512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2005/fcst_phy2m.211_uswrf.reg_tl319.200501_200512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2005/fcst_phy2m.212_ulwrf.reg_tl319.200501_200512
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2006/fcst_phy2m.121_lhtfl.reg_tl319.200601_200612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2006/fcst_phy2m.122_shtfl.reg_tl319.200601_200612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2006/fcst_phy2m.204_dswrf.reg_tl319.200601_200612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2006/fcst_phy2m.205_dlwrf.reg_tl319.200601_200612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2006/fcst_phy2m.211_uswrf.reg_tl319.200601_200612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2006/fcst_phy2m.212_ulwrf.reg_tl319.200601_200612
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2007/fcst_phy2m.121_lhtfl.reg_tl319.200701_200712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2007/fcst_phy2m.122_shtfl.reg_tl319.200701_200712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2007/fcst_phy2m.204_dswrf.reg_tl319.200701_200712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2007/fcst_phy2m.205_dlwrf.reg_tl319.200701_200712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2007/fcst_phy2m.211_uswrf.reg_tl319.200701_200712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2007/fcst_phy2m.212_ulwrf.reg_tl319.200701_200712
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2008/fcst_phy2m.121_lhtfl.reg_tl319.200801_200812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2008/fcst_phy2m.122_shtfl.reg_tl319.200801_200812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2008/fcst_phy2m.204_dswrf.reg_tl319.200801_200812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2008/fcst_phy2m.205_dlwrf.reg_tl319.200801_200812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2008/fcst_phy2m.211_uswrf.reg_tl319.200801_200812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2008/fcst_phy2m.212_ulwrf.reg_tl319.200801_200812
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2009/fcst_phy2m.121_lhtfl.reg_tl319.200901_200912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2009/fcst_phy2m.122_shtfl.reg_tl319.200901_200912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2009/fcst_phy2m.204_dswrf.reg_tl319.200901_200912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2009/fcst_phy2m.205_dlwrf.reg_tl319.200901_200912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2009/fcst_phy2m.211_uswrf.reg_tl319.200901_200912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2009/fcst_phy2m.212_ulwrf.reg_tl319.200901_200912
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2010/fcst_phy2m.121_lhtfl.reg_tl319.201001_201012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2010/fcst_phy2m.122_shtfl.reg_tl319.201001_201012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2010/fcst_phy2m.204_dswrf.reg_tl319.201001_201012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2010/fcst_phy2m.205_dlwrf.reg_tl319.201001_201012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2010/fcst_phy2m.211_uswrf.reg_tl319.201001_201012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2010/fcst_phy2m.212_ulwrf.reg_tl319.201001_201012
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2011/fcst_phy2m.121_lhtfl.reg_tl319.201101_201112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2011/fcst_phy2m.122_shtfl.reg_tl319.201101_201112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2011/fcst_phy2m.204_dswrf.reg_tl319.201101_201112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2011/fcst_phy2m.205_dlwrf.reg_tl319.201101_201112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2011/fcst_phy2m.211_uswrf.reg_tl319.201101_201112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2011/fcst_phy2m.212_ulwrf.reg_tl319.201101_201112
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2012/fcst_phy2m.121_lhtfl.reg_tl319.201201_201212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2012/fcst_phy2m.122_shtfl.reg_tl319.201201_201212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2012/fcst_phy2m.204_dswrf.reg_tl319.201201_201212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2012/fcst_phy2m.205_dlwrf.reg_tl319.201201_201212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2012/fcst_phy2m.211_uswrf.reg_tl319.201201_201212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2012/fcst_phy2m.212_ulwrf.reg_tl319.201201_201212
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2013/fcst_phy2m.121_lhtfl.reg_tl319.201301_201312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2013/fcst_phy2m.122_shtfl.reg_tl319.201301_201312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2013/fcst_phy2m.204_dswrf.reg_tl319.201301_201312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2013/fcst_phy2m.205_dlwrf.reg_tl319.201301_201312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2013/fcst_phy2m.211_uswrf.reg_tl319.201301_201312
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.1/fcst_phy2m/2013/fcst_phy2m.212_ulwrf.reg_tl319.201301_201312
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
