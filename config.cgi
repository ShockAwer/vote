sub global_config {
$cgidir = 'http://www.zianplus.net/cgi-bin/vote+';	#CGI��u���ꏊ
$logdir = '';	#���O�f�B���N�g����
$htmdir = '';	#���������t�@�C���f�B���N�g����
$coudir = '';	#�J�E���^�f�B���N�g����
$vkey = '0001';		#�`�F�b�N�L�[
$postf ='on';		#�o�n�r�s���ǂ����̃`�F�b�N
$brmax=15;		#�R�����g�ő�s��
$chatmax=1000;		#�R�����g���̍ő咷��
$namemax=35;		#�^�C�g���̍ő咷��
$sday = 0.1;		#��������
$masterkey = '';	#�}�X�^�[�p�X���[�h

#�����ݒ�{ by �j�Z���N�i���΃p�X�ŁB�Ō�ɃX���b�V���͕t���Ȃ��ł��������j
$sendhtm = '../';	#�ړ��p��htm�����f�B���N�g��
$senddat = '../';	#�ړ��p��dat�����f�B���N�g��
$forbid = '100';	#���쐬���

$cginame1 = 'list.cgi';		#���X�g�X�N���v�g��
$cginame2 = 'vote.cgi';		#�A���P�[�g�X�N���v�g��
}

sub vote_config() {
$max = 1000;			#�ő哊�[��
$gif = '../bar.gif';		#�o�[�t�@�C��
$votemax=40;			#���ږ��̍ő咷��
$commax=20;			#50�ŋ߂̓��[�̕\����
$comtime= 12;			#�\������R�����g�̉ߋ�����
$tmpdir='';			#�e���|�����f�B���N�g��

$daylimit = 1.5;	#�������݂̖����������[�����폜����܂ł̓���
$aday = 0.05;		#�P�����ŐL�т�폜�܂ł̓���
$hday = 5.00;		#�Œ����
$lday = 864000;		#�����[�΍�B10*24*60*60
$lbox = 900;		#�����c�点�锠�̐�

$hakosokudo=100;			#����z�X�g����Q�S���ԓ��ɍ��锠�̍ő吔
$wspeedfile = '';		#�������ݑ��x�`�F�b�N�p�t�@�C����
$wspeedtime = 300;		#�������ݑ��x�L�^���ԁi���j
$wspeedcou = 300;			#���x�ᔽ�̏������ݐ�

@titleNGwords = ();
@voteNGwords = (); # �������ڂւ̌p�����[���K��
@votenNGwords = ();# �V�K���ڂ̂݋K��
@chatNGwords = ();#

$xhakosokudo=3;		#����R�������Q�S���ԓ��ɍ��锠�̍ő吔
$xwspeedcou = 1;	#���x�ᔽ�̏������ݐ�(�������p)

@banned_proxies = ();   #�֎~�����X�g
$ban_open_proxy = 0;    #���J������̔��쐬�̋֎~

$port_check_timeout = 5; # ���`�F�b�N�̃^�C���A�E�g(�|�[�g�����)�P�ʂ͕b
}

# $proxycheck = 0:�R��� 2:������ 3:�C�O�A�N�Z�X 4:������w��

#############
# ����������
sub is_annonymous_proxy() {
    return ( ($proxycheck == 2) || ($proxycheck == 3) );
}

#############
# �֎~������
sub is_banned_proxy() {
    # return 1 if($proxycheck == 3); #���^�C�v�Œe��
    foreach (@banned_proxies) {
	return 1 if(($host eq $_) || ($hosta eq $_) || ($xhost eq $_));
    }
    return 0;
}

1; # RETURN TRUE
__END__
