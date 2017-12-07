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
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1958/anl_surf.001_pres.reg_tl319.1958010100_1958123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1959/anl_surf.001_pres.reg_tl319.1959010100_1959123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1960/anl_surf.001_pres.reg_tl319.1960010100_1960123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1961/anl_surf.001_pres.reg_tl319.1961010100_1961123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1962/anl_surf.001_pres.reg_tl319.1962010100_1962123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1963/anl_surf.001_pres.reg_tl319.1963010100_1963123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1964/anl_surf.001_pres.reg_tl319.1964010100_1964123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1965/anl_surf.001_pres.reg_tl319.1965010100_1965123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1966/anl_surf.001_pres.reg_tl319.1966010100_1966123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1967/anl_surf.001_pres.reg_tl319.1967010100_1967123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1968/anl_surf.001_pres.reg_tl319.1968010100_1968123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1969/anl_surf.001_pres.reg_tl319.1969010100_1969123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1970/anl_surf.001_pres.reg_tl319.1970010100_1970123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1971/anl_surf.001_pres.reg_tl319.1971010100_1971123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1972/anl_surf.001_pres.reg_tl319.1972010100_1972123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1973/anl_surf.001_pres.reg_tl319.1973010100_1973123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1974/anl_surf.001_pres.reg_tl319.1974010100_1974123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1975/anl_surf.001_pres.reg_tl319.1975010100_1975123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1976/anl_surf.001_pres.reg_tl319.1976010100_1976123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1977/anl_surf.001_pres.reg_tl319.1977010100_1977123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1978/anl_surf.001_pres.reg_tl319.1978010100_1978123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1979/anl_surf.001_pres.reg_tl319.1979010100_1979123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1980/anl_surf.001_pres.reg_tl319.1980010100_1980123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1981/anl_surf.001_pres.reg_tl319.1981010100_1981123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1982/anl_surf.001_pres.reg_tl319.1982010100_1982123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1983/anl_surf.001_pres.reg_tl319.1983010100_1983123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1984/anl_surf.001_pres.reg_tl319.1984010100_1984123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1985/anl_surf.001_pres.reg_tl319.1985010100_1985123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1986/anl_surf.001_pres.reg_tl319.1986010100_1986123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1987/anl_surf.001_pres.reg_tl319.1987010100_1987123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1988/anl_surf.001_pres.reg_tl319.1988010100_1988123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1989/anl_surf.001_pres.reg_tl319.1989010100_1989123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1990/anl_surf.001_pres.reg_tl319.1990010100_1990123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1991/anl_surf.001_pres.reg_tl319.1991010100_1991123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1992/anl_surf.001_pres.reg_tl319.1992010100_1992123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1993/anl_surf.001_pres.reg_tl319.1993010100_1993123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1994/anl_surf.001_pres.reg_tl319.1994010100_1994123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1995/anl_surf.001_pres.reg_tl319.1995010100_1995123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1996/anl_surf.001_pres.reg_tl319.1996010100_1996123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1997/anl_surf.001_pres.reg_tl319.1997010100_1997123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1998/anl_surf.001_pres.reg_tl319.1998010100_1998123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/1999/anl_surf.001_pres.reg_tl319.1999010100_1999123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2000/anl_surf.001_pres.reg_tl319.2000010100_2000123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2001/anl_surf.001_pres.reg_tl319.2001010100_2001123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2002/anl_surf.001_pres.reg_tl319.2002010100_2002123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2003/anl_surf.001_pres.reg_tl319.2003010100_2003123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2004/anl_surf.001_pres.reg_tl319.2004010100_2004123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2005/anl_surf.001_pres.reg_tl319.2005010100_2005123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2006/anl_surf.001_pres.reg_tl319.2006010100_2006123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2007/anl_surf.001_pres.reg_tl319.2007010100_2007123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2008/anl_surf.001_pres.reg_tl319.2008010100_2008123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2009/anl_surf.001_pres.reg_tl319.2009010100_2009123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2010/anl_surf.001_pres.reg_tl319.2010010100_2010123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2011/anl_surf.001_pres.reg_tl319.2011010100_2011123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2012/anl_surf.001_pres.reg_tl319.2012010100_2012123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2013/anl_surf.001_pres.reg_tl319.2013010100_2013123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014010100_2014013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014020100_2014022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014030100_2014033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014040100_2014043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014050100_2014053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014060100_2014063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014070100_2014073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014080100_2014083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014090100_2014093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014100100_2014103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014110100_2014113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2014/anl_surf.001_pres.reg_tl319.2014120100_2014123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015010100_2015013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015020100_2015022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015030100_2015033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015040100_2015043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015050100_2015053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015060100_2015063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015070100_2015073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015080100_2015083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015090100_2015093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015100100_2015103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015110100_2015113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2015/anl_surf.001_pres.reg_tl319.2015120100_2015123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016010100_2016013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016020100_2016022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016030100_2016033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016040100_2016043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016050100_2016053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016060100_2016063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016070100_2016073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016080100_2016083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016090100_2016093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016100100_2016103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016110100_2016113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2016/anl_surf.001_pres.reg_tl319.2016120100_2016123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2017/anl_surf.001_pres.reg_tl319.2017010100_2017013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2017/anl_surf.001_pres.reg_tl319.2017020100_2017022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2017/anl_surf.001_pres.reg_tl319.2017030100_2017033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2017/anl_surf.001_pres.reg_tl319.2017040100_2017043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2017/anl_surf.001_pres.reg_tl319.2017050100_2017053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_surf/2017/anl_surf.001_pres.reg_tl319.2017060100_2017063018
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
