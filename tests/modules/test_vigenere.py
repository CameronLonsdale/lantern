"""Tests for the Simple Substitution module"""

import pycipher
import random
import string

import pytest
from tests.util import get_top_decryptions

from lantern import fitness
from lantern.modules import vigenere
from lantern.analysis import frequency
from lantern.util import remove


def _test_vigenere(plaintext, first, *rest, key, period=None, top_n=1):
    ciphertext = pycipher.Vigenere(key).encipher(plaintext)
    decryptions = vigenere.crack(ciphertext, first, *rest, key_period=period)

    top_decryptions = get_top_decryptions(decryptions, top_n)

    match = None
    for decrypt in top_decryptions:
        print(decrypt)
        if decrypt.plaintext.upper() == remove(plaintext.upper(), string.punctuation + string.whitespace):
            match = decrypt
            break

    assert match is not None
    assert ''.join(key) in match.key  # Not equality because key can be repeated if the chosen period was longer


def test_250_character_text_periods_unknown():
    """Testing text of length ~250, many different periods, none given to cracker"""
    plaintext = """Almost all of the game's cut-scenes are done in a stick puppet style. The game begins with the narrator (voiced by Will Stamper) telling the adventures of the hundreds of friends aboard the S.S. Friendship, as well as Hatty Hattington, who is known as "best friend to one and all"."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]
        _test_vigenere(plaintext, fitness.ChiSquared(frequency.english.unigrams), fitness.english.quadgrams, key=key)


def test_250_character_text_periods_known():
    """Testing text of length ~250, many different periods, none given to cracker"""
    plaintext = """Almost all of the game's cut-scenes are done in a stick puppet style. The game begins with the narrator (voiced by Will Stamper) telling the adventures of the hundreds of friends aboard the S.S. Friendship, as well as Hatty Hattington, who is known as "best friend to one and all"."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]
        _test_vigenere(
            plaintext,
            fitness.ChiSquared(frequency.english.unigrams), fitness.english.quadgrams,
            key=key, period=period
        )


def test_500_character_text_all_periods_unknown():
    """Testing text of length ~500, many different periods, none given to cracker"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]
        _test_vigenere(
            plaintext,
            fitness.ChiSquared(frequency.english.unigrams), fitness.english.quadgrams,
            key=key
        )


def test_500_character_text_all_periods_known():
    """Testing text of length ~500, many different periods, none given to cracker"""
    plaintext = """Upon its release, the novel received near universal acclaim. Although Dickens' contemporary Thomas Carlyle referred to it disparagingly as that "Pip nonsense," he nevertheless reacted to each fresh instalment with "roars of laughter."Later, George Bernard Shaw praised the novel, as "All of one piece and consistently truthful." During the serial publication, Dickens was pleased with public response to Great Expectations and its sales; when the plot first formed in his mind, he called it "a very fine, new and grotesque idea."""
    for period in range(1, 10):
        key = list(string.ascii_uppercase)
        random.shuffle(key)
        key = key[:period]
        _test_vigenere(
            plaintext, fitness.ChiSquared(frequency.english.unigrams),
            key=key, period=period)


def test_text_with_punctuation_and_mixed_case():
    """Testing text containing punctauation and mixed case to test they are preserved"""
    ciphertext = """YYICS jizib AGYYX RIEWV IXAFN JOOVQ QVHDL CRKLB SSLYX RIQYI IOXQT WXRIC RVVKP BHZXI YLYZP DLCDI IKGFJ UXRIP TFQGL CWVXR IEZRV NMYSF JDLCL RXOWJ NMINX FNJSP JGHVV ERJTT OOHRM VMBWN JTXKG JJJXY TSYKL OQZFT OSRFN JKBIY YSSHE LIKLO RFJGS VMRJC CYTCS VHDLC LRXOJ MWFYB JPNVR NWUMZ GRVMF UPOEB XKSDL CBZGU IBBZX MLMKK LOACX KECOC IUSBS RMPXR IPJZW XSPTR HKRQB VVOHR MVKEE PIZEX SDYYI QERJJ RYSLJ VZOVU NJLOW RTXSD LYYNE ILMBK LORYW VAOXM KZRNL CWZRA YGWVH DLCLZ VVXFF KASPJ GVIKW WWVTV MCIKL OQYSW SBAFJ EWRII SFACC MZRVO MLYYI MSSSK VISDY YIGML PZICW FJNMV PDNEH ISSFE HWEIJ PSEEJ QYIBW JFMIC TCWYE ZWLTK WKMBY YICGY WVGBS UKFVG IKJRR DSBJJ XBSWM VVYLR MRXSW BNWJO VCSKW KMBYY IQYYW UMKRM KKLOK YYVWX SMSVL KWCAV VNIQY ISIIB MVVLI DTIIC SGSRX EVYQC CDLMZ XLDWF JNSEP BRROO WJFMI CSDDF YKWQM VLKWM KKLOV CXKFE XRFBI MEPJW SBWFJ ZWGMA PVHKR BKZIB GCFEH WEWSF XKPJT NCYYR TUICX PTPLO VIJVT DSRMV AOWRB YIBIR MVWER QJKWK RBDFY MELSF XPEGQ KSPML IYIBX FJPXR ELPVH RMKFE HLEBJ YMWKM TUFII YSUXE VLJUX YAYWU XRIUJ JXGEJ PZRQS TJIJS IJIJS PWMKK KBEQX USDXC IYIBI YSUXR IPJNM DLBFZ WSIQF EHLYR YVVMY NXUSB SRMPW DMJQN SBIRM VTBIR YPWSP IIIIC WQMVL KHNZK SXMLY YIZEJ FTILY RSFAD SFJIW EVNWZ WOWFJ WSERB NKAKW LTCSX KCWXV OILGL XZYPJ NLSXC YYIBM ZGFRK VMZEH DSRTJ ROGIM RHKPQ TCSCX GYJKB ICSTS VSPFE HGEQF JARMR JRWNS PTKLI WBWVW CXFJV QOVYQ UGSXW BRWCS MSCIP XDFIF OLGSU ECXFJ PENZY STINX FJXVY YLISI MEKJI SEKFJ IEXHF NCPSI PKFVD LCWVA OVCSF JKVKX ESBLM ZJICM LYYMC GMZEX BCMKK LOACX KEXHR MVKBS SSUAK WSSKM VPCIZ RDLCF WXOVL TFRDL CXLRC LMSVL YXGSK LOMPK RGOWD TIXRI PJNIB ILTKV OIQYF SPJCW KLOQQ MRHOW MYYED FCKFV ORGLY XNSPT KLIEL IKSDS YSUXR IJNFR GIPJK MBIBF EHVEW IFAXY NTEXR IEWRW CELIW IVPYX CIOTU NKLDL CBFSN QYSRR NXFJJ GKVCH ISGOC JGMXK UFKGR"""
    decryptions = vigenere.crack(ciphertext, fitness.ChiSquared(frequency.english.unigrams))
    assert "FREKEY" in decryptions[0].key


def test_20_character_key_length_2():
    """Testing text of length 20 characters, key of length 2"""
    plaintext = """THE EARTH IS GOOD YES"""
    key = "BC"
    _test_vigenere(plaintext, fitness.ChiSquared(frequency.english.unigrams), fitness.english.quadgrams, key=key)


def test_invalid_key_period():
    """Testing invalid values of key_period and max_key_period"""
    with pytest.raises(ValueError):
        vigenere.crack("abc", None, key_period=0)

    with pytest.raises(ValueError):
        vigenere.crack("abc", None, key_period=-1)

    with pytest.raises(ValueError):
        vigenere.crack("abc", None, max_key_period=0)

    with pytest.raises(ValueError):
        vigenere.crack("abc", None, max_key_period=-1)


def test_decrypt():
    """Test decrypt successfully decrypts ciphertext enciphered with the same key"""
    assert vigenere.decrypt("KEY", "RIJVS") == "HELLO"


def test_decrypt_with_punctuation():
    """Test decrypt skips punctuation characters"""
    assert vigenere.decrypt("SECRETS", "A PQMI VJQTVFPHYQ") == "I LOVE CRYPTOLOGY"


def test_decrypt_lower_case():
    """Test decrypt skips punctuation characters"""
    assert vigenere.decrypt("secrets", "a pqmi vjqtvfphyq") == "i love cryptology"


def test_decrypt_mixed_case():
    """Test decrypt skips punctuation characters"""
    assert vigenere.decrypt("sEcReTs", "A pQmI vJqTvFpHyQ") == "I lOvE cRyPtOlOgY"
