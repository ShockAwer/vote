#!/usr/bin/perl
#
#�䂢�ځ[��2.1(yuivote2.cgi)
#1997.10.10����
#������ՂƁ@�΂��@�䂢������Ɓ@
#���쐬���x�ᔽ�ł��@�@�@�@�@�@�@�@�@Since  1996
#������cgi��snog�̐��삵��vote4�����ǂ������ł�
#�����������҂����Ȃ��ׁA�Ƃ肠�����񎟔z�z�Ǝg�p�͕s�ɂȂ��Ă܂�

require './jcodeLE.pl';
require './prei.cgi';

$| = 1;	
&winit;
&init;
&wdecode;
&decode;
&jikan;
if($detail){
	if(($delete eq 'on') && ($postf eq 'on')){
		&deletevote;
		&resulthtml;	#�W�v��ʍ쐬
		print "Location: $cgidir/$cginame2?detail=$detail&room=$room\n\n";
	}else{
		&readlog;
		&detailhtml;	#�R�����g�W��ʂ�
	}
	exit;
}
if($allres eq 'on'){
	if(($delete eq 'on') && ($postf eq 'on')){
		&deletevote;
		&resulthtml;	#�W�v��ʍ쐬
		print "Location: $cgidir/$cginame2?allres=on&room=$room\n\n";
	}else{
		&readlog;
		&allreshtml;	#�R�����g�W��ʂ�
	}
	exit;
}
if($postf ne 'on'){
	&err("�s���ȓ��e�ł�");
}
if( $title ne '' ){
	if( $title eq $masterkey ){
		&remakehtml;
		print "Location: $cgidir/$cginame1\n\n";
	}else{
		&wspeed;
		&make;
		&resulthtml;	#�W�v��ʍ쐬
		print "Location: $cgidir/$htmdir/$room.html\n\n";
	}
	exit;
}elsif($vote ne ''){
	&wspeed;
	&writelog;
	&resulthtml;	#�W�v��ʍ쐬
	print "Location: $cgidir/$htmdir/$room.html\n\n";
	exit;
}
&err("�s���ȓ��e�ł�");
exit;
##############################################################################
#�����ݒ�Ȃ�
sub init{
    &vote_config();
}#init END
##############################################################################
#���͕ϊ�
sub decode{

$title = $FORM{'title'};
if( $title ne '' ){
	&err("�^�C�g�����������܂��B") if(length($title) > ($namemax*2));
	$chktitle = $title;
	$chktitle =~ s/�@//g;$chktitle =~ s/ //g;
	$title = '' if( $chktitle eq '' );
}
$vote=$FORM{'vote'};
$voten=$FORM{'voten'};
&err("���[�̎d�����ԈႦ�Ă��܂��B") if( $voten ne '' && $vote ne '' );
$vote=$voten if( $vote eq '');
&err("���ږ����������܂��B") if(length($vote) > ($votemax*2) );
$chkvote = $vote;
$chkvote =~ s/�@//g;$chkvote =~ s/ //g;
$vote = '' if( $chkvote eq '' );
$chat=$FORM{'chat'};
if(length($chat) > ($chatmax*2)){&err("�R�����g���������܂��B");}
$_ = $chat;$brnum = s/ //ig;$brnum = s/�@//ig;$brnum = s/<br>//ig;
if( ($_ eq '') && ( ($vote ne '') || ($title ne '') ) ){&err("�R�����g��������Ă��܂���");}
if($brnum >= $brmax){&err("�R�����g�̍s�����������܂�");}
$detail=$FORM{'detail'};
$room = $FORM{'room'};$room =~s/\D//g;$room = '000' if($room eq '');
$mrev = $FORM{'mr'};$mrev = 'on' if($mrev eq '');$mrev = 'off' if($mrev ne 'on');
$allres=$FORM{'allres'};
$root = $FORM{'root'};
$delete = $FORM{'delete'};

&ngCheck("�I", $title, @titleNGwords);
&ngCheck("�I", $vote, @voteNGwords);
&ngCheck("�I", $voten, @votenNGwords);
&ngCheck("�I", $chat, @chatNGwords);
sub ngCheck() {
    my($msg, $target) = @_;
    $target =~ s/ //g;
    $target =~ s/�@//g;
    shift(@_);
    shift(@_);
    foreach(@_){
	&err($msg) if( $target =~ /\Q$_\E/ );
    }
}

}#decode END
##############################################################################
#�z��@lines�Ƀ��O��ǂݍ���
sub readlog{
my($m_set);

open(DB,"./$logdir/$room.dat") || &err("���O�t�@�C�����J���܂���B");
	@lines = <DB>;
close(DB);
$m_set=shift(@lines);
($title,$vchkkey,$ddata,$opwhost,$otimes,$ochat,$odate,$oxhost) = split(/:#/,$m_set);
if( $vkey ne $vchkkey ){ &err("���O�t�@�C�������Ă��܂��B"); }
}#readlog END
##############################################################################
#�`�F�b�N����������
sub writelog{	
my($m_set,$m_chktime,$m_line,$m_kpwhost,$m_dmy,$m_ktimes,$m_krev,$m_kvote,$m_chkday,$m_kchat,$m_chkchat,$m_hatu,$m_room);

open(DB,"+<./$logdir/$room.dat") || &err("���O�t�@�C�����J���܂���B");
	eval 'flock(DB,2);';
	@lines = <DB>;
	$m_set=shift(@lines);
	($title,$vchkkey,$ddata,$opwhost,$otimes,$ochat,$odate,$oxhost) = split(/:#/,$m_set);
	if( $vkey ne $vchkkey ){
		close(DB);
		&err("���O�t�@�C�������Ă��܂��B");
	}

	$m_hatu = @lines;
	if($m_hatu >= $max){
		close(DB);
		&err("���[���������ς��ɂȂ�܂����B");
	}
	$m_chktime = $times - 30*60;
	if( 'on' ne $mrev ){
		$m_chkchat = $chat;$m_chkchat =~ s/�@//g;$m_chkchat =~ s/ //g;$m_chkchat =~ s/<br>//ig;
	}
	@lines = reverse (@lines);
	foreach $m_line (@lines) {	#��l�g�D�[��}��
		($m_kpwhost, $m_ktimes, $m_krev, $m_kvote,$m_kchat) = split(/:#/, $m_line);
		if( $m_ktimes < $m_chktime ){ last; }
		if( $m_kpwhost eq $pwhost ){
			$m_kvote =~ s/�@//g;$m_kvote =~ s/ //g;
			if( 'on' eq $mrev ){
				if( $chkvote eq $m_kvote ){
					close(DB);
					&err("��l�g�D�[�}���@�\\�Ɉ���������܂����B");
				}
			}else{
				if( $chkvote eq $m_kvote ){ #2002/12/03 �ϐ������Ԉ���Ă���
					$m_kchat =~ s/�@//g;$m_kchat =~ s/ //g;$m_kchat =~ s/<br>//ig;
					if( $m_kchat eq $m_chkchat){
						close(DB);
						&err("��d�������݋֎~�@�\\�Ɉ���������܂����B");
					}else{
						last;
					}
				}
			}
		}
	}
#�V�K���[�́A������
	@lines = reverse (@lines);
	push(@lines,"$pwhost:#$times:#$mrev:#$vote:#$chat:#$date:#:#\n");
	$m_chkday = (($lday - ($times - $otimes))/$lday)*$daylimit;
	$m_chkday = $hday if( $m_chkday < $hday );
	$ddata += $aday;
	if( $ddata > $m_chkday ){ $ddata = $m_chkday; }
	elsif( $ddata < $hday ){ $ddata = $hday;}
	$ddata = sprintf("%4.2f",$ddata);
	$m_set = "$title:#$vchkkey:#$ddata:#$opwhost:#$otimes:#$ochat:#$odate:#$oxhost:#:#\n";

	$m_hatu++;
	seek(DB,0,0);	print DB $m_set; print DB @lines;
	truncate(DB,tell(DB));
close(DB);

opendir(DIR,"$coudir") || return;
	@readlist = grep(/dat/, readdir(DIR));
closedir(DIR);
foreach $m_room (@readlist) {
	if($m_room=~/$room/){
		unlink "./$coudir/$m_room";
	}
}#foreach
open(DB,">./$coudir/$m_hatu.$room.dat") || return;
close(DB);
chmod 0666, "./$coudir/$m_hatu.$room.dat";

}#writelog END
##############################################################################
#���[���ʉ��
sub resulthtml{
my($m_hatu,$m_total,$m_line,$m_dmy1,$m_wtimes,$m_wrev,$m_wvote,$m_wcvote,$m_percent,$m_img,$m_count,$m_wdetail,$m_wpwhost,$m_wdate,$m_comtimes,$m_ranka,$m_rankb,$m_rankc,$m_hatu);

open(DB,">./$tmpdir/$room.$times.$pwhost") || &err("�e���|�����t�@�C�����J���܂���");

print DB <<"_HTML_";
<HTML><HEAD>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
$metacode
<TITLE>$title </TITLE><STYLE><!--.linka{text-decoration : none;color : #A1FE9F;vertical-align : baseline;}
--></STYLE></HEAD>
$body
[<A HREF="../$cginame1">���X�g�ɖ߂�</A>] [<A href="#now">�ŋ߂̓��[</A>]<FONT COLOR="red"><B> ���@�j���[�X�T�C�g����̓��[�ő�ϖ��f���Ă��܂��B���[���ւ̃����N�͂��������������B</B></FONT><BR><BR>
<FONT SIZE=+2 COLOR="hotpink"><B>${title} </B></FONT>
<BR><BR>
<DIV ALIGN=right>($odate)</DIV><BR>
<HR><PRE><FONT SIZE=3>$ochat </FONT></PRE>
<HR>���݂̃A���P�[�g�W�v���ʂ͈ȉ��̂Ƃ���ł��B<BR>
���ꂼ��̑I�����ڂ��N���b�N����ƃR�����g���݂邱�Ƃ��ł��܂��B�i�Â����[���ɂȂ��Ă��܂��B�j<BR>
<TABLE border WIDTH=100%>
<TR><TH NOWRAP>����</TH><TH NOWRAP>�I������</TH><TH NOWRAP>�L���[���i���[���j</TH><TH NOWRAP>����</TH><TH>�O���t</TH></TR>
_HTML_

$m_hatu = @lines;
$m_total = 0;undef %votes;undef %alvotes;undef @oplist;
foreach $m_line (@lines) {
	next unless($m_line=~/:#/);
	($m_dmy, $m_dmy2, $m_wrev, $m_wvote) = split(/:#/, $m_line);
	$m_dmy =~s/\*//g;
	next if( $m_dmy eq "");
	$m_wcvote = $m_wvote;
	$m_wcvote =~ s/ //g;$m_wcvote =~ s/�@//g;
	if ( $m_wcvote ne '') {
		unless($ans{$m_wcvote}){
			$ans{$m_wcvote} = $m_wvote;
			$votes{$m_wcvote} = 0;
			$alvotes{$m_wcvote} = 0;
		}
		if($m_wrev eq 'on'){
			$votes{$m_wcvote}++;
			$m_total++;
		}
		$alvotes{$m_wcvote}++;
	}
}#foreach

$m_ranka = 1;$m_rankb = 0;$m_rankc = 0;
foreach (sort { ($votes{$b} <=> $votes{$a}) || ($alvotes{$b} <=> $alvotes{$a}) } keys %votes) {
	if( $votes{$_} == 0 ){
		$m_percent = 0;
		$m_img = 1;
	}else{
		$m_percent = int( ($votes{$_} / $m_total)*100);
		$m_img = int($m_percent * 3);
		$m_img = 1 if($m_img < 1);
	}
	$m_rankb++;
	if( $m_rankc != $votes{$_} ){
		$m_ranka = $m_rankb;
		$m_rankc = $votes{$_};
	}
	push(@oplist,$ans{$_});
	&URLEncoder($ans{$_});
	print  DB "<TR><TH NOWRAP><A HREF=\"\.\.\/$cginame2?detail=$encode&room=$room\" target=\"_blank\">$m_ranka</A></TH><TH NOWRAP><A HREF=\"\.\.\/$cginame2?detail=$encode&room=$room\">$ans{$_} </A></TH><TH NOWRAP>$votes{$_}($alvotes{$_})</TH><TH>$m_percent\% </TH><td nowrap><img src=\"$gif\" WIDTH=$m_img HEIGHT=20></td></TR>\n";
}#foreach

if($m_hatu >= $max){

print  DB <<"_HTML_";
</TABLE>
<B>�L�����[����$m_total�[�i���[����$m_hatu�[�j</B><BR><P>
<HR><A name="now">�ŋ߂̓��[</A>�i�ߋ�$comtime���ԑO�A�܂���$commax���[�j�@
<A HREF=\"\.\.\/$cginame2?allres=on&room=$room\">�S���[�\\��</A><BR>
_HTML_

}else{

print  DB <<"_HTML_";
</TABLE>
<B>�L�����[����$m_total�[�i���[����$m_hatu�[�j</B><BR><P>
<FORM METHOD="POST" ACTION="../$cginame2">
<INPUT TYPE=hidden NAME="room" VALUE="$room">
<SELECT NAME="vote" SIZE="1">
<OPTION VALUE="0" SELECTED>�I�����ĂˁB
_HTML_

foreach (@oplist) {
	print DB "<OPTION>$_\n";
}#foreach

print DB <<"_HTML_";
</SELECT><BR>
���ڂ�ǉ�����ꍇ��<INPUT TYPE=text NAME=\"voten\" SIZE=\"60\">�S�p${votemax}�����܂�<BR>
<BR>��L���ڂ�I���������R���ȒP�ɂ������������B�i�K�{�j�i�^�O�͎g���܂���B�j<BR>
<TEXTAREA NAME="chat" rows="10" cols="80"></TEXTAREA><BR>
�i${brmax}�s�A${chatmax}�����܂Łj<BR>
<input type="radio" name="mr" value="on">�L���[<input type="radio" name="mr" value="off" checked><FONT COLOR=\"#0000FF\">�����[�i�ӌ��̂݁j</FONT><BR>
<BR>
<INPUT TYPE=submit VALUE="���[����"><FONT size="-1" COLOR="red"> <A href="http://www.zianplus.net/guideline.txt">���p�K��</A>��ǂ݁A�K��Ɋ��S�ɓ��ӂ��Ă��瑗�M���Ă��������B</FONT>
<INPUT TYPE=reset VALUE="���Z�b�g"></FORM>
<HR><A name="now">�ŋ߂̓��[</A>�i�ߋ�$comtime���ԑO�A�܂���$commax���[�j�@
<A HREF=\"\.\.\/$cginame2?allres=on&room=$room\">�S���[�\\��</A><BR>
<HR>
<script type="text/javascript"><!--
  amazon_ad_tag = "wwwzianplusne-22";
  amazon_ad_width = "468";
  amazon_ad_height = "60";
  amazon_color_background = "A1FE9F";
  amazon_color_link = "0000FF";
  amazon_color_price = "FF0000";
  amazon_color_logo = "009900";
  amazon_ad_logo = "hide";
  amazon_ad_product_images = "hide";
  amazon_ad_link_target = "new";
  amazon_ad_price = "retail";
  amazon_ad_border = "hide";
//--></script>
<script type="text/javascript" src="http://www.assoc-amazon.jp/s/ads.js"></script>
<noscript><FONT SIZE=1 COLOR="red">���̃y�[�W�ł�JavaScript���g�p���Ă��܂��B</FONT></noscript>
_HTML_

}#if

$m_count = 0;$m_comtimes = $times - ($comtime*60*60);
@lines = reverse (@lines);
foreach $m_line (@lines) {
	($m_dmy1, $m_wtimes, $m_wrev, $m_wvote, $m_wchat,$m_wdate) = split(/:#/, $m_line);
	last if( ($m_wtimes < $m_comtimes) && ($m_count >= $commax) );
	$encode2 = $m_wvote;
	$encode2 =~ s/([^\w ])/'%' . unpack('H2', $1)/eg;
	$encode2 =~ tr/ /+/;
	if($m_wrev eq 'on'){
		print DB "<HR><B>$m_wvote </B><PRE><FONT SIZE=3>$m_wchat </FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)<A HREF=\"\.\.\/$cginame2?detail=$encode2&room=$room\" target=\"_blank\" class=\"linka\">__</A>+<A HREF=\"\.\.\/$cginame2?detail=$encode2&room=$room\" class=\"linka\">__</A></FONT> \n";
	}else{
		print DB "<HR><FONT COLOR=\"#0000FF\"><B>$m_wvote </B><PRE><FONT SIZE=3>$m_wchat </FONT></FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)<A HREF=\"\.\.\/$cginame2?detail=$encode2&room=$room\" target=\"_blank\" class=\"linka\">__</A>+<A HREF=\"\.\.\/$cginame2?detail=$encode2&room=$room\" class=\"linka\">__</A></FONT> \n";
	}
	$m_count++;
}#foreach
print DB "<HR>\n";
print DB "[<A HREF=\"../$cginame1\">���X�g�ɖ߂�</A>]<BR>\n";
print DB "$maruc\n";
print DB "</BODY></HTML>\n";
close(DB);

unlink "./$htmdir/$room.html";
rename("./$tmpdir/$room.$times.$pwhost","./$htmdir/$room.html");
unlink "./$tmpdir/$room.$times.$pwhost";	#�O�̈�
chmod 0666, "./$htmdir/$room.html";

}#resulthtml END
##############################################################################
#�R�����g���
sub detailhtml {
my($m_keyword,$m_line,$m_dmy,$m_times,$m_wrev,$m_wvote,$m_wdetail,$m_wdate);

print "Content-type: text/html; charset=Shift_JIS\n\n";
print <<"_HTML_";
<HTML><HEAD>
$metacode
<TITLE>$title </TITLE></HEAD>
$body
[<A HREF="./$htmdir/$room.html">���[���ʂɖ߂�</A>]<A name="ue">&nbsp;</A><A href="#sita">��</A><BR><BR>
[${detail}]�ɂ��ẴR�����g�B<BR>
<HR SIZE=5>
<noscript><FONT SIZE=+5 COLOR="red">���̃y�[�W�ł�JavaScript���g�p���Ă��܂��B(���܂ɃV���b�t�����܂���)</FONT></noscript>
_HTML_

$m_keyword = $detail;
$m_keyword =~ s/ //g;$m_keyword =~ s/�@//g;

print "<FORM method=\"POST\" ACTION=\"./$cginame2\">\n" if($root eq $masterkey);

$m_hatu = @lines;
foreach $m_line (@lines) {
	next unless($m_line=~/:#/);
	($m_dmy, $m_times, $m_wrev, $m_wvote, $m_wchat,$m_wdate) = split(/:#/, $m_line);
	$m_wvote =~ s/ //g;$m_wvote =~ s/�@//g;
	if($m_wvote eq $m_keyword ){
		print "<INPUT TYPE=checkbox NAME=\"erase\" VALUE=\"$m_times\">\n" if($root eq $masterkey);
		if($m_wrev eq 'on'){
			print "<BR><PRE><FONT SIZE=3>$m_wchat </FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)</FONT><HR>\n";
		}else{
			print "<BR><FONT COLOR=\"#0000FF\"><PRE><FONT SIZE=3>$m_wchat </FONT></FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)</FONT><HR>\n";
		}
	}
}#foreach
print qq!<INPUT TYPE=hidden NAME="erase" VALUE="dummy" ><INPUT TYPE=hidden NAME="delete" VALUE="on"><INPUT TYPE=hidden NAME="detail" VALUE="$detail" ><INPUT TYPE=hidden NAME="room" VALUE="$room" ><INPUT TYPE=hidden NAME="root" VALUE="$root" ><INPUT type=submit value="�폜"></FORM>\n! if($root eq $masterkey);

if($m_hatu >= $max){

print   <<"_HTML_";
[<A HREF=\"./$htmdir/$room.html\">���[���ʂɖ߂�</A>]<BR>
<H5 align=right><FORM method="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="detail" VALUE="$detail" >
<INPUT TYPE=hidden NAME="room" VALUE="$room" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="�Ǘ�"><BR>
$maruc
</BODY></HTML>
_HTML_

}else{

print   <<"_HTML_";
<B>${title}</B><BR>����[${detail}]
<FORM METHOD="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="room" VALUE="$room">
<INPUT TYPE=hidden NAME="vote" VALUE="$detail">
���̍��ڂɓ��[����ꍇ�A���[�̗��R���ȒP�ɂ������������B�i�K�{�j�i�^�O�͎g���܂���B�j<BR>
<TEXTAREA NAME="chat" rows="10" cols="80"></TEXTAREA><BR>
�i${brmax}�s�A${chatmax}�����܂Łj<BR>
<input type="radio" name="mr" value="on">�L���[<input type="radio" name="mr" value="off" checked><FONT COLOR=\"#0000FF\">�����[�i�ӌ��̂݁j</FONT><BR>
<BR>
<INPUT TYPE=submit VALUE="���[����"><FONT size="-1" COLOR="red"><A href="http://www.zianplus.net/guideline.txt">���p�K��</A>��ǂ݁A�K��Ɋ��S�ɓ��ӂ��Ă��瑗�M���Ă��������B</FONT>
<INPUT TYPE=reset VALUE="���Z�b�g"></FORM>
�i��l�g�D�[�}���@�\\���t���Ă��܂��B�j<HR>
<script type="text/javascript"><!--
  amazon_ad_tag = "wwwzianplusne-22";
  amazon_ad_width = "468";
  amazon_ad_height = "60";
  amazon_color_background = "A1FE9F";
  amazon_color_link = "0000FF";
  amazon_color_price = "FF0000";
  amazon_color_logo = "009900";
  amazon_ad_logo = "hide";
  amazon_ad_product_images = "hide";
  amazon_ad_link_target = "new";
  amazon_ad_price = "retail";
  amazon_ad_border = "hide";
//--></script>
<script type="text/javascript" src="http://www.assoc-amazon.jp/s/ads.js"></script>
<HR>
[<A HREF=\"./$htmdir/$room.html\">���[���ʂɖ߂�</A>]<A name="sita">&nbsp;</A><A href="#ue">��</A><BR>
<H5 align=right><FORM method="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="detail" VALUE="$detail" >
<INPUT TYPE=hidden NAME="room" VALUE="$room" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="�Ǘ�"><BR>
$maruc
</BODY></HTML>
_HTML_

}#if

}#detailhtml END
##############################################################################
#�S�R�����g���
sub allreshtml {
my($m_line,$m_dmy,$m_times,$m_wrev,$m_wvote,$m_wdate,$m_hatu);

$m_hatu = @lines;
print "Content-type: text/html; charset=Shift_JIS\n\n";
print <<"_HTML_";
<HTML><HEAD>
$metacode
<TITLE>$title </TITLE></HEAD>
$body
[<A HREF="./$htmdir/$room.html">���[���ʂɖ߂�</A>]<A name="ue">&nbsp;</A><A href="#sita">��</A><BR><BR>
<B>$title</B>�̓��[���� $m_hatu�[<BR>
<HR SIZE=5>
_HTML_

print "<FORM method=\"POST\" ACTION=\"./$cginame2\">\n" if($root eq $masterkey);
foreach $m_line (@lines) {
	next unless($m_line=~/:#/);
	($m_dmy, $m_times, $m_wrev, $m_wvote, $m_wchat,$m_wdate) = split(/:#/, $m_line);
	print "<INPUT TYPE=checkbox NAME=\"erase\" VALUE=\"$m_times\">\n" if($root eq $masterkey);
	if($m_wrev eq 'on'){
		print "<B>$m_wvote </B><BR><BR><PRE><FONT SIZE=3>$m_wchat </FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)</FONT><HR>\n";
	}else{
		print "<FONT COLOR=\"#0000FF\"><B>$m_wvote </B><BR><BR><PRE><FONT SIZE=3>$m_wchat </FONT></FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)</FONT><HR>\n";
	}
}#foreach
print qq!<INPUT TYPE=hidden NAME="erase" VALUE="dummy" ><INPUT TYPE=hidden NAME="delete" VALUE="on"><INPUT TYPE=hidden NAME="allres" VALUE="$allres" ><INPUT TYPE=hidden NAME="room" VALUE="$room" ><INPUT TYPE=hidden NAME="root" VALUE="$root" ><INPUT type=submit value="�폜"></FORM>\n! if($root eq $masterkey);

print <<"_HTML_";
[<A HREF=\"./$htmdir/$room.html\">���[���ʂɖ߂�</A>]<A name="sita">&nbsp;</A><A href="#ue">��</A><BR>
<H5 align=right><FORM method="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="allres" VALUE="$allres" >
<INPUT TYPE=hidden NAME="room" VALUE="$room" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="�Ǘ�"><BR>
$maruc
</BODY></HTML>
_HTML_
}#allreslhtml END
##############################################################################
#�t�q�k�p�ϊ�
sub URLEncoder {
$encode = $_[0];
$encode =~ s/([^0-9A-Za-z_ ])/"%".unpack("H2",$1)/ge;
$encode =~ tr/ /+/;
}
##################################################
#�V�K�b�胋�[����ݒu
sub make {
my($m_set,$m_title2,$m_dmy,$m_ddata,$m_chkpwlhost,$m_chktimes,$m_chkcou,$m_chktm,$m_roomtotal,$m_room,$m_chkxhost,$m_chkxcou);

opendir(DIR,"$logdir") || &err("���O�̃f�B���N�g�����J���܂���B");
	@readlist = grep(/dat/, readdir(DIR));
closedir(DIR);
$test = @readlist;
if($test >= $forbid) {
    &err("�������쐬���\�ɒB���܂���");
}
if(&is_banned_proxy()) {
    &err("���̃z�X�g����̔��쐬�͏o���܂���B�}�C�i�X���䗘�p�������BA<!-- b $proxycheck,$host,$hosta,$xhost -->");
}
if($ban_open_proxy && &is_open_proxy()) {
    &err("���̃z�X�g����̔��쐬�͏o���܂���B�}�C�i�X���䗘�p�������BB<!-- o $proxycheck,$host,$hosta,$xhost -->");
}

$m_chktimes = $times - 24*60*60;
$m_chkcou = $m_chkxcou = 0;

foreach $room (@readlist) {
	$room=~s/(.*)\.dat/$1/;
	open(DB, "./$logdir/$room.dat") || next;
		$m_set = <DB>;
	close(DB);
	($m_title2,$m_dmy,$m_ddata,$m_chkpwlhost,$m_chktm,$m_dmy,$m_dmy,$m_chkxhost) = split(/:#/,$m_set);
	$m_title2 =~ s/ //g;$m_title2 =~ s/�@//g;
	&err("���ɓ����^�C�g���̃A���P�[�g������܂��B") if($chktitle eq $m_title2);
	if( ($m_chkpwlhost eq $pwlhost) && ($m_chktm >= $m_chktimes) ){
	    	$m_chkcou++;
		if( $m_chkcou >= $hakosokudo ){
			&err("�����������ł��B<!-- $proxycheck,$host -->");
		}
	}
	if( ($m_chkxhost ne "") && ($m_chkxhost eq $xhost) 
	    && ($m_chktm >= $m_chktimes)) {
	    	$m_chkxcou++;
		if( ($xhost ne "") &&  ($m_chkxcou >= $xhakosokudo) ) {
		    # �R����p
		    &err("�����������ł��B<!-- x $proxycheck,$host -->");
		}
	}
}#foreach
$ddata = sprintf("%4.2f",$sday);
$m_set = "$title:#$vkey:#$ddata:#$pwlhost:#$times:#$chat:#$date:#$xhost:#:#\n";
open(DB,">./$logdir/$times.dat") || &err("���O�t�@�C�������܂���B");
	print DB $m_set;
close(DB);
chmod 0666, "./$logdir/$times.dat";

#�J�E���g�t�@�C�������
open(DB,">./$coudir/0.$times.dat") || return;
close(DB);
chmod 0666, "./$coudir/0.$times.dat";

#��̏����p�Ƀf�[�^���ڂ�
$room = $times;
$ochat = $chat;
$odate = $date;
$oxhost = $xhost;
undef @lines;

$m_roomtotal = @readlist;
if($m_roomtotal >= $lbox ){
	undef @roomlist;
	foreach $m_room (@readlist) {
		$m_room=~s/(.*)\.dat/$1/;
		open(DB, "./$logdir/$m_room.dat") || next;
			$m_set = <DB>;
		close(DB);
		($m_title2,$m_dmy,$m_ddata) = split(/:#/,$m_set);
		$m_filedata = -M "./$logdir/$m_room.dat";
		$ans{$m_room} = $m_ddata - $m_filedata;
		push(@roomlist,$m_room);
	}
	@roomlist = sort { $ans{$a} <=> $ans{$b} } @roomlist;
	foreach $m_room (@roomlist) {
		if($ans{$m_room} <= 0){
			&logdel($m_room);
			$m_roomtotal--;
		}else{
			last;
		}
		if( $m_roomtotal < $lbox ){
			last;
		}
	}
}

}#make END
##################################################
#�������ݑ��x�`�F�b�N
sub wspeed{
my($m_line,$m_eqtime,$m_eqrh,$m_chktime,$m_flag,$m_eqxh);

undef @new;
$m_chktime = $times - $wspeedtime*60;
$m_flag = 0;
open(DB,"+<./$wspeedfile") || return;
	eval 'flock(DB,2);';
	@lines = <DB>;
	foreach $m_line (@lines) {
		($m_eqtime,$m_eqrh,$m_eqxh) = split(/\,/,$m_line);
		if( $m_eqtime < $m_chktime ){
			next;
		}
		if( $pwhost eq $m_eqrh ){
			$m_flag += 1;
		}
		push(@new,$m_line);
	}
	if( &is_annonymous_proxy() && ($m_flag > $xwspeedcou) ) {
	    # ���������x�K��
	    &err("�������ݑ��x�ᔽ�ł��B<!-- x $m_flag,$proxycheck,$host -->");
	}
	if( $m_flag > $wspeedcou ){
		&err("�������ݑ��x�ᔽ�ł��B<!-- $m_flag,$proxycheck,$host -->");
	}
	$m_line = "$times\,$pwhost\,$xhost\n";
	push(@new,$m_line);
	seek(DB,0,0);	print DB @new;
	truncate(DB,tell(DB));
close(DB);
}#wspeed END
##################################################
#�g�s�l�k�̍č쐬
sub remakehtml {
my($m_set,$m_file,$m_hatu);

opendir(DIR,"$coudir") || &err("�J�E���^�f�B���N�g�����J���܂���B");
	@dellist = grep(/dat/, readdir(DIR));
closedir(DIR);
foreach (@dellist) {
	unlink "./$coudir/$_";
}#foreach

opendir(DIR,"$logdir")|| &err("���O�f�B���N�g�����J���܂���B");
	@readlist = grep(/dat/, readdir(DIR));
closedir(DIR);

foreach $room (@readlist) {
	$room=~s/(.*)\.dat/$1/;
	open(DB,"./$logdir/$room.dat") || next;
		@lines = <DB>;
	close(DB);
	$m_set=shift(@lines);
	($title,$vchkkey,$ddata,$opwhost,$otimes,$ochat,$odate) = split(/:#/,$m_set);
	if( $vkey eq $vchkkey ){
		$m_hatu = @lines;
		&resulthtml;
		$m_file = "./$coudir/$m_hatu.$room.dat";
		open(DB,">$m_file") || next;
		close(DB);
		chmod 0666, "$m_file";
	}else{
		&logdel($room);
	}
}#foreach
}#remakehtml END
##################################################
#���O�폜
sub deletevote {
my($m_dmy,$m_erase,$m_line,$m_dmy, $m_times,$m_set,$m_filedata,$m_pwhost,$m_mrev,$m_vote,$m_chat,$m_date);

&err("�p�X���[�h���Ⴂ�܂��B") if($root ne $masterkey);

open(DB,"+<./$logdir/$room.dat") || &err("���O�t�@�C�����J���܂���B");
	eval 'flock(DB,2);';
	@lines = <DB>;
	$m_set=shift(@lines);
	($title,$vchkkey,$ddata,$opwhost,$otimes,$ochat,$odate,$oxhost) = split(/:#/,$m_set);
	if( $vkey ne $vchkkey ){
		close(DB);
		&err("���O�t�@�C�������Ă��܂��B");
	}

	$buffer=~s/&//g;	#�]���ȕ������폜
	(@erase) = split(/erase=/, $buffer);	#�폜���X�g���쐬
	$m_dmy = shift( @erase);
	foreach $m_erase(@erase){
		$m_erase =~s/\D//g;
		foreach $m_line (@lines) {
			next unless($m_line=~/:#/);
			($m_pwhost,$m_times,$m_mrev,$m_vote,$m_chat,$m_date) = split(/:#/, $m_line);
			if( $m_times eq $m_erase ){
				$m_pwhost =~s/./\ /g;
				$m_vote =~s/./\ /g;
				$m_chat =~s/./\ /g;
				$m_line = "$m_pwhost:#$m_times:#$m_mrev:#$m_vote:#$m_chat:#$m_date:#:#\n";
				last;
			}
		}#foreach
	}#foreach
	$m_set = "$title:#$vchkkey:#$ddata:#$opwhost:#$otimes:#$ochat:#$odate:#$oxhost:#:#\n";
	$m_filedata = -M "./$logdir/$room.dat";
	seek(DB,0,0);	print DB $m_set; print DB @lines;
	truncate(DB,tell(DB));
close(DB);
$m_filedata = $times - ($m_filedata*24*60*60);
utime($times,$m_filedata,"./$logdir/$room.dat");

}#deletevote END
__END__
