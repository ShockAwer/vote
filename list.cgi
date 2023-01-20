#!/usr/bin/perl
#
#ゆいぼーど2.001(list.cgi)
#※このcgiはsnogの製作したvote4を改良した物です
#※許可が取れる作者が少ない為、とりあえず二次配布と使用は不可になってます

require './jcodeLE.pl';
require './prei.cgi';

$| = 1;
&winit;
&init;
&wdecode;
&decode;
&jikan;
if(($delete eq 'on') && ($postf eq 'on')){
	&deletelog;
	print "Location: $cgidir/$cginame1?page=$m_i&h=$hotlist&r=$rev&lm=$lmax&chg=$chg\n\n";
}else{
	&html;
}
exit;
##################################################
#初期設定
sub init{
$limax=100;				#１ページに表示するリスト標準数
}#init END
##################################################
#ページ作成
sub html {
my ( @list );
open( IN, "list.txt" );
while ( <IN> ) {
    push ( @list, $_ );
}
close( IN );
$message = $list[int(rand(scalar(@list)))];
print "Content-type: text/html; charset=Shift_JIS\n\n";
print <<"_HTML_";
<HTML><HEAD>
$metacode
<meta http-equiv="adalign" content="right">
<meta http-equiv="adimage" content="5">
<TITLE>$orititle</TITLE>
<style type="text/css"> 
<!-- 
.rss-items {
    margin: 3px 0 20px;
    _font-size: x-small;
}
--> 
</style>
</HEAD>
$body
<FONT size=+2><B>$orititle</B></FONT>
<HR>
<FONT size="-1">
<script src="http://feed2js.org//feed2js.php?src=http%3A%2F%2Fa.hatena.ne.jp%2Fnatori%2Frss&amp;num=5&amp;desc=500&amp;targ=y&amp;utf=y" type="text/javascript" charset="utf-8"></script>
<noscript><a href="http://feed2js.org//feed2js.php?src=http%3A%2F%2Fa.hatena.ne.jp%2Fnatori%2Frss&amp;num=5&amp;desc=500&amp;targ=y&amp;utf=y&amp;html=y">rss</a></noscript>
</FONT>
<FONT size="-1">[<A href="#make">New Box Creation＿</A>][<A href="http://www.zianplus.net">Index</A>][<A href="http://www.zianplus.net/mail.htm">Admin</A>][<A href="http://www.zianplus.net/cgi-bin/php/zianchat.cgi">(Internet) chat</A>][<A href="http://www.zianplus.net/cgi-bin/vote-/list.cgi">Automatic Questionnaire-</A>][<A href="http://www.zianplus.net/guideline.txt">Terms of Use</A>]</FONT><FONT size="-1">[<A href="http://d.hatena.ne.jp/natori/">#A1FE9F</A>][<A href="http://ee.uuhp.com/~shi946/">Scoring</A>][<A href="http://www.zianplus.net/cgi-bin/e/bbsnote.cgi">Drawing</A>]</FONT>
<FORM method="GET" ACTION="./$cginame1"><FONT size="-1"><INPUT TYPE=text NAME="lm" SIZE="3" VALUE="$lmax"> Subject table <INPUT TYPE=text NAME="h" SIZE="3" VALUE="0">Boxes updated within days</FONT><FONT size="-1"><input type="radio" name="r" value="0" checked>Creation-order<input type="radio" name="r" value="1" >Order of votes<input type="radio" name="r" value="2" >By (order of) votes</FONT>
<FONT size="-1"><input type="checkbox" name="chg" value="on">Context table　</FONT><FONT size="-1"><INPUT type="submit" value="Setting"></FONT></FORM>
<UL>
<li>${date}Current list of ballot boxes
<li>The date and time are the last time the file was written.
<li>Clicking on the first ◇ at the top will open a new browser.
_HTML_
	&listing;#リスト作成
if($test >= $forbid){
print <<"_HTML_";
</UL>
The maximum number of boxes has been reached and new topics cannot be posted.
<p>
<HR>
<FORM method="GET" ACTION="./$cginame1">
<FONT size="-1"><INPUT TYPE=text NAME="lm" SIZE="3" VALUE="$lmax"> Subject table <INPUT TYPE=text NAME="h" SIZE="3" VALUE="0">Boxes updated within days</FONT>
<FONT size="-1"><input type="radio" name="r" value="0" checked>Creation-order<input type="radio" name="r" value="1" >Order of votes<input type="radio" name="r" value="2" >By (order of) votes</FONT>
<FONT size="-1"><input type="checkbox" name="chg" value="on">Content table　</FONT><FONT size="-1"><INPUT type="submit" value="Setting"></FONT></FORM><HR>
<H5 align=right><FORM method="POST" ACTION="./$cginame1">
<INPUT TYPE=hidden NAME="page" VALUE="$page" >
<INPUT TYPE=hidden NAME="h" VALUE="$hotlist" >
<INPUT TYPE=hidden NAME="r" VALUE="$rev" >
<INPUT TYPE=hidden NAME="lm" VALUE="$lmax" >
<INPUT TYPE=hidden NAME="chg" VALUE="$chg" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="Control"><BR>
$maruc
</BODY></HTML>
_HTML_
}else{
print <<"_HTML_";
</UL>
<FORM method="POST" ACTION="./$cginame2">
タイトル：<INPUT TYPE=text NAME="title" SIZE="60">（全角${namemax}文字まで）<BR>
内容:<TEXTAREA NAME="chat" rows="10" cols="80"></TEXTAREA><BR>
　　　（${brmax}行、${chatmax}文字まで）（必須）<BR>
<INPUT type=submit value="This is fine."><FONT size="-1" COLOR="red"> <A href="http://www.zianplus.net/guideline.txt">利用規約</A>を読み、規約に完全に同意してから送信してください。</FONT>
<INPUT TYPE=reset VALUE="Reset">
</FORM>
<p>
<HR>
<FORM method="GET" ACTION="./$cginame1">
<FONT size="-1"><INPUT TYPE=text NAME="lm" SIZE="3" VALUE="$lmax"> 件表\示 <INPUT TYPE=text NAME="h" SIZE="3" VALUE="0">日以内に更新した箱</FONT>
<FONT size="-1"><input type="radio" name="r" value="0" checked>作成順<input type="radio" name="r" value="1" >投票順<input type="radio" name="r" value="2" >票数順</FONT>
<FONT size="-1"><input type="checkbox" name="chg" value="on">内容文表\示　</FONT><FONT size="-1"><INPUT type="submit" value="設定"></FONT></FORM><HR>
<H5 align=right><FORM method="POST" ACTION="./$cginame1">
<INPUT TYPE=hidden NAME="page" VALUE="$page" >
<INPUT TYPE=hidden NAME="h" VALUE="$hotlist" >
<INPUT TYPE=hidden NAME="r" VALUE="$rev" >
<INPUT TYPE=hidden NAME="lm" VALUE="$lmax" >
<INPUT TYPE=hidden NAME="chg" VALUE="$chg" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="管理"><BR>
$maruc
</BODY></HTML>
_HTML_
}
}#html END
##################################################
#箱のリストデータを作る
sub listing{
my($m_room,$m_filedata,$m_roomtotal,$m_count,$m_i,$m_set,$m_title,$m_chkkey,$m_ddata,$m_datedata,$m_sec,$m_min,$m_hour,$m_mday,$m_month,$m_year,$m_wday,$m_yday,$m_isdst,$m_dmy1,$m_dmy2,$m_schat,$m_hatu,$m_rnum,$m_dates);

opendir(DIR,"$coudir") || return;
	@readlist = grep(/dat/, readdir(DIR));
closedir(DIR);

foreach $m_room (@readlist) {
	($m_hatu,$m_rnum) = split(/\./,$m_room);
	$ans2{$m_rnum} = $m_hatu;
}#foreach

opendir(DIR,"$logdir") || return;
	@readlist = grep(/dat/, readdir(DIR));
closedir(DIR);

foreach $m_room (@readlist) {
	$m_filedata = -M "./$logdir/$m_room";
	$m_room=~s/(.*)\.dat/$1/;
	if($hotlist){#更新日付がhotlist以内のものをピックアップ
		push(@roomlist,$m_room) if ($m_filedata < $hotlist);
	}else{
		push(@roomlist,$m_room);
	}
	$ans{$m_room} = $m_filedata;
}#foreach
if( $rev eq '1'){
	@roomlist = sort { $ans{$a} <=> $ans{$b} } @roomlist;
}elsif($rev eq '2'){
	@roomlist = sort { $ans2{$a} <=> $ans2{$b} } @roomlist;
	@roomlist = reverse (@roomlist);
}else{
	@roomlist = sort { $a <=> $b; } @roomlist;
	@roomlist = reverse (@roomlist);
}

$m_roomtotal = @roomlist;
$test = @roomlist;
print "<LI>現在の投票箱数<FONT SIZE=+2><B>$m_roomtotal</B></FONT>箱\n";
print "<P><LI>Page:\n";
$m_count = int(($m_roomtotal-1)/$lmax);
for($m_i=0;$m_i<=$m_count;$m_i++){
	if($m_i eq $page){
		print "[<b>$m_i</b>] \n";
	}else{
		print "[<A HREF=\"./$cginame1?page=$m_i&h=$hotlist&r=$rev&lm=$lmax&chg=$chg\">$m_i</A>] \n";
	}
}#for
print "<FORM method=\"POST\" ACTION=\"./$cginame1\">\n" if($root eq $masterkey);
print "<DL>\n";
print "実行したいコマンドにチェックを入れて実行ボタンを押してください。<br>\n" if($root eq $masterkey);
print "移動と削除両方にチェックを入れた場合、移動が優先されます。<br>\n<br>\n" if($root eq $masterkey);
(@roomlist < $lmax) || (@roomlist = @roomlist[$page2 .. $page2+$lmax-1]);

foreach $m_room (@roomlist) {
	open(DB, "./$logdir/$m_room.dat") || next;
		$m_set = <DB>;
	close(DB);
	($m_title,$m_chkkey,$m_ddata,$m_dmy1,$m_dmy2,$m_schat,$m_dates) = split(/:#/,$m_set);
	$m_title = unpack("A60",$m_title);
	if( $vkey ne $m_chkkey){
		&logdel($m_room);next;	#ログが壊れている
	}
	$m_filedata = $ans{$m_room};
	$m_datedata = $m_ddata - $m_filedata;

	($m_sec,$m_min,$m_hour,$m_mday,$m_month,$m_year,$m_wday,$m_yday,$m_isdst) = localtime($times-$m_filedata*24*60*60);
	$m_month++;
	if($m_datedata < 1){
			$m_dates = sprintf("<FONT COLOR=\"red\"> %d/%02d %02d時%02d分<\/FONT>",$m_month,$m_mday,$m_hour,$m_min);
	}else{
		if($m_filedata < 0.5 ){
			$m_dates = sprintf("<FONT COLOR=\"blue\"> %d/%02d %02d時%02d分<\/FONT>",$m_month,$m_mday,$m_hour,$m_min);
		}else{
			$m_dates = sprintf(" %d/%02d %02d時%02d分",$m_month,$m_mday,$m_hour,$m_min);
		}
	}
	$m_ddata = sprintf("%4.2f",$m_ddata);
	print "<DT>\n";
	print "移<INPUT TYPE=checkbox NAME=\"erase\" VALUE=\"$m_room\move\">\n" if($root eq $masterkey);
	print "削<INPUT TYPE=checkbox NAME=\"erase\" VALUE=\"$m_room\">\n" if($root eq $masterkey);
	print "<FONT size=5><A HREF=\"./$htmdir/$m_room.html\" target=\"_blank\">◇</A></FONT>　\n";
	print "<FONT size=5><A HREF=\"./$htmdir/$m_room.html\">$m_title </A></FONT><FONT size=2>:$m_dates: $ans2{$m_room}投票<BR></FONT>\n";
	if($chg eq 'on'){
		print "$m_schat\n";
	}
}#foreach
print "</DL>\n";
print qq!<INPUT TYPE=hidden NAME="erase" VALUE="dummy" ><INPUT TYPE=hidden NAME="delete" VALUE="on"><INPUT TYPE=hidden NAME="page" VALUE="$page" ><INPUT TYPE=hidden NAME="h" VALUE="$hotlist" ><INPUT TYPE=hidden NAME="r" VALUE="$rev" ><INPUT TYPE=hidden NAME="lm" VALUE="$lmax" ><INPUT TYPE=hidden NAME="chg" VALUE="$chg" ><INPUT TYPE=hidden NAME="root" VALUE="$root" ><INPUT type=submit value="実行"></FORM>\n! if($root eq $masterkey);

print "</OL><P><LI>Page:\n";
for($m_i=0;$m_i<=$m_count;$m_i++){
	if($m_i eq $page){
		print "[<b>$m_i</b>] \n";
	}else{
		print "[<A HREF=\"./$cginame1?page=$m_i&h=$hotlist&r=$rev&lm=$lmax&chg=$chg\">$m_i</A>] \n";
	}
}#for

}#listing END

##################################################
#入力変換
sub decode {
$hotlist = $FORM{'h'};$hotlist = '0' if($hotlist eq '');
$chg = $FORM{'chg'};
$lmax = $FORM{'lm'};$lmax = $limax if($lmax < 1);$lmax = int($lmax);
$page = $FORM{'page'};$page = int($page);$page = 0 if($page < 0);
$page2 = $page*$lmax;
$rev = $FORM{'r'};$rev = '0' if($rev eq '');
$root = $FORM{'root'};
$delete = $FORM{'delete'};
}#decode END
##################################################
#ログ削除
sub deletelog {
my($m_dmy,$m_erase);
&err("パスワードが違います。") if($root ne $masterkey);
$buffer =~ s/&//g;	#余分な部分を削除
(@erase) = split(/erase=/, $buffer);	#削除リストを作成
$m_dmy = shift( @erase);
foreach $m_erase(@erase){
	if($m_erase =~ s/move//){
		$m_erase =~ s/\D//g;
		$m_move = "move";
	}else{
		$m_erase =~ s/\D//g;
		$m_move = "";
	}
	if(-e "./$logdir/$m_erase.dat"){
		&logdel($m_erase);
	}
}#foreach
}#deletelog END

__END__

##################################################
