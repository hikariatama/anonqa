import base64
import hashlib
import os
import random

from . import config

cfg = config.parse(os.environ["CONFIG_PATH"])

# fmt: off

NAMES = ["Akira", "Banko", "Banzan", "Bassui", "Benjiro", "Chimon", "Chotan", "Dai", "Daido", "Doryo", "Engu", "Enki", "Enmei", "Eryu", "Fudoki", "Fujita", "Genko", "Goro", "Hakaku", "Haru", "Hideaki", "Hiromasa", "Hiroshi", "Hisoka", "Hoshi", "Iachima", "Itsu", "Jikai", "Jiro", "Jiryu", "Joben", "Joji", "Jomei", "Junichiro", "Kado", "Kaisha", "Kakumyo", "Kanaye", "Kando", "Kane", "Kaori", "Kazuo", "Keitaro", "Kentaro", "Kin", "Kishi", "Kisho", "Kiyoshi", "Ai", "Aiko", "Akako", "Akanah", "Aki", "Akina", "Akiyama", "Amarante", "Amaya", "Aneko", "Anzan", "Anzu", "Aoi", "Asa", "Ayame", "Bankei", "Chika", "Chinshu", "Chiyo", "Cho", "Chorei", "Dai", "Eido", "Etsu", "Fuyo", "Gyo Shin", "Hakue", "Hama", "Hanako", "Haya", "Hisa", "Hoshi", "Ima", "Ishi", "Iva", "Jakushitsu", "Jimin", "Jin", "JoMei", "Kaede", "Kagami", "Kaida", "Kaiya", "Kameko", "Kamin", "Kane", "Kaori", "Kaoru", "Kata", "Kaya", "Kogen", "Koichi", "Kozan", "Makoto", "Mamoru", "Manzo", "Mareo", "Maro", "Masahiro", "Masakazu", "Masao", "Masato", "Masatoshi", "Michio", "Minoru", "Montaro", "Morio", "Mu-nan", "Mugen", "Nan Shin", "Naoko", "Oki", "Raidon", "Rei", "Ringo", "Roka", "Ronin", "Ryogi", "Ryoichi", "Ryozo", "Ryuichi", "Saburo", "Seiichi", "Seiko", "Senichi", "Shinichi", "Shiro", "Yasuo", "Yemon", "Yogi", "Yoshi", "Yoshifumi", "Yukio", "Yutaka", "Zen", "Miya", "Miyoko", "Miyuki", "Momoko", "Mutsuko", "Myoki", "Nahoko", "Nami", "Nanako", "Nanami", "Naoko", "Nariko", "Natsuko", "Nayoko", "Nishi", "Nori", "Noriko", "Nozomi", "Nyoko", "Oki", "Rai", "Raku", "Rei", "Reiko", "Ren", "Renora", "Rieko", "Rikako", "Riku", "Rinako", "Rini", "Risako", "Roshin", "Rumiko", "Ruri", "Ryoko", "Sachi", "Sachiko", "Sada", "Saeko", "Saiun", "Saki", "Sakiko", "Sakuko", "Sakura", "Sakurako", "Sanako", "Sasa", "Sashi", "Sato", "Satoko", "Sawa", "Sayo", "Sayoko", "Seki", "Shika", "Shikah", "Shina", "Shinko", "Shoko", "Sorano", "Suki", "Sumi", "Tadako", "Taido", "Taka", "Takako", "Takara", "Taki", "Tamaka", "Tamiko", "Tanaka", "Taney", "Tani", "Taree", "Tazu", "Tennen", "Tetsu", "Tokiko", "Tomi", "Tomiko", "Tora", "Tori", "Toyo", "Umeko", "Usagi", "Wakana", "Washi", "Yachi", "Yaki", "Yama", "Yasu", "Yayoi", "Yei", "Yoi", "Yoko", "Yori", "Yoshiko", "Yuka", "Yukako", "Yukiko", "Yumi", "Yumiko", "Yuri", "Yuriko", "Yutsuko", "Zadhiya"]
SURNAMES = ["Abe", "Adachi", "Akagi", "Akamine", "Aki", "Akiyama", "Amano", "Amari", "Amaya", "Ando", "Anno", "Anzai", "Aoki", "Aoyama", "Arai", "Arakaki", "Arakawa", "Araki", "Arata", "Araya", "Arima", "Arita", "Asa", "Asai", "Asano", "Asato", "Ashikaga", "Azuma", "Baba", "Ban", "Bando", "Chiba", "Chinen", "Chino", "Date", "Doi", "Domen", "Eguchi", "Endo", "Enomoto", "Eto", "Fujii", "Fujikawa", "Fujimori", "Fujimoto", "Fujimura", "Fujino", "Fujioka", "Fujita", "Fujiwara", "Fukuda", "Fukuhara", "Fukui", "Fukumoto", "Fukunaga", "Fukushima", "Funai", "Furukawa", "Furuta", "Furutani", "Furuya", "Fuse", "Gima", "Go", "Goda", "Goto", "Goya", "Hada", "Haga", "Hagiwara", "Hamada", "Hamamoto", "Hamasaki", "Handa", "Hano", "Hara", "Harada", "Hase", "Hasegawa", "Hashimoto", "Hata", "Hatanaka", "Hattori", "Hayakawa", "Hayashi", "Hayashida", "Higa", "Higashi", "Higuchi", "Hino", "Hirabayashi", "Hirai", "Hirano", "Hiraoka", "Hirata", "Hirayama", "Hironaka", "Hirose", "Hirota", "Hoga", "Hokama", "Honda", "Hora", "Hori", "Horie", "Horiuchi", "Hoshino", "Ichikawa", "Ida", "Ide", "Igarashi", "Ige", "Iha", "Iida", "Ike", "Ikeda", "Ikehara", "Imada", "Imai", "Imamura", "Inaba", "Inouye", "Isa", "Iseri", "Ishibashi", "Ishida", "Ishihara", "Ishii", "Ishikawa", "Ishimoto", "Isobe", "Ito", "Itoh", "Iwai", "Iwamoto", "Iwasaki", "Iwata", "Izumi", "Jin", "Jo", "Juba", "Kaba", "Kagawa", "Kai", "Kajiwara", "Kamei", "Kamiya", "Kanai", "Kanda", "Kaneko", "Kanemoto", "Kaneshiro", "Kanno", "Kano", "Kasai", "Kase", "Kataoka", "Katayama", "Kato", "Kawabata", "Kawaguchi", "Kawahara", "Kawai", "Kawakami", "Kawamoto", "Kawamura", "Kawano", "Kawasaki", "Kawashima", "Kawata", "Kaya", "Kibe", "Kida", "Kido", "Kikuchi", "Kimoto", "Kimura", "Kinoshita", "Kishi", "Kishimoto", "Kita", "Kitagawa", "Kitamura", "Kiyabu", "Kobashigawa", "Kobayashi", "Kobe", "Koda", "Kodama", "Koga", "Koike", "Koizumi", "Kojima", "Komatsu", "Kon", "Konda", "Kondo", "Konishi", "Konno", "Kono", "Konya", "Koyama", "Koyanagi", "Kuba", "Kubo", "Kubota", "Kudo", "Kumagai", "Kuno", "Kuramoto", "Kurata", "Kure", "Kurihara", "Kuroda", "Kurokawa", "Kuse", "Kusumoto", "Kuwahara", "Machi", "Machida", "Mae", "Maeda", "Maekawa", "Maita", "Maki", "Makino", "Mano", "Maruyama", "Masaki", "Mase", "Masuda", "Matsubara", "Matsuda", "Matsui", "Matsumoto", "Matsumura", "Matsunaga", "Matsuno", "Matsuo", "Matsuoka", "Matsushima", "Matsushita", "Matsuura", "Matsuyama", "Matsuzaki", "Mayeda", "Mihara", "Mikami", "Miki", "Minami", "Minamoto", "Mino", "Mita", "Miura", "Miya", "Miyagawa", "Miyahara", "Miyahira", "Miyake", "Miyamoto", "Miyasaki", "Miyasato", "Miyashiro", "Miyashita", "Miyata", "Miyazaki", "Miyoshi", "Mizuno", "Mochizuki", "Mori", "Morikawa", "Morimoto", "Morine", "Morino", "Morioka", "Morishige", "Morishita", "Morita", "Moriyama", "Mukai", "Mura", "Murai", "Murakami", "Muramoto", "Muranaka", "Murano", "Muraoka", "Murata", "Murayama", "Muto", "Nagai", "Nagamine", "Nagano", "Nagao", "Nagasawa", "Nagata", "Naito", "Nakada", "Nakagawa", "Nakahara", "Nakai", "Nakajima", "Nakama", "Nakamoto", "Nakamura", "Nakanishi", "Nakano", "Nakao", "Nakashima", "Nakasone", "Nakata", "Nakatani", "Nakatomi", "Nakayama", "Nakazawa", "Namba", "Nii", "Nishi", "Nishida", "Nishihara", "Nishikawa", "Nishimoto", "Nishimura", "Nishioka", "Nishiyama", "Nitta", "Niwa", "No", "Noda", "Noguchi", "Nomura", "Nonaka", "Noya", "Oba", "Obara", "Obi", "Oda", "Oe", "Ogasawara", "Ogata", "Ogata", "Ogawa", "Ogino", "Ogura", "Oh", "Ohara", "Ohashi", "Ohta", "Oishi", "Oka", "Okabe", "Okada", "Okamoto", "Okamura", "Okane", "Okano", "Okawa", "Okazaki", "Oki", "Okimoto", "Okino", "Okita", "Okubo", "Okuda", "Okuma", "Okumura", "Okura", "Omori", "Omura", "Onaga", "Onishi", "Ono", "Orio", "Osada", "Osaki", "Ose", "Oshima", "Oshima", "Oshiro", "Oshiro", "Oshiro", "Oshita", "Ota", "Otake", "Otani", "Otani", "Otsuka", "Ouchi", "Oyama", "Oyama", "Oye", "Ozaki", "Ozawa", "Sada", "Sadow", "Saeki", "Saiki", "Saito", "Sakaguchi", "Sakai", "Sakamoto", "Sakata", "Sako", "Sakuma", "Sakurai", "Sama", "Sanda", "Sando", "Sano", "Sasaki", "Sasaki", "Sato", "Satow", "Sawa", "Sawada", "Sawaya", "Sazama", "Seki", "Sekiguchi", "Seno", "Seo", "Sera", "Seta", "Seto", "Shiba", "Shibata", "Shibuya", "Shima", "Shimabukuro", "Shimada", "Shimamoto", "Shimizu", "Shimoda", "Shimomura", "Shinohara", "Shinsato", "Shintani", "Shirai", "Shiraishi", "Shiraki", "Shiro", "Shiroma", "Shishido", "Shoda", "Shoji", "Soda", "Soga", "Soma", "Sone", "Sonoda", "Suda", "Sugai", "Sugawara", "Sugihara", "Sugimoto", "Sugita", "Sugiyama", "Suko", "Sumida", "Sunada", "Suto", "Suzuki", "Tabata", "Tachibana", "Tada", "Tagawa", "Taguchi", "Tahara", "Taira", "Tajima", "Takagi", "Takahashi", "Takai", "Takaki", "Takamoto", "Takano", "Takara", "Takashima", "Takata", "Takayama", "Takeda", "Takei", "Takemoto", "Takenaka", "Takeshita", "Taketa", "Takeuchi", "Tamaki", "Tamanaha", "Tamashiro", "Tamura", "Tanabe", "Tanaka", "Tani", "Tanigawa", "Taniguchi", "Tanimoto", "Tanji", "Tano", "Tao", "Tashiro", "Tengan", "Terada", "Teramoto", "Teruya", "Teshima", "Tobe", "Toda", "Tokuda", "Tokunaga", "Toma", "Tominaga", "Tomita", "Tone", "Toyama", "Toyoda", "Tsuchida", "Tsuchiya", "Tsuda", "Tsuji", "Tsukamoto", "Tsutsui", "Tsutsumi", "Uchida", "Uchiyama", "Ueda", "Uehara", "Uemura", "Ueno", "Umeda", "Umemoto", "Uno", "Usui", "Uyeda", "Uyehara", "Uyemura", "Uyeno", "Wada", "Wakabayashi", "Watanabe", "Yagi", "Yamada", "Yamagata", "Yamaguchi", "Yamakawa", "Yamamoto", "Yamamura", "Yamanaka", "Yamane", "Yamaoka", "Yamasaki", "Yamashiro", "Yamashita", "Yamauchi", "Yamazaki", "Yanagi", "Yano", "Yasuda", "Yasui", "Yasutake", "Yogi", "Yokota", "Yokoyama", "Yonamine", "Yoneda", "Yoshida", "Yoshihara", "Yoshikawa", "Yoshimoto", "Yoshimura", "Yoshinaga", "Yoshino", "Yoshioka"]

# fmt: on

USERNAMES = list(map(lambda x: x[0] + " " + x[1], zip(NAMES, SURNAMES)))


def escape_html(text: str, /) -> str:  # sourcery skip
    """
    Pass all untrusted/potentially corrupt input here
    :param text: Text to escape
    :return: Escaped text
    """
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def get_hash(user_id: int) -> str:
    """
    Generate hash for user_id
    :param user_id: User ID
    :return: Hash
    """
    return hashlib.sha256(
        str(user_id).encode() + bytes.fromhex(cfg.main.secret)
    ).hexdigest()


def get_hash_base(user_id: int) -> str:
    """
    Generate base64 tag for user_id
    :param user_id: User ID
    :return: Hash
    """
    return base64.b64encode(bytes.fromhex(get_hash(user_id))).decode()


def get_name(user_id: int) -> str:
    """
    Get name for user
    :param user_id: User ID
    :return: Name
    """
    random.seed(user_id * cfg.main.prime_a + cfg.main.prime_b)
    return random.choice(USERNAMES)
