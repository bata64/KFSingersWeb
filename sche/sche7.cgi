#!/usr/local/bin/perl

###############################################
#   sche7.cgi
#      V2.1 (2007.1.28)
#                     Copyright(C) CGI-design
###############################################

$script = 'sche7.cgi';
$base = './schedata';				#�f�[�^�i�[�f�B���N�g��
$opfile = "$base/option.txt";

@week = ('��','��','��','��','��','��','�y');
@mdays = (31,28,31,30,31,30,31,31,30,31,30,31);

open(IN,"$opfile") || &error("OPEN ERROR");		$opdata = <IN>;		close IN;
if (!$opdata) {
	$pass = &crypt('cgi');
	chmod(0666,$opfile);	open(OUT,">$opfile") || &error("OPEN ERROR");
	print OUT "$pass<>�X�P�W���[��<><>$base/style.css<><>$base/home.gif<>$base/last.gif<>$base/next.gif<>#fafaf5<>#666666<>#c00000<>#d3e3fe<>#f0f8ff<>#ffffff<>#ff0000<>#ff0000<>#0000ff<>#ffffdd<>900<>12";
	close OUT;
}

##### ���C������ #####
if ($ENV{'REQUEST_METHOD'} eq "POST") {read(STDIN, $in, $ENV{'CONTENT_LENGTH'});} else {$in = $ENV{'QUERY_STRING'};}
foreach (split(/&/,$in)) {
	($n,$val) = split(/=/);
	$val =~ tr/+/ /;
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$in{$n} = $val;
}
$mode = $in{'mode'};

open(IN,"$opfile") || &error("OPEN ERROR");
($pass,$title,$home,$style_file,$bg_img,$home_icon,$last_icon,$next_icon,$bg_color,$text_color,$title_color,$frame_color,$week_color,$combg_color,$sub_color,$holi_color,$sat_color,$today_color,$calw,$fsize) = split(/<>/,<IN>);
close IN;
@wcolor = ($holi_color,$text_color,$text_color,$text_color,$text_color,$text_color,$sat_color);

($sec,$min,$hour,$nowday,$nowmon,$nowyear) = localtime;
$nowyear += 1900;
$nowmon++;

$logyear = $in{'year'};
$logmon = $in{'mon'};
if (!$logyear) {$logyear = $nowyear; $logmon = $nowmon;}
$logfile = "$base/$logyear$logmon.txt";

$mdays = $mdays[$logmon - 1];
if ($logmon == 2 && $logyear % 4 == 0) {$mdays = 29;}

&header;
if ($mode eq 'admin') {&admin;} else {&main;}

print "</center></body></html>\n";
exit;

###
sub header {
	print "Content-type: text/html\n\n";
	print "<html><head><META HTTP-EQUIV=\"Content-type\" CONTENT=\"text/html; charset=Shift_JIS\">\n";
	print "<title>$title</title><link rel=\"stylesheet\" type=\"text/css\" href=\"$style_file\"></head>\n";
	$head = 1;
}

###
sub main {
	print "<body background=\"$bg_img\" bgcolor=\"$bg_color\" text=\"$text_color\"><center>\n";
	print "<table width=98%><tr><td width=100 valign=top>\n";
	if ($home) {if ($home_icon) {print "<a href=\"$home\"><img src=\"$home_icon\" border=0></a>";} else {print "<a href=\"$home\">[HOME]</a>";}}
	print "</td><td align=center><font color=\"$title_color\" size=\"+1\"><b>$title</b></font></td><td width=100></td></tr></table>\n";
	&dsp;
	&dsp_cal;
	print "<table width=$calw><tr><td align=right><a href=\"$script?mode=admin\">[�Ǘ�]</a></td></tr></table>\n";
	# ���̍s�͒��쌠�\���ł��̂ō폜���Ȃ��ŉ������B#
	print "<a href=\"http://cgi-design.net\" target=\"_blank\">CGI-design</a>\n";
}

###
sub dsp {
	print "<table width=",$calw-40," cellspacing=2 cellpadding=0><tr><td width=100><font size=\"+1\"><b>$logyear�N</b></font></td>\n";
	$mon = $logmon - 1;
	if ($mon < 1) {$mon = 12; $year = $logyear - 1;} else {$year = $logyear;}
	print "<td align=right><form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=\"$mode\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$year\">\n";
	print "<input type=hidden name=mon value=\"$mon\">\n";
	print "<input type=image src=\"$last_icon\"></td></form>\n";
	print "<td width=100 align=center><font size=\"+2\"><b>$logmon��</b></font></td>\n";
	$mon = $logmon + 1;
	if (12 < $mon) {$mon = 1; $year = $logyear + 1;} else {$year = $logyear;}
	print "<td><form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=\"$mode\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$year\">\n";
	print "<input type=hidden name=mon value=\"$mon\">\n";
	print "<input type=image src=\"$next_icon\"></td></form><td width=100></td></tr></table>\n";
}

###
sub dsp_cal {
	@holi=@sub=@com=();
	$flag = 0;
	if (-e $logfile) {
		open(IN,"$logfile") || &error("OPEN ERROR");
		while (<IN>) {
			($day,$holi,$sub,$com) = split(/<>/);
			$holi[$day] = $holi;
			$sub[$day] = $sub;
			$com[$day] = $com;
		}
		close IN;
	} else {
		$flag = 1;
		&holi_set;
	}
	print "<table width=$calw bgcolor=\"$combg_color\" bordercolor=\"$frame_color\" border=1 cellspacing=0 cellpadding=4 style=\"border-collapse: collapse\">\n";
	print "<tr bgcolor=\"$week_color\" align=center>\n";
	for (0 .. 6) {print "<td width=14%><font color=\"$wcolor[$_]\"><b>$week[$_]</b></font></td>\n";}
	print "</tr>\n";

	&get_date($logyear,$logmon,1);
	$w=$n=0;
	$k=1;
	for (0 .. 41) {
		if (!$w) {print "<tr>";}
		if ($wday <= $_ && $k <= $mdays) {
			if ($w == 1) {$n++;}
			$wcolor = $wcolor[$w];
			if ($flag && 2006 < $logyear) {
				&get_holiday($logmon,$k,$w,$n);
				if ($holiday) {$holi[$k] = 1; $sub[$k] = $holiday;}
			}
			if ($holi[$k]) {$wcolor = $holi_color;}
			if ($logyear == $nowyear && $logmon == $nowmon && $k == $nowday) {$bc = " bgcolor=\"$today_color\"";} else {$bc = '';}
			if ($k < 10) {$day = "&nbsp;$k";} else {$day = $k;}

			print "<td$bc height=90 valign=top><font color=\"$wcolor\" size=\"+1\"><b>$day</b></font>";
			if ($mode eq 'admin') {
				$com[$k] =~ s/<br>/\r/g;
				if ($holi[$k]) {$chk = ' checked';} else {$chk = '';}
				print "<input type=checkbox name=holi$k value=\"1\"$chk>";
				print "<input type=text size=15 name=sub$k value=\"$sub[$k]\"><br>\n";
				print "<textarea cols=15 rows=8 name=com$k wrap=soft>$com[$k]</textarea>\n";
			} else {
				print "&nbsp;<font style=\"font-size: $fsize","px\"><font color=\"$sub_color\">$sub[$k]</font><br>$com[$k]</font>\n";
			}
			print "</td>\n";
			$k++;
		} else {print "<td></td>\n";}
		$w++;
		if ($w == 7) {
			print "</tr>\n";
			if ($mdays < $k) {last;}
			$w = 0;
		}
	}
	print "</table>\n";
}

###
sub holi_set {
	$def = 0.242194*($logyear-1980)-int(($logyear-1980)/4);
	$spr = int(20.8431+$def);
	$aut = int(23.2488+$def);
	%holi_d = ('0101','����','0211','�����L�O�̓�',"03$spr",'�t���̓�','0429','���a�̓�','0503','���@�L�O��','0504','�݂ǂ�̓�','0505','���ǂ��̓�',"09$aut",'�H���̓�','1103','�����̓�','1123','�ΘJ���ӂ̓�','1223','�V�c�a����');
	%holi_w = ('012','���l�̓�','073','�C�̓�','093','�h�V�̓�','102','�̈�̓�');
}

###
sub get_holiday {
	$sm = sprintf("%02d%02d",$_[0],$_[1]);
	$holiday = $holi_d{$sm};
	if ($holiday && !$_[2]) {$hflag = 1;}
	if (!$holiday && $_[2] == 1) {
		$smw = sprintf("%02d$_[3]",$_[0]);
		$holiday = $holi_w{$smw};
	}
	if ($hflag && !$holiday) {$holiday = '�U�֋x��'; $hflag = 0;}
	if (($logyear eq '2009' || $logyear eq '2015') && $sm eq '0922') {$holiday = '�x��';}
}

###
sub get_date {
	($y,$m,$d) = @_;
	if ($m < 3) {$y--; $m+=12;}
	$wday = ($y+int($y/4)-int($y/100)+int($y/400)+int((13*$m+8)/5)+$d)%7;
}

###
sub admin {
	print "<body><center>\n";
	$inpass = $in{'pass'};
	if ($inpass eq '') {
		print "<table width=97%><tr><td><a href=\"$script\">[Return]</a></td></tr></table>\n";
		print "<br><br><br><br><h4>�p�X���[�h����͂��ĉ�����</h4>\n";
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=password name=pass size=10 maxlength=8>\n";
		print "<input type=submit value=\" �F�� \"></form>\n";
		print "</center></body></html>\n";
		exit;
	}
	$mat = &decrypt($inpass,$pass);
	if (!$mat) {&error("�p�X���[�h���Ⴂ�܂�");}

	print "<table width=100% bgcolor=\"#8c4600\"><tr><td>�@<a href=\"$script\"><font color=\"#ffffff\"><b>Return</b></font></a></td>\n";
	print "<td align=right><form action=\"$script\" method=POST>\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=submit value=\"�@�ҏW�@\">\n";
	print "<input type=submit name=set value=\"�@�ݒ�@\"></td></form><td width=10></td></tr></table><br>\n";

	$wrt = $in{'wrt'};
	if ($in{'set'}) {&setup;} else {&edt;}
}

###
sub edt {
	if ($wrt) {
		open(OUT,">$logfile") || &error("OPEN ERROR");
		for (1 .. $mdays) {
			$in{"com$_"} =~ s/\r\n|\r|\n/<br>/g;
			print OUT "$_<>$in{\"holi$_\"}<>$in{\"sub$_\"}<>$in{\"com$_\"}<>\n";
		}
		close OUT;
		chmod(0666,$logfile);
	}
	&dsp;
	print "<table><tr><td><form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=year value=\"$logyear\">\n";
	print "<input type=hidden name=mon value=\"$logmon\">\n";
	print "�x���`�F�b�N�A���L�����A�X�P�W���[������͌�A�u�o�^����v�������ĉ������B\n";
	print "�@�@<input type=submit name=wrt value=\"�o�^����\"></td></tr></table>\n";
	&dsp_cal;
	print "</form>\n";
}

###
sub setup {
	if ($wrt) {
		if ($in{'newpass'} ne '') {$pass = &crypt($in{'newpass'});}
		$title = $in{'title'};
		$home = $in{'home'};
		$style_file = $in{'style'};
		$bg_img = $in{'bg_img'};			$home_icon = $in{'home_icon'};
		$last_icon = $in{'last_icon'};		$next_icon = $in{'next_icon'};

		$bg_color = $in{'color0'};
		$text_color = $in{'color1'};
		$title_color = $in{'color2'};
		$frame_color = $in{'color3'};
		$week_color = $in{'color4'};
		$combg_color = $in{'color5'};
		$sub_color = $in{'color6'};
		$holi_color = $in{'color7'};
		$sat_color = $in{'color8'};
		$today_color = $in{'color9'};

		$calw = $in{'calw'};
		$fsize = $in{'fsize'};

		open(OUT,">$opfile") || &error("OPEN ERROR");
		print OUT "$pass<>$title<>$home<>$style_file<>$bg_img<>$home_icon<>$last_icon<>$next_icon<>$bg_color<>$text_color<>$title_color<>$frame_color<>$week_color<>$combg_color<>$sub_color<>$holi_color<>$sat_color<>$today_color<>$calw<>$fsize";
		close OUT;
	}

	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=pass value=\"$inpass\">\n";
	print "<input type=hidden name=set value=\"1\">\n";
	print "<input type=submit name=wrt value=\"�ݒ肷��\"><br><br>\n";

	print "<table bgcolor=\"#dddddd\" cellspacing=10><tr><td><table cellspacing=1 cellpadding=0>\n";
	print "<tr><td><b>�^�C�g��</b></td><td><input type=text name=title size=40 value=\"$title\"></td></tr>\n";
	print "<tr><td><b>�z�[��URL</b></td><td><input type=text size=60 name=home value=\"$home\"></td></tr>\n";
	print "<tr><td><b>�X�^�C���V�[�g</b></td><td><input type=text size=60 name=style value=\"$style_file\"></td></tr>\n";
	print "<tr><td><b>�ǎ�</b></td><td><input type=text size=60 name=bg_img value=\"$bg_img\">";
	if ($bg_img) {print "�@<img src=\"$bg_img\" width=30>";}
	print "</td></tr>\n";
	print "<tr><td><b>�z�[���A�C�R��</b></td><td><input type=text size=60 name=home_icon value=\"$home_icon\">";
	if ($home_icon) {print "�@<img src=\"$home_icon\">";}
	print "</td></tr>\n";
	print "<tr><td><b>LAST�A�C�R��</b></td><td><input type=text size=60 name=last_icon value=\"$last_icon\">�@<img src=\"$last_icon\"></td></tr>\n";
	print "<tr><td><b>NEXT�A�C�R��</b></td><td><input type=text size=60 name=next_icon value=\"$next_icon\">�@<img src=\"$next_icon\"></td></tr>\n";

	print "<tr><td></td><td><a href=\"$base/color.htm\" target=\"_blank\">�J���[�R�[�h</a></td></tr>\n";
	@name = ('��{�w�i�F','��{�����F','�^�C�g��','�g�F','�j���w�i�F','�L���w�i�F','���L����','�x���̓��t','�y�j���̓��t','�{���̔w�i�F');
	@data = ($bg_color,$text_color,$title_color,$frame_color,$week_color,$combg_color,$sub_color,$holi_color,$sat_color,$today_color);
	for (0 .. $#name) {
		print "<tr><td><b>$name[$_]</b></td><td><table cellspacing=0 cellpadding=0><tr>\n";
		print "<td><input type=text name=color$_ size=10 value=\"$data[$_]\"></td>\n";
		print "<td width=5></td><td width=80 bgcolor=\"$data[$_]\"></td></tr></table></td></tr>\n";
	}
	print "<tr><td><b>�\\���T�C�Y</b></td><td>�J�����_�[����<input type=text size=4 name=calw value=\"$calw\" style=\"text-align: right\">px\n";
	print "�@�@�����T�C�Y<input type=text size=3 name=fsize value=\"$fsize\" style=\"text-align: right\">px</td></tr>\n";
	print "<tr><td><b>�p�X���[�h�ύX</b></td><td><input type=password name=newpass size=10 maxlength=8> �i�p��8�����ȓ��j</td></tr>\n";
	print "</table></td></tr></table></form>\n";
}

###
sub crypt {
	@salt = ('a' .. 'z','A' .. 'Z','0' .. '9');
	srand;
	$salt = "$salt[int(rand($#salt))]$salt[int(rand($#salt))]";
	return crypt($_[0],$salt);
}

###
sub decrypt {
	$salt = $_[1] =~ /^\$1\$(.*)\$/ && $1 || substr($_[1],0,2);
	if (crypt($_[0],$salt) eq $_[1] || crypt($_[0],'$1$' . $salt) eq $_[1]) {return 1;}
	return 0;
}

###
sub error {
	if (!$head) {&header; print "<body><center>\n";}
	print "<br><br><br><br><h3>ERROR !!</h3><font color=red><b>$_[0]</b></font>\n";
	print "</center></body></html>\n";
	exit;
}
