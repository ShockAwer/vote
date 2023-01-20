package jcode;
&init unless defined $version;
sub init {
    $version = $rcsid =~ /,v ([\d.]+)/ ? $1 : 'unkown';

    $re_bin       = '[\000-\006\177\377]';

    $re_jis1978   = '\e\$\@';
    $re_jis1983   = '\e\$B';
    $re_jis1990   = '\e\@\e\$B';
    $re_jp        = "$re_jis1978|$re_jis1983|$re_jis1990";

    $re_asc       = '\e\([BJ]';
    $re_kana      = '\e\(I';

    $re_ascii     = '[\007-\176]';
    $re_odd_kana  = '[\241-\337]([\241-\337][\241-\337])*';

    $re_sjis_c    = '[\201-\237\340-\374][\100-\176\200-\374]';
    $re_sjis_ank  = '[\007-\176\241-\337]';

    $re_euc_c     = '\[241-\376][\241-\376]';
    $re_euc_kana  = '\216[\241-\337]';


    ($esc_jp, $esc_asc, $esc_kana) = ("\e\$B", "\e(B", "\e(I");
    $re_sjis_kana = '[\241-\337]';
    $re_euc_c     = '\[241-\376][\241-\376]';    $re_euc_kana  = '\216[\241-\337]';

    $re_euc_s = "($re_euc_c)+";
    $re_sjis_s = "($re_sjis_c)+";

	$convf{'jis', 'sjis'} = *jis2sjis;
	$convf{'sjis', 'sjis'} = *sjis2sjis;
	$convf{'euc', 'sjis'} = *euc2sjis;

}

sub getcode {
    local(*_) = @_;
    local($matched, $code);

    if (!/[\e\200-\377]/) {     # not Japanese
        $matched = 0;
        $code = undef;
    }                           # 'jis'
    elsif (/$re_jp|$re_asc|$re_kana/o) {
        $matched = 1;
        $code = 'jis';
    }
    elsif (/$re_bin/o) {        # 'binary'
        $matched = 0;
        $code = 'binary';
    }
    elsif (/(^|[\000-\177])[\241-\337]([\241-\337][\241-\337])*($|[\000-\177])/go) {
                                # 'sjis' jis îºäpÉJÉiÇÃäÔêîå¬ÇÃòAë±
        $matched = 1;
        $code = 'sjis';
    }
    else {                      # should be 'euc' or 'sjis'
        local($sjis, $euc);

        $sjis += length($&) while /([\201-\237\340-\374][\100-\176\200-\374]|[\007-\176\241-\337])+/go;
        $euc  += length($&) while /(\[241-\376][\241-\376]|\216[\241-\337]|[\007-\176])+/go;

        $matched = &max($sjis, $euc);
        $code = ('euc', undef, 'sjis')[($sjis<=>$euc) + $[ + 1];
    }
#    (&max($sjis, $euc), ('euc', undef, 'sjis')[($sjis<=>$euc) + $[ + 1]);
    wantarray ? ($matched, $code) : $code;

}

sub max { $_[ $[ + ($_[$[] < $_[$[+1]) ]; }

sub convert {
    local(*_, $ocode, $icode) = @_;
    return (undef, undef) unless $icode = $icode || &getcode(*_);
    return (undef, $icode) if $icode eq 'binary';
    local(*convf) = $convf{$icode, $ocode};
    do convf(*_);
    (*convf, $icode);
}
sub jis2sjis {
    local(*_, $n) = @_;
    s/(\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I)([^\e]*)/&_jis2sjis($1,$2)/geo;
    $n;
}
sub _jis2sjis {
    local($esc, $_) = @_;
    if ($esc =~ /\e\$\(D/o) {
	s/../\x81\xac/g;
	$n = length;
    }
    elsif ($esc !~ /\e\([BJ]/o) {
	$n += tr/\041-\176/\241-\376/;
	s/([\241-\376][\241-\376])/&e2s($1)/geo if $esc =~ /\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D/o;
    }
    $_;
}
sub euc2sjis {
    local(*_, $n) = @_;
    $n = s/([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])/&e2s($1)/geo;
}
sub e2s {
    local($c1, $c2, $code);
    ($c1, $c2) = unpack('CC', $code = shift);
    if ($c1 == 0x8e) {		# SS2
	return substr($code, 1, 1);
    } elsif ($c1 == 0x8f) {	# SS3
	return "\x81\xac";
    } elsif ($c1 % 2) {
	$c1 = ($c1>>1) + ($c1 < 0xdf ? 0x31 : 0x71);
	$c2 -= 0x60 + ($c2 < 0xe0);
    } else {
	$c1 = ($c1>>1) + ($c1 < 0xdf ? 0x30 : 0x70);
	$c2 -= 2;
    }
	pack('CC', $c1, $c2);
}
sub sjis2sjis {
    local(*_) = @_;
}
1;

