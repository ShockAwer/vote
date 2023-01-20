#!/usr/bin/perl
#
#ゆいぼーと2.1(yuivote2.cgi)
#1997.10.10製作
#すくりぷと　ばい　ゆいちゃっと　
#箱作成速度違反です　　　　　　　　　Since  1996
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
if($detail){
	if(($delete eq 'on') && ($postf eq 'on')){
		&deletevote;
		&resulthtml;	#集計画面作成
		print "Location: $cgidir/$cginame2?detail=$detail&room=$room\n\n";
	}else{
		&readlog;
		&detailhtml;	#コメント集画面へ
	}
	exit;
}
if($allres eq 'on'){
	if(($delete eq 'on') && ($postf eq 'on')){
		&deletevote;
		&resulthtml;	#集計画面作成
		print "Location: $cgidir/$cginame2?allres=on&room=$room\n\n";
	}else{
		&readlog;
		&allreshtml;	#コメント集画面へ
	}
	exit;
}
if($postf ne 'on'){
	&err("不正な投稿です");
}
if( $title ne '' ){
	if( $title eq $masterkey ){
		&remakehtml;
		print "Location: $cgidir/$cginame1\n\n";
	}else{
		&wspeed;
		&make;
		&resulthtml;	#集計画面作成
		print "Location: $cgidir/$htmdir/$room.html\n\n";
	}
	exit;
}elsif($vote ne ''){
	&wspeed;
	&writelog;
	&resulthtml;	#集計画面作成
	print "Location: $cgidir/$htmdir/$room.html\n\n";
	exit;
}
&err("不正な投稿です");
exit;
##############################################################################
#初期設定など
sub init{
    &vote_config();
}#init END
##############################################################################
#入力変換
sub decode{

$title = $FORM{'title'};
if( $title ne '' ){
	&err("タイトルが長すぎます。") if(length($title) > ($namemax*2));
	$chktitle = $title;
	$chktitle =~ s/　//g;$chktitle =~ s/ //g;
	$title = '' if( $chktitle eq '' );
}
$vote=$FORM{'vote'};
$voten=$FORM{'voten'};
&err("投票の仕方を間違えています。") if( $voten ne '' && $vote ne '' );
$vote=$voten if( $vote eq '');
&err("項目名が長すぎます。") if(length($vote) > ($votemax*2) );
$chkvote = $vote;
$chkvote =~ s/　//g;$chkvote =~ s/ //g;
$vote = '' if( $chkvote eq '' );
$chat=$FORM{'chat'};
if(length($chat) > ($chatmax*2)){&err("コメントが長すぎます。");}
$_ = $chat;$brnum = s/ //ig;$brnum = s/　//ig;$brnum = s/<br>//ig;
if( ($_ eq '') && ( ($vote ne '') || ($title ne '') ) ){&err("コメントが書かれていません");}
if($brnum >= $brmax){&err("コメントの行数が多すぎます");}
$detail=$FORM{'detail'};
$room = $FORM{'room'};$room =~s/\D//g;$room = '000' if($room eq '');
$mrev = $FORM{'mr'};$mrev = 'on' if($mrev eq '');$mrev = 'off' if($mrev ne 'on');
$allres=$FORM{'allres'};
$root = $FORM{'root'};
$delete = $FORM{'delete'};

&ngCheck("！", $title, @titleNGwords);
&ngCheck("！", $vote, @voteNGwords);
&ngCheck("！", $voten, @votenNGwords);
&ngCheck("！", $chat, @chatNGwords);
sub ngCheck() {
    my($msg, $target) = @_;
    $target =~ s/ //g;
    $target =~ s/　//g;
    shift(@_);
    shift(@_);
    foreach(@_){
	&err($msg) if( $target =~ /\Q$_\E/ );
    }
}

}#decode END
##############################################################################
#配列@linesにログを読み込む
sub readlog{
my($m_set);

open(DB,"./$logdir/$room.dat") || &err("ログファイルが開けません。");
	@lines = <DB>;
close(DB);
$m_set=shift(@lines);
($title,$vchkkey,$ddata,$opwhost,$otimes,$ochat,$odate,$oxhost) = split(/:#/,$m_set);
if( $vkey ne $vchkkey ){ &err("ログファイルが壊れています。"); }
}#readlog END
##############################################################################
#チェックしつつ書き込む
sub writelog{	
my($m_set,$m_chktime,$m_line,$m_kpwhost,$m_dmy,$m_ktimes,$m_krev,$m_kvote,$m_chkday,$m_kchat,$m_chkchat,$m_hatu,$m_room);

open(DB,"+<./$logdir/$room.dat") || &err("ログファイルが開けません。");
	eval 'flock(DB,2);';
	@lines = <DB>;
	$m_set=shift(@lines);
	($title,$vchkkey,$ddata,$opwhost,$otimes,$ochat,$odate,$oxhost) = split(/:#/,$m_set);
	if( $vkey ne $vchkkey ){
		close(DB);
		&err("ログファイルが壊れています。");
	}

	$m_hatu = @lines;
	if($m_hatu >= $max){
		close(DB);
		&err("投票箱がいっぱいになりました。");
	}
	$m_chktime = $times - 30*60;
	if( 'on' ne $mrev ){
		$m_chkchat = $chat;$m_chkchat =~ s/　//g;$m_chkchat =~ s/ //g;$m_chkchat =~ s/<br>//ig;
	}
	@lines = reverse (@lines);
	foreach $m_line (@lines) {	#一人組織票を抑制
		($m_kpwhost, $m_ktimes, $m_krev, $m_kvote,$m_kchat) = split(/:#/, $m_line);
		if( $m_ktimes < $m_chktime ){ last; }
		if( $m_kpwhost eq $pwhost ){
			$m_kvote =~ s/　//g;$m_kvote =~ s/ //g;
			if( 'on' eq $mrev ){
				if( $chkvote eq $m_kvote ){
					close(DB);
					&err("一人組織票抑制機能\に引っかかりました。");
				}
			}else{
				if( $chkvote eq $m_kvote ){ #2002/12/03 変数名が間違っていた
					$m_kchat =~ s/　//g;$m_kchat =~ s/ //g;$m_kchat =~ s/<br>//ig;
					if( $m_kchat eq $m_chkchat){
						close(DB);
						&err("二重書き込み禁止機能\に引っかかりました。");
					}else{
						last;
					}
				}
			}
		}
	}
#新規投票は、加える
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
#投票結果画面
sub resulthtml{
my($m_hatu,$m_total,$m_line,$m_dmy1,$m_wtimes,$m_wrev,$m_wvote,$m_wcvote,$m_percent,$m_img,$m_count,$m_wdetail,$m_wpwhost,$m_wdate,$m_comtimes,$m_ranka,$m_rankb,$m_rankc,$m_hatu);

open(DB,">./$tmpdir/$room.$times.$pwhost") || &err("テンポラリファイルが開けません");

print DB <<"_HTML_";
<HTML><HEAD>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
$metacode
<TITLE>$title </TITLE><STYLE><!--.linka{text-decoration : none;color : #A1FE9F;vertical-align : baseline;}
--></STYLE></HEAD>
$body
[<A HREF="../$cginame1">リストに戻る</A>] [<A href="#now">最近の投票</A>]<FONT COLOR="red"><B> ※　ニュースサイトからの投票で大変迷惑しています。投票箱へのリンクはご遠慮ください。</B></FONT><BR><BR>
<FONT SIZE=+2 COLOR="hotpink"><B>${title} </B></FONT>
<BR><BR>
<DIV ALIGN=right>($odate)</DIV><BR>
<HR><PRE><FONT SIZE=3>$ochat </FONT></PRE>
<HR>現在のアンケート集計結果は以下のとおりです。<BR>
それぞれの選択項目をクリックするとコメントをみることができます。（古い投票順になっています。）<BR>
<TABLE border WIDTH=100%>
<TR><TH NOWRAP>順位</TH><TH NOWRAP>選択項目</TH><TH NOWRAP>有効票数（投票数）</TH><TH NOWRAP>割合</TH><TH>グラフ</TH></TR>
_HTML_

$m_hatu = @lines;
$m_total = 0;undef %votes;undef %alvotes;undef @oplist;
foreach $m_line (@lines) {
	next unless($m_line=~/:#/);
	($m_dmy, $m_dmy2, $m_wrev, $m_wvote) = split(/:#/, $m_line);
	$m_dmy =~s/\*//g;
	next if( $m_dmy eq "");
	$m_wcvote = $m_wvote;
	$m_wcvote =~ s/ //g;$m_wcvote =~ s/　//g;
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
<B>有効投票総数$m_total票（投票総数$m_hatu票）</B><BR><P>
<HR><A name="now">最近の投票</A>（過去$comtime時間前、または$commax投票）　
<A HREF=\"\.\.\/$cginame2?allres=on&room=$room\">全投票表\示</A><BR>
_HTML_

}else{

print  DB <<"_HTML_";
</TABLE>
<B>有効投票総数$m_total票（投票総数$m_hatu票）</B><BR><P>
<FORM METHOD="POST" ACTION="../$cginame2">
<INPUT TYPE=hidden NAME="room" VALUE="$room">
<SELECT NAME="vote" SIZE="1">
<OPTION VALUE="0" SELECTED>選択してね。
_HTML_

foreach (@oplist) {
	print DB "<OPTION>$_\n";
}#foreach

print DB <<"_HTML_";
</SELECT><BR>
項目を追加する場合→<INPUT TYPE=text NAME=\"voten\" SIZE=\"60\">全角${votemax}文字まで<BR>
<BR>上記項目を選択した理由を簡単にお書き下さい。（必須）（タグは使えません。）<BR>
<TEXTAREA NAME="chat" rows="10" cols="80"></TEXTAREA><BR>
（${brmax}行、${chatmax}文字まで）<BR>
<input type="radio" name="mr" value="on">有効票<input type="radio" name="mr" value="off" checked><FONT COLOR=\"#0000FF\">無効票（意見のみ）</FONT><BR>
<BR>
<INPUT TYPE=submit VALUE="投票する"><FONT size="-1" COLOR="red"> <A href="http://www.zianplus.net/guideline.txt">利用規約</A>を読み、規約に完全に同意してから送信してください。</FONT>
<INPUT TYPE=reset VALUE="リセット"></FORM>
<HR><A name="now">最近の投票</A>（過去$comtime時間前、または$commax投票）　
<A HREF=\"\.\.\/$cginame2?allres=on&room=$room\">全投票表\示</A><BR>
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
<noscript><FONT SIZE=1 COLOR="red">このページではJavaScriptを使用しています。</FONT></noscript>
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
print DB "[<A HREF=\"../$cginame1\">リストに戻る</A>]<BR>\n";
print DB "$maruc\n";
print DB "</BODY></HTML>\n";
close(DB);

unlink "./$htmdir/$room.html";
rename("./$tmpdir/$room.$times.$pwhost","./$htmdir/$room.html");
unlink "./$tmpdir/$room.$times.$pwhost";	#念の為
chmod 0666, "./$htmdir/$room.html";

}#resulthtml END
##############################################################################
#コメント画面
sub detailhtml {
my($m_keyword,$m_line,$m_dmy,$m_times,$m_wrev,$m_wvote,$m_wdetail,$m_wdate);

print "Content-type: text/html; charset=Shift_JIS\n\n";
print <<"_HTML_";
<HTML><HEAD>
$metacode
<TITLE>$title </TITLE></HEAD>
$body
[<A HREF="./$htmdir/$room.html">投票結果に戻る</A>]<A name="ue">&nbsp;</A><A href="#sita">▽</A><BR><BR>
[${detail}]についてのコメント。<BR>
<HR SIZE=5>
<noscript><FONT SIZE=+5 COLOR="red">このページではJavaScriptを使用しています。(たまにシャッフルしますね)</FONT></noscript>
_HTML_

$m_keyword = $detail;
$m_keyword =~ s/ //g;$m_keyword =~ s/　//g;

print "<FORM method=\"POST\" ACTION=\"./$cginame2\">\n" if($root eq $masterkey);

$m_hatu = @lines;
foreach $m_line (@lines) {
	next unless($m_line=~/:#/);
	($m_dmy, $m_times, $m_wrev, $m_wvote, $m_wchat,$m_wdate) = split(/:#/, $m_line);
	$m_wvote =~ s/ //g;$m_wvote =~ s/　//g;
	if($m_wvote eq $m_keyword ){
		print "<INPUT TYPE=checkbox NAME=\"erase\" VALUE=\"$m_times\">\n" if($root eq $masterkey);
		if($m_wrev eq 'on'){
			print "<BR><PRE><FONT SIZE=3>$m_wchat </FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)</FONT><HR>\n";
		}else{
			print "<BR><FONT COLOR=\"#0000FF\"><PRE><FONT SIZE=3>$m_wchat </FONT></FONT></PRE><FONT COLOR=\"#888888\" SIZE=-1>($m_wdate)</FONT><HR>\n";
		}
	}
}#foreach
print qq!<INPUT TYPE=hidden NAME="erase" VALUE="dummy" ><INPUT TYPE=hidden NAME="delete" VALUE="on"><INPUT TYPE=hidden NAME="detail" VALUE="$detail" ><INPUT TYPE=hidden NAME="room" VALUE="$room" ><INPUT TYPE=hidden NAME="root" VALUE="$root" ><INPUT type=submit value="削除"></FORM>\n! if($root eq $masterkey);

if($m_hatu >= $max){

print   <<"_HTML_";
[<A HREF=\"./$htmdir/$room.html\">投票結果に戻る</A>]<BR>
<H5 align=right><FORM method="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="detail" VALUE="$detail" >
<INPUT TYPE=hidden NAME="room" VALUE="$room" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="管理"><BR>
$maruc
</BODY></HTML>
_HTML_

}else{

print   <<"_HTML_";
<B>${title}</B><BR>項目[${detail}]
<FORM METHOD="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="room" VALUE="$room">
<INPUT TYPE=hidden NAME="vote" VALUE="$detail">
この項目に投票する場合、投票の理由を簡単にお書き下さい。（必須）（タグは使えません。）<BR>
<TEXTAREA NAME="chat" rows="10" cols="80"></TEXTAREA><BR>
（${brmax}行、${chatmax}文字まで）<BR>
<input type="radio" name="mr" value="on">有効票<input type="radio" name="mr" value="off" checked><FONT COLOR=\"#0000FF\">無効票（意見のみ）</FONT><BR>
<BR>
<INPUT TYPE=submit VALUE="投票する"><FONT size="-1" COLOR="red"><A href="http://www.zianplus.net/guideline.txt">利用規約</A>を読み、規約に完全に同意してから送信してください。</FONT>
<INPUT TYPE=reset VALUE="リセット"></FORM>
（一人組織票抑制機能\が付いています。）<HR>
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
[<A HREF=\"./$htmdir/$room.html\">投票結果に戻る</A>]<A name="sita">&nbsp;</A><A href="#ue">△</A><BR>
<H5 align=right><FORM method="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="detail" VALUE="$detail" >
<INPUT TYPE=hidden NAME="room" VALUE="$room" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="管理"><BR>
$maruc
</BODY></HTML>
_HTML_

}#if

}#detailhtml END
##############################################################################
#全コメント画面
sub allreshtml {
my($m_line,$m_dmy,$m_times,$m_wrev,$m_wvote,$m_wdate,$m_hatu);

$m_hatu = @lines;
print "Content-type: text/html; charset=Shift_JIS\n\n";
print <<"_HTML_";
<HTML><HEAD>
$metacode
<TITLE>$title </TITLE></HEAD>
$body
[<A HREF="./$htmdir/$room.html">投票結果に戻る</A>]<A name="ue">&nbsp;</A><A href="#sita">▽</A><BR><BR>
<B>$title</B>の投票総数 $m_hatu票<BR>
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
print qq!<INPUT TYPE=hidden NAME="erase" VALUE="dummy" ><INPUT TYPE=hidden NAME="delete" VALUE="on"><INPUT TYPE=hidden NAME="allres" VALUE="$allres" ><INPUT TYPE=hidden NAME="room" VALUE="$room" ><INPUT TYPE=hidden NAME="root" VALUE="$root" ><INPUT type=submit value="削除"></FORM>\n! if($root eq $masterkey);

print <<"_HTML_";
[<A HREF=\"./$htmdir/$room.html\">投票結果に戻る</A>]<A name="sita">&nbsp;</A><A href="#ue">△</A><BR>
<H5 align=right><FORM method="POST" ACTION="./$cginame2">
<INPUT TYPE=hidden NAME="allres" VALUE="$allres" >
<INPUT TYPE=hidden NAME="room" VALUE="$room" >
<INPUT TYPE=text NAME="root" SIZE="10" VALUE="$root">
<INPUT type=submit value="管理"><BR>
$maruc
</BODY></HTML>
_HTML_
}#allreslhtml END
##############################################################################
#ＵＲＬ用変換
sub URLEncoder {
$encode = $_[0];
$encode =~ s/([^0-9A-Za-z_ ])/"%".unpack("H2",$1)/ge;
$encode =~ tr/ /+/;
}
##################################################
#新規話題ルームを設置
sub make {
my($m_set,$m_title2,$m_dmy,$m_ddata,$m_chkpwlhost,$m_chktimes,$m_chkcou,$m_chktm,$m_roomtotal,$m_room,$m_chkxhost,$m_chkxcou);

opendir(DIR,"$logdir") || &err("ログのディレクトリが開けません。");
	@readlist = grep(/dat/, readdir(DIR));
closedir(DIR);
$test = @readlist;
if($test >= $forbid) {
    &err("箱数が作成上限\に達しました");
}
if(&is_banned_proxy()) {
    &err("そのホストからの箱作成は出来ません。マイナスを御利用下さい。A<!-- b $proxycheck,$host,$hosta,$xhost -->");
}
if($ban_open_proxy && &is_open_proxy()) {
    &err("そのホストからの箱作成は出来ません。マイナスを御利用下さい。B<!-- o $proxycheck,$host,$hosta,$xhost -->");
}

$m_chktimes = $times - 24*60*60;
$m_chkcou = $m_chkxcou = 0;

foreach $room (@readlist) {
	$room=~s/(.*)\.dat/$1/;
	open(DB, "./$logdir/$room.dat") || next;
		$m_set = <DB>;
	close(DB);
	($m_title2,$m_dmy,$m_ddata,$m_chkpwlhost,$m_chktm,$m_dmy,$m_dmy,$m_chkxhost) = split(/:#/,$m_set);
	$m_title2 =~ s/ //g;$m_title2 =~ s/　//g;
	&err("既に同じタイトルのアンケートがあります。") if($chktitle eq $m_title2);
	if( ($m_chkpwlhost eq $pwlhost) && ($m_chktm >= $m_chktimes) ){
	    	$m_chkcou++;
		if( $m_chkcou >= $hakosokudo ){
			&err("箱が多すぎです。<!-- $proxycheck,$host -->");
		}
	}
	if( ($m_chkxhost ne "") && ($m_chkxhost eq $xhost) 
	    && ($m_chktm >= $m_chktimes)) {
	    	$m_chkxcou++;
		if( ($xhost ne "") &&  ($m_chkxcou >= $xhakosokudo) ) {
		    # 漏れ串用
		    &err("箱が多すぎです。<!-- x $proxycheck,$host -->");
		}
	}
}#foreach
$ddata = sprintf("%4.2f",$sday);
$m_set = "$title:#$vkey:#$ddata:#$pwlhost:#$times:#$chat:#$date:#$xhost:#:#\n";
open(DB,">./$logdir/$times.dat") || &err("ログファイルが作れません。");
	print DB $m_set;
close(DB);
chmod 0666, "./$logdir/$times.dat";

#カウントファイルを作る
open(DB,">./$coudir/0.$times.dat") || return;
close(DB);
chmod 0666, "./$coudir/0.$times.dat";

#後の処理用にデータを移す
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
#書き込み速度チェック
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
	    # 匿名串速度規制
	    &err("書き込み速度違反です。<!-- x $m_flag,$proxycheck,$host -->");
	}
	if( $m_flag > $wspeedcou ){
		&err("書き込み速度違反です。<!-- $m_flag,$proxycheck,$host -->");
	}
	$m_line = "$times\,$pwhost\,$xhost\n";
	push(@new,$m_line);
	seek(DB,0,0);	print DB @new;
	truncate(DB,tell(DB));
close(DB);
}#wspeed END
##################################################
#ＨＴＭＬの再作成
sub remakehtml {
my($m_set,$m_file,$m_hatu);

opendir(DIR,"$coudir") || &err("カウンタディレクトリが開けません。");
	@dellist = grep(/dat/, readdir(DIR));
closedir(DIR);
foreach (@dellist) {
	unlink "./$coudir/$_";
}#foreach

opendir(DIR,"$logdir")|| &err("ログディレクトリが開けません。");
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
#ログ削除
sub deletevote {
my($m_dmy,$m_erase,$m_line,$m_dmy, $m_times,$m_set,$m_filedata,$m_pwhost,$m_mrev,$m_vote,$m_chat,$m_date);

&err("パスワードが違います。") if($root ne $masterkey);

open(DB,"+<./$logdir/$room.dat") || &err("ログファイルが開けません。");
	eval 'flock(DB,2);';
	@lines = <DB>;
	$m_set=shift(@lines);
	($title,$vchkkey,$ddata,$opwhost,$otimes,$ochat,$odate,$oxhost) = split(/:#/,$m_set);
	if( $vkey ne $vchkkey ){
		close(DB);
		&err("ログファイルが壊れています。");
	}

	$buffer=~s/&//g;	#余分な部分を削除
	(@erase) = split(/erase=/, $buffer);	#削除リストを作成
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
