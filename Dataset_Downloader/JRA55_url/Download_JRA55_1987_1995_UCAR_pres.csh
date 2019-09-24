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
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987050100_1987053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987050100_1987053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987050100_1987053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987050100_1987053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987050100_1987053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987060100_1987063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987060100_1987063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987060100_1987063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987060100_1987063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987060100_1987063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987070100_1987073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987070100_1987073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987070100_1987073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987070100_1987073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987070100_1987073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987080100_1987083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987080100_1987083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987080100_1987083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987080100_1987083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987080100_1987083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987090100_1987093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987090100_1987093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987090100_1987093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987090100_1987093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987090100_1987093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987100100_1987103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987100100_1987103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987100100_1987103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987100100_1987103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987100100_1987103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987110100_1987113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987110100_1987113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987110100_1987113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987110100_1987113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987110100_1987113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.007_hgt.1987120100_1987123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.011_tmp.1987120100_1987123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.033_ugrd.1987120100_1987123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.034_vgrd.1987120100_1987123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1987/anl_p125.051_spfh.1987120100_1987123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988010100_1988013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988010100_1988013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988010100_1988013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988010100_1988013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988010100_1988013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988020100_1988022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988020100_1988022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988020100_1988022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988020100_1988022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988020100_1988022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988030100_1988033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988030100_1988033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988030100_1988033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988030100_1988033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988030100_1988033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988040100_1988043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988040100_1988043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988040100_1988043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988040100_1988043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988040100_1988043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988050100_1988053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988050100_1988053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988050100_1988053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988050100_1988053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988050100_1988053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988060100_1988063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988060100_1988063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988060100_1988063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988060100_1988063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988060100_1988063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988070100_1988073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988070100_1988073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988070100_1988073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988070100_1988073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988070100_1988073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988080100_1988083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988080100_1988083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988080100_1988083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988080100_1988083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988080100_1988083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988090100_1988093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988090100_1988093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988090100_1988093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988090100_1988093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988090100_1988093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988100100_1988103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988100100_1988103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988100100_1988103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988100100_1988103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988100100_1988103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988110100_1988113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988110100_1988113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988110100_1988113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988110100_1988113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988110100_1988113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.007_hgt.1988120100_1988123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.011_tmp.1988120100_1988123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.033_ugrd.1988120100_1988123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.034_vgrd.1988120100_1988123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1988/anl_p125.051_spfh.1988120100_1988123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989010100_1989013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989010100_1989013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989010100_1989013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989010100_1989013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989010100_1989013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989020100_1989022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989020100_1989022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989020100_1989022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989020100_1989022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989020100_1989022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989030100_1989033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989030100_1989033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989030100_1989033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989030100_1989033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989030100_1989033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989040100_1989043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989040100_1989043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989040100_1989043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989040100_1989043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989040100_1989043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989050100_1989053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989050100_1989053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989050100_1989053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989050100_1989053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989050100_1989053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989060100_1989063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989060100_1989063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989060100_1989063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989060100_1989063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989060100_1989063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989070100_1989073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989070100_1989073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989070100_1989073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989070100_1989073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989070100_1989073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989080100_1989083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989080100_1989083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989080100_1989083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989080100_1989083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989080100_1989083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989090100_1989093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989090100_1989093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989090100_1989093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989090100_1989093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989090100_1989093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989100100_1989103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989100100_1989103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989100100_1989103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989100100_1989103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989100100_1989103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989110100_1989113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989110100_1989113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989110100_1989113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989110100_1989113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989110100_1989113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.007_hgt.1989120100_1989123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.011_tmp.1989120100_1989123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.033_ugrd.1989120100_1989123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.034_vgrd.1989120100_1989123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1989/anl_p125.051_spfh.1989120100_1989123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990010100_1990013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990010100_1990013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990010100_1990013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990010100_1990013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990010100_1990013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990020100_1990022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990020100_1990022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990020100_1990022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990020100_1990022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990020100_1990022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990030100_1990033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990030100_1990033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990030100_1990033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990030100_1990033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990030100_1990033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990040100_1990043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990040100_1990043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990040100_1990043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990040100_1990043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990040100_1990043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990050100_1990053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990050100_1990053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990050100_1990053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990050100_1990053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990050100_1990053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990060100_1990063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990060100_1990063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990060100_1990063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990060100_1990063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990060100_1990063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990070100_1990073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990070100_1990073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990070100_1990073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990070100_1990073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990070100_1990073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990080100_1990083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990080100_1990083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990080100_1990083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990080100_1990083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990080100_1990083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990090100_1990093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990090100_1990093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990090100_1990093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990090100_1990093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990090100_1990093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990100100_1990103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990100100_1990103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990100100_1990103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990100100_1990103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990100100_1990103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990110100_1990113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990110100_1990113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990110100_1990113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990110100_1990113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990110100_1990113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.007_hgt.1990120100_1990123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.011_tmp.1990120100_1990123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.033_ugrd.1990120100_1990123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.034_vgrd.1990120100_1990123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1990/anl_p125.051_spfh.1990120100_1990123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991010100_1991013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991010100_1991013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991010100_1991013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991010100_1991013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991010100_1991013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991020100_1991022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991020100_1991022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991020100_1991022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991020100_1991022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991020100_1991022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991030100_1991033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991030100_1991033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991030100_1991033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991030100_1991033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991030100_1991033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991040100_1991043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991040100_1991043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991040100_1991043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991040100_1991043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991040100_1991043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991050100_1991053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991050100_1991053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991050100_1991053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991050100_1991053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991050100_1991053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991060100_1991063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991060100_1991063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991060100_1991063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991060100_1991063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991060100_1991063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991070100_1991073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991070100_1991073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991070100_1991073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991070100_1991073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991070100_1991073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991080100_1991083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991080100_1991083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991080100_1991083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991080100_1991083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991080100_1991083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991090100_1991093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991090100_1991093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991090100_1991093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991090100_1991093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991090100_1991093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991100100_1991103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991100100_1991103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991100100_1991103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991100100_1991103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991100100_1991103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991110100_1991113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991110100_1991113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991110100_1991113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991110100_1991113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991110100_1991113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.007_hgt.1991120100_1991123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.011_tmp.1991120100_1991123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.033_ugrd.1991120100_1991123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.034_vgrd.1991120100_1991123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1991/anl_p125.051_spfh.1991120100_1991123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992010100_1992013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992010100_1992013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992010100_1992013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992010100_1992013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992010100_1992013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992020100_1992022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992020100_1992022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992020100_1992022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992020100_1992022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992020100_1992022918
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992030100_1992033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992030100_1992033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992030100_1992033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992030100_1992033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992030100_1992033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992040100_1992043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992040100_1992043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992040100_1992043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992040100_1992043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992040100_1992043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992050100_1992053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992050100_1992053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992050100_1992053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992050100_1992053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992050100_1992053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992060100_1992063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992060100_1992063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992060100_1992063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992060100_1992063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992060100_1992063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992070100_1992073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992070100_1992073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992070100_1992073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992070100_1992073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992070100_1992073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992080100_1992083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992080100_1992083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992080100_1992083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992080100_1992083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992080100_1992083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992090100_1992093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992090100_1992093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992090100_1992093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992090100_1992093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992090100_1992093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992100100_1992103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992100100_1992103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992100100_1992103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992100100_1992103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992100100_1992103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992110100_1992113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992110100_1992113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992110100_1992113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992110100_1992113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992110100_1992113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.007_hgt.1992120100_1992123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.011_tmp.1992120100_1992123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.033_ugrd.1992120100_1992123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.034_vgrd.1992120100_1992123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1992/anl_p125.051_spfh.1992120100_1992123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993010100_1993013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993010100_1993013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993010100_1993013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993010100_1993013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993010100_1993013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993020100_1993022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993020100_1993022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993020100_1993022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993020100_1993022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993020100_1993022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993030100_1993033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993030100_1993033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993030100_1993033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993030100_1993033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993030100_1993033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993040100_1993043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993040100_1993043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993040100_1993043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993040100_1993043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993040100_1993043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993050100_1993053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993050100_1993053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993050100_1993053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993050100_1993053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993050100_1993053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993060100_1993063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993060100_1993063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993060100_1993063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993060100_1993063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993060100_1993063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993070100_1993073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993070100_1993073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993070100_1993073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993070100_1993073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993070100_1993073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993080100_1993083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993080100_1993083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993080100_1993083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993080100_1993083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993080100_1993083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993090100_1993093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993090100_1993093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993090100_1993093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993090100_1993093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993090100_1993093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993100100_1993103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993100100_1993103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993100100_1993103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993100100_1993103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993100100_1993103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993110100_1993113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993110100_1993113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993110100_1993113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993110100_1993113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993110100_1993113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.007_hgt.1993120100_1993123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.011_tmp.1993120100_1993123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.033_ugrd.1993120100_1993123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.034_vgrd.1993120100_1993123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1993/anl_p125.051_spfh.1993120100_1993123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994010100_1994013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994010100_1994013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994010100_1994013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994010100_1994013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994010100_1994013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994020100_1994022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994020100_1994022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994020100_1994022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994020100_1994022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994020100_1994022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994030100_1994033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994030100_1994033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994030100_1994033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994030100_1994033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994030100_1994033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994040100_1994043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994040100_1994043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994040100_1994043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994040100_1994043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994040100_1994043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994050100_1994053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994050100_1994053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994050100_1994053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994050100_1994053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994050100_1994053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994060100_1994063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994060100_1994063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994060100_1994063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994060100_1994063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994060100_1994063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994070100_1994073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994070100_1994073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994070100_1994073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994070100_1994073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994070100_1994073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994080100_1994083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994080100_1994083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994080100_1994083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994080100_1994083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994080100_1994083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994090100_1994093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994090100_1994093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994090100_1994093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994090100_1994093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994090100_1994093018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994100100_1994103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994100100_1994103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994100100_1994103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994100100_1994103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994100100_1994103118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994110100_1994113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994110100_1994113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994110100_1994113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994110100_1994113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994110100_1994113018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.007_hgt.1994120100_1994123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.011_tmp.1994120100_1994123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.033_ugrd.1994120100_1994123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.034_vgrd.1994120100_1994123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1994/anl_p125.051_spfh.1994120100_1994123118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995010100_1995013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995010100_1995013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995010100_1995013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995010100_1995013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995010100_1995013118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995020100_1995022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995020100_1995022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995020100_1995022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995020100_1995022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995020100_1995022818
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995030100_1995033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995030100_1995033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995030100_1995033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995030100_1995033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995030100_1995033118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995040100_1995043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995040100_1995043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995040100_1995043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995040100_1995043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995040100_1995043018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995050100_1995053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995050100_1995053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995050100_1995053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995050100_1995053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995050100_1995053118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995060100_1995063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995060100_1995063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995060100_1995063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995060100_1995063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995060100_1995063018
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995070100_1995073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995070100_1995073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995070100_1995073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995070100_1995073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995070100_1995073118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.007_hgt.1995080100_1995083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.011_tmp.1995080100_1995083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.033_ugrd.1995080100_1995083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.034_vgrd.1995080100_1995083118
wget $cert_opt $opts --load-cookies auth.rda.ucar.edu.$$ https://rda.ucar.edu/data/ds628.0/anl_p125/1995/anl_p125.051_spfh.1995080100_1995083118
#
# clean up
rm auth.rda.ucar.edu.$$ auth_status.rda.ucar.edu
