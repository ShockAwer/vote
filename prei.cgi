#!/usr/bin/perl
#
#������cgi��snog�̐��삵��vote4�����ǂ������ł�
#�����������҂����Ȃ��ׁA�Ƃ肠�����񎟔z�z�Ǝg�p�͕s�ɂȂ��Ă܂�
#prei.cgi�́A���ʂ��Ďg����T�u���[�`���W�ł��B
#���O�f�[�^�t�H�[�}�b�g
#
#$title:#$vkey:#$ddata:#$pwlhost:#$times:#$chat:#$date:#$pwxhost:#:#
#$pwhost:#$times:#$mrev:#$vote:#$chat:#$date:#:#
##############################################################################
#�����ݒ�Ȃ�
use Socket;

require './config.cgi'; # �ݒ�ǂݍ���

sub winit{
my($m_h1,$m_h2,$m_h3,$m_h4,$m_ph1,$m_ph2,$m_ph3,$m_ph4,$m_ph5,$m_ph6,$m_ph7,$m_ph8,$m_wh1,$m_wh2);

&global_config();

$host = $ENV{'REMOTE_HOST'};
$hosta = '';	#������
$xhost = ''; ## ���A�h���X
$proxycheck = 0;	#�v���L�V�t���O������
$hosta=$ENV{'HTTP_VIA'} if( $ENV{'HTTP_VIA'}=~s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_X_FORWARDED_FOR'} if( $ENV{'HTTP_X_FORWARDED_FOR'}=~s/^(\d+)\.(\d+)\.(\d+)\.(\d+)(\D*).*/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_FORWARDED'} if( $ENV{'HTTP_FORWARDED'}=~s/.*\s(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_CLIENT_IP'} if( $ENV{'HTTP_CLIENT_IP'} =~s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
$hosta=$ENV{'HTTP_SP_HOST'} if( $ENV{'HTTP_SP_HOST'} =~s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$1.$2.$3.$4/ );
if( $hosta eq '' ){		#�R�������Ȃ�
	$hosta=$ENV{'REMOTE_ADDR'};			#���h�o�A�h���X
	$proxycheck = &proxy_status();
}else{
    	$xhost = $ENV{'REMOTE_ADDR'};
	$proxycheck = 1; #�R���
}
($m_h1,$m_h2,$m_h3,$m_h4) = split(/\./,$hosta);		#�h�o�̈Í����i�ʓ|�������̂ňꗥ�������l�Ɂj
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
$orititle='�����A���P�[�g+';	#�^�C�g��
$body = '<BODY BGCOLOR="#A1FE9F" TEXT="#000000" LINK="#0000ff" VLINK="#ff0000">
';	#�W���\���ݒ�
$metacode = '<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">';	#�����R�[�h�w��
$maruc = '<H5 ALIGN=right>�I���W�i����<A HREF="http://www.cup.com/yui/index.html">�䂢�ځ[�ǁ��䂢�ځ[��</A></H5>';	#���쌠�\��

#���p��S�p�ɕϊ�����e�[�u��
%h2z = qw(
� �A � �C � �E � �G � �I
� �J � �L � �N � �P � �R
� �T � �V � �X � �Z � �\
� �^ � �` � �c � �e � �g
� �i � �j � �k � �l � �m
� �n � �q � �t � �w � �z
� �} � �~ � �� � �� � ��
� �� � �� � ��
� �� � �� � �� � �� � ��
� �� � �� � ��
� �b � �[
� �� � �� � ��
� �@ � �B � �D � �F � �H
�� �K �� �M �� �O �� �Q �� �S
�� �U �� �W �� �Y �� �[ �� �]
�� �_ �� �a �� �d �� �f �� �h
�� �o �� �r �� �u �� �x �� �{
�� �p �� �s �� �v �� �y �� �|
� �u � �v � �A � �B . �D
);

}#winit END

#################################################
#���`�F�b�N
sub proxy_status {
    foreach(('HTTP_VIA', 'HTTP_X_FORWARDED_FOR', 'HTTP_FORWARDED',
	     'HTTP_X_LOCKING', 'HTTP_CACHE_INFO', 'HTTP_PROXY_CONNECTION')) {
	#&err("$_=$ENV{$_}") if($ENV{$_} ne ""); # ��
	return 2 if($ENV{$_} ne ""); # ��
    }
    return 3 if(($host !~ /jp$/i) # �C�O�A�N�Z�X�B�����������B
		&& ($host !~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/));
    return 4 if($host =~ /ac\.jp$/i); # ��w�Ƃ�����A�N�Z�X�B����������??

    return 0; #��IP(���Ԃ�)
}

#################################################
#open���`�F�b�N(�d���̂Ŕ��쐬���ɂ̂ݎg�p)
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
#$date�Ɏ����������܂��B
sub jikan{
my($m_sec,$m_min,$m_hour,$m_mday,$m_month,$m_year,$m_wday,$m_yday,$m_isdst,$m_youbi);

$ENV{'TZ'}   = 'JST-9';$times = time;
#18���Ԏ���������Ȃ�A$times = time+18*60*60�Ƃ���B
($m_sec,$m_min,$m_hour,$m_mday,$m_month,$m_year,$m_wday,$m_yday,$m_isdst) = localtime($times);
$m_month++;
$m_youbi = ('��','��','��','��','��','��','�y') [$m_wday];
$date = sprintf("%d��%02d���i%s�j%02d��%02d��%02d�b",$m_month,$m_mday,$m_youbi,$m_hour,$m_min,$m_sec);
}#jikan END

##################################################
#���͕ϊ�
#���p�J�i�@a1-df(161-223)
#�V�t�gjis�@81-9f e0-fc(129-159 224-252) + 40-7e 80-fc(64-126 128-252)
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
#�G���[�\��
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
<CENTER><FONT SIZE=6><A HREF="$cgidir/$cginame1">���X�g�֖߂�</A></FONT></CENTER>
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
