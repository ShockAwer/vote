#!/usr/bin/perl
#
#※このcgiはsnogの製作したvote4を改良した物です
#※許可が取れる作者が少ない為、とりあえず二次配布と使用は不可になってます
#prei.cgiは、共通して使われるサブルーチン集です。
#ログデータフォーマット
#
#$title:#$vkey:#$ddata:#$pwlhost:#$times:#$chat:#$date:#$pwxhost:#:#
#$pwhost:#$times:#$mrev:#$vote:#$chat:#$date:#:#
##############################################################################
#初期設定など
use Socket;

require './config.cgi'; # 設定読み込み

sub winit{
my($m_h1,$m_h2,$m_h3,$m_h4,$m_ph1,$m_ph2,$m_ph3,$m_ph4,$m_ph5,$m_ph6,$m_ph7,$m_ph8,$m_wh1,$m_wh2);

&global_config();

$host = $ENV{'REMOTE_HOST'};

$hosta = '';	#初期化
$xhost = ''; ## 串アドレス
$proxycheck = 0;	#プロキシフラグ初期化
$hosta=$ENV{'HTTP_VIA'} if( $ENV{'HTTP_VIA'}=~s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_X_FORWARDED_FOR'} if( $ENV{'HTTP_X_FORWARDED_FOR'}=~s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_FORWARDED'} if( $ENV{'HTTP_FORWARDED'}=~s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_CLIENT_IP'} if( $ENV{'HTTP_CLIENT_IP'} =~s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_SP_HOST'} if( $ENV{'HTTP_SP_HOST'} =~s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
if( $hosta eq '' ){		#漏れ串じゃない
	$hosta=$ENV{'REMOTE_ADDR'};			#実ＩＰアドレス
	$proxycheck = &proxy_status();
}else{
    	$xhost = $ENV{'REMOTE_ADDR'};
	$proxycheck = 1; #漏れ串
}
($m_h1,$m_h2,$m_h3,$m_h4) = split(/\./,$hosta);		#ＩＰの暗号化（面倒くさいので一律同じ数値に）
$m_wh1 = int($m_h1/16);$m_wh2 = $m_h1%16;
$m_ph1 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh1%16];
$m_ph2 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh2];
$m_wh1 = int($m_h2/16);$m_wh2 = $m_h2%16;
$m_ph3 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh1%16];
$m_ph4 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh2];
$m_wh1 = int($m_h3/16);$m_wh2 = $m_h3%16;
$m_ph5 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh1%16];
$m_ph6 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh2];
$m_wh1 = int($m_h4/16);$m_wh2 = $m_h4%16;
$m_ph7 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh1%16];
$m_ph8 = ('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') [$m_wh2];
$pwlhost="$m_ph1$m_ph2$m_ph3$m_ph4$m_ph5$m_ph6$m_ph7$m_ph8";
$pwhost="$m_ph1$m_ph2$m_ph3$m_ph4$m_ph5$m_ph6$m_ph7$m_ph8";
$orititle='自動アンケート+';	#タイトル
$body = '<BODY BGCOLOR="#A1FE9F" TEXT="#000000" LINK="#0000ff" VLINK="#ff0000">
';	#標準表示設定
$metacode = '<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">';	#文字コード指定
$maruc = '<H5 ALIGN=right>オリジナルは<A HREF="http://www.cup.com/yui/index.html">ゆいぼーど＆ゆいぼーと</A></H5>';	#著作権表示

#半角を全角に変換するテーブル
%h2z = qw(
ｱ ア ｲ イ ｳ ウ ｴ エ ｵ オ
ｶ カ ｷ キ ｸ ク ｹ ケ ｺ コ
ｻ サ ｼ シ ｽ ス ｾ セ ｿ ソ
ﾀ タ ﾁ チ ﾂ ツ ﾃ テ ﾄ ト
ﾅ ナ ﾆ ニ ﾇ ヌ ﾈ ネ ﾉ ノ
ﾊ ハ ﾋ ヒ ﾌ フ ﾍ ヘ ﾎ ホ
ﾏ マ ﾐ ミ ﾑ ム ﾒ メ ﾓ モ
ﾔ ヤ ﾕ ユ ﾖ ヨ
ﾗ ラ ﾘ リ ﾙ ル ﾚ レ ﾛ ロ
ﾜ ワ ｦ ヲ ﾝ ン
ｯ ッ ｰ ー
ｬ ャ ｭ ュ ｮ ョ
ｧ ァ ｨ ィ ｩ ゥ ｪ ェ ｫ ォ
ｶﾞ ガ ｷﾞ ギ ｸﾞ グ ｹﾞ ゲ ｺﾞ ゴ
ｻﾞ ザ ｼﾞ ジ ｽﾞ ズ ｾﾞ ゼ ｿﾞ ゾ
ﾀﾞ ダ ﾁﾞ ヂ ﾂﾞ ヅ ﾃﾞ デ ﾄﾞ ド
ﾊﾞ バ ﾋﾞ ビ ﾌﾞ ブ ﾍﾞ ベ ﾎﾞ ボ
ﾊﾟ パ ﾋﾟ ピ ﾌﾟ プ ﾍﾟ ペ ﾎﾟ ポ
｢ 「 ｣ 」 ､ 、 ｡ 。 . ．
);

}#winit END

#################################################
#串チェック
sub proxy_status {
    foreach(('HTTP_VIA', 'HTTP_X_FORWARDED_FOR', 'HTTP_FORWARDED',
	     'HTTP_X_LOCKING', 'HTTP_CACHE_INFO', 'HTTP_PROXY_CONNECTION')) {
	#&err("$_=$ENV{$_}") if($ENV{$_} ne ""); # 串
	return 2 if($ENV{$_} ne ""); # 串
    }
    return 3 if(($host !~ /jp$/i) # 海外アクセス。匿名串かも。
		&& ($host !~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/));
    return 4 if($host =~ /ac\.jp$/i); # 大学とかからアクセス。匿名串かも??

    return 0; #生IP(たぶん)
}

#################################################
#open串チェック(重いので箱作成時にのみ使用)
sub is_open_proxy() {
	foreach((80, 8080, 3128, 8000)){
		return 1 if &is_port_open($ENV{'REMOTE_ADDR'}, $_);
	}
	return 0;
}

sub is_port_open() {
	my($m_host, $m_port) = @_;
	my($m_sock, $m_result,$m_prot);
	$m_resuld = 0;
	$m_host = (gethostbyname($m_host))[4];
	$m_prot = (getprotobyname('tcp'))[2];
	$m_sock = pack('S n a4 x8',AF_INET,$m_port,$m_host);
	if (socket(SOCK,PF_INET,SOCK_STREAM,$m_prot)) {
		eval {
			local $SIG{'ALRM'} = sub { die "timeout"; };
			alarm($port_check_timeout);
			if (connect(SOCK,$m_sock)) {
				$m_result = 1;
				close(SOCK);
			}
			alarm(0);
		};
	}
	return $m_result;
}


#################################################
#$dateに時刻を代入します。
sub jikan{
my($m_sec,$m_min,$m_hour,$m_mday,$m_month,$m_year,$m_wday,$m_yday,$m_isdst,$m_youbi);

$ENV{'TZ'}   = 'JST-9';$times = time;
#18時間時差があるなら、$times = time+18*60*60とする。
($m_sec,$m_min,$m_hour,$m_mday,$m_month,$m_year,$m_wday,$m_yday,$m_isdst) = localtime($times);
$m_month++;
$m_youbi = ('日','月','火','水','木','金','土') [$m_wday];
$date = sprintf("%d月%02d日（%s）%02d時%02d分%02d秒",$m_month,$m_mday,$m_youbi,$m_hour,$m_min,$m_sec);
}#jikan END

##################################################
#入力変換
#半角カナ　a1-df(161-223)
#シフトjis　81-9f e0-fc(129-159 224-252) + 40-7e 80-fc(64-126 128-252)
sub wdecode {
my($m_pair,$m_name,$m_value);

if($ENV{'REQUEST_METHOD'} eq "POST"){
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); 
	$postf='on';
}else{
	$buffer = $ENV{'QUERY_STRING'};
}
@pairs = split(/&/,$buffer);
foreach $m_pair (@pairs){
	($m_name, $m_value) = split(/=/, $m_pair);
	$m_value =~ tr/+/ /;
	$m_value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*m_value,'sjis');
	$m_value =~ s/(([\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc])+)|(([\xa1-\xdf])([\xde-\xdf])?)/$1 || $h2z{$3}/geo;
        $m_value =~ s/[\x00-\x09\x0b-\x0c\x0e-\x1f]//g;
        $m_value =~ s/&#/&amp;#/g;
        $m_value =~ s/&rlo;/&amp;rlo;/g;
        $m_value =~ s/&rlm;/&amp;rlm;/g;
        $m_value =~ s/</&lt;/g;
        $m_value =~ s/>/&gt;/g;
        $m_value =~ s/"/&quot;/g;
        $m_value =~ s/:#/:&#35;/g;
	if( $m_name eq 'chat' ){
		$m_value =~ s/\r\n/<br>/g;$m_value =~ s/\r/<br>/g;$m_value =~ s/\n/<br>/g;
	}
	$m_value =~ s/[\x00-\x1f]//g;
	$FORM{$m_name} = $m_value if($m_name && $m_value);
}#foreach

}#wdecode END
##################################################
#エラー表示
sub err{
my($m_error);

$m_error = $_[0];
print "Content-type: text/html; charset=Shift_JIS\n\n";
print <<"_HTML_";
<HTML><HEAD>
$metacode
<TITLE>$ortitle</TITLE></HEAD>
<META HTTP-EQUIV=refresh CONTENT=5;URL="./$cginame1">
$body
<BR><BR><BR><BR><BR>
<CENTER><H1>$m_error</H1></CENTER><BR>
<BR><BR><BR><BR><BR>
<CENTER><FONT SIZE=6><A HREF="$cgidir/$cginame1">リストへ戻る</A></FONT></CENTER>
$maruc
</BODY></HTML>
_HTML_
exit;
}#err END
##################################################
sub logdel { 
my($m_lognum,$m_line,$m_room);

$m_lognum = $_[0];

if($m_move eq "move"){
	use File::Copy;
	move("./$logdir/$m_lognum.dat", "$senddat/$m_lognum.dat");
	move("./$htmdir/$m_lognum.html", "$sendhtm/$m_lognum.html");
}else{
	unlink "./$logdir/$m_lognum.dat";
	unlink "./$htmdir/$m_lognum.html";
}

opendir(DIR,"$coudir") || return;
	@readlist = grep(/dat/, readdir(DIR));
closedir(DIR);
foreach $m_room (@readlist) {
	if($m_room=~/$m_lognum/){
		unlink "./$coudir/$m_room";
	}
}#foreach

}#logdel END

1;  # RETURN TRUE
__END__
