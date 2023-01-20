sub global_config {
$cgidir = '../~vote';	#CGIを置く場所
$logdir = '';	#ログディレクトリ名
$htmdir = '';	#ｈｔｍｌファイルディレクトリ名
$coudir = '';	#カウンタディレクトリ名
$vkey = '0001';		#チェックキー
$postf ='on';		#ＰＯＳＴかどうかのチェック
$brmax=15;		#コメント最大行数
$chatmax=1000;		#コメント文の最大長さ
$namemax=35;		#タイトルの最大長さ
$sday = 0.1;		#初期日数
$masterkey = '';	#マスターパスワード

#初期設定＋ by ニセモク（相対パスで。最後にスラッシュは付けないでください）
$sendhtm = '../';	#移動用のhtm送り先ディレクトリ
$senddat = '../';	#移動用のdat送り先ディレクトリ
$forbid = '100';	#箱作成上限

$cginame1 = 'list.cgi';		#リストスクリプト名
$cginame2 = 'vote.cgi';		#アンケートスクリプト名
}

sub vote_config() {
$max = 1000;			#最大投票数
$gif = '../bar.gif';		#バーファイル
$votemax=40;			#項目名の最大長さ
$commax=20;			#50最近の投票の表示数
$comtime= 12;			#表示するコメントの過去時間
$tmpdir='';			#テンポラリディレクトリ

$daylimit = 1.5;	#書き込みの無かった投票箱を削除するまでの日数
$aday = 0.05;		#１発言で伸びる削除までの日数
$hday = 5.00;		#最低日数
$lday = 864000;		#延命票対策。10*24*60*60
$lbox = 900;		#生き残らせる箱の数

$hakosokudo=100;			#同一ホストから２４時間内に作れる箱の最大数
$wspeedfile = '';		#書き込み速度チェック用ファイル名
$wspeedtime = 300;		#書き込み速度記録時間（分）
$wspeedcou = 300;			#速度違反の書き込み数

@titleNGwords = ();
@voteNGwords = (); # 既存項目への継続投票も規制
@votenNGwords = ();# 新規項目のみ規制
@chatNGwords = ();#

$xhakosokudo=3;		#同一漏れ串から２４時間内に作れる箱の最大数
$xwspeedcou = 1;	#速度違反の書き込み数(匿名串用)

@banned_proxies = ();   #禁止串リスト
$ban_open_proxy = 0;    #公開串からの箱作成の禁止

$port_check_timeout = 5; # 串チェックのタイムアウト(ポート一つ毎の)単位は秒
}

# $proxycheck = 0:漏れ串 2:匿名串 3:海外アクセス 4:国内大学等

#############
# 匿名串判定
sub is_annonymous_proxy() {
    return ( ($proxycheck == 2) || ($proxycheck == 3) );
}

#############
# 禁止串判定
sub is_banned_proxy() {
    # return 1 if($proxycheck == 3); #串タイプで弾く
    foreach (@banned_proxies) {
	return 1 if(($host eq $_) || ($hosta eq $_) || ($xhost eq $_));
    }
    return 0;
}

1; # RETURN TRUE
__END__
