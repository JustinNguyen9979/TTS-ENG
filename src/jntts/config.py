MIN_RAM_GB = 8
MIN_VRAM_GB = 6
PROGRESS_BAR_WIDTH = 40  # Độ rộng của thanh tiến trình (số ký tự)
PROGRESS_BAR_CHAR = '█'  # Ký tự cho phần đã hoàn thành
REMAINING_BAR_CHAR = '░' # Ký tự cho phần còn lại

TEXT_SAMPLES = {
    "en": "A very warm welcome to you! It is a genuine pleasure to have you with us today. I sincerely hope you've been having a wonderful day so far and that the rest of your time here is enjoyable and productive.",
    "fr": "Bonjour et bienvenue ! Je suis absolument ravi(e) de vous accueillir parmi nous. J'espère sincèrement que votre journée se déroule bien jusqu'à présent et je vous souhaite de passer un excellent moment en notre compagnie. Comment allez-vous ?",
    "ja": "はじめまして。本日はようこそお越しくださいました。皆様にお会いできて大変光栄に存じます。これから素晴らしい時間を共に過ごせることを心より楽しみにしております。どうぞ、よろしくお願いいたします。",
    "zh": "大家好！非常欢迎各位的光临，我们在此怀着无比激动的心情迎接您的到来。希望您旅途顺利，并能在这里度过一段愉快而难忘的时光。我们期待与您共创美好回忆。",
    "de": "Guten Tag! Ich hoffe, es geht Ihnen blendend und Sie haben einen absolut wundervollen Tag voller Freude und Erfolg. Es ist mir eine große Freude, heute mit Ihnen in Kontakt zu treten und ich freue mich auf unser Gespräch.",
    "es": "¡Hola! Espero sinceramente que estés teniendo un día fantástico, lleno de alegría y momentos maravillosos. Es un verdadero placer conectar contigo hoy y te envío mis mejores deseos para que todo te vaya genial. ¡Un saludo muy cordial!",
    "it": "Ciao! Spero tu stia passando una giornata davvero meravigliosa, piena di sole e cose belle. È un grande piacere per me entrare in contatto con te oggi. Ti auguro tutto il meglio e spero di sentirti presto!",
    "ko": "안녕하세요! 오늘 하루도 즐겁고 행복한 일만 가득하시기를 진심으로 바랍니다. 당신과 이렇게 소통하게 되어 정말 기쁘게 생각하며, 앞으로 모든 일이 잘되시기를 응원하겠습니다. 좋은 하루 보내세요!",
    "ru": "Здравствуйте! Я искренне надеюсь, что у вас всё отлично и ваш день проходит просто замечательно. Мне очень приятно сегодня связаться с вами. Желаю вам всего самого наилучшего, успехов и прекрасного настроения!",
    "hi": "नमस्ते! मुझे पूरी उम्मीद है कि आपका दिन बहुत शानदार बीत रहा होगा और आप स्वस्थ होंगे। आज आपसे जुड़कर मुझे बहुत खुशी हो रही है। मैं आपके लिए ढेर सारी शुभकामनाएँ भेजता हूँ और आपके अच्छे स्वास्थ्य की कामना करता हूँ।",
    "pt": "Olá! Espero que você esteja tendo um dia absolutamente maravilhoso, cheio de alegria e muitas realizações. É um verdadeiro prazer conectar-me com você hoje. Envio-lhe os meus melhores votos e um grande abraço!",
    "tr": "Merhaba! Umarım harika bir gün geçiriyorsundur ve her şey yolundadır. Seninle bugün bağlantı kurmak benim için büyük bir zevk. Umarım günün geri kalanı da neşe ve başarılarla dolu olur. En iyi dileklerimle!",
}

VOICE_PRESETS = {
    # --- English (Anh) ---
    "1. English - Male, Drake": {"preset": "v2/en_speaker_1", "lang": "en"},
    "2. English - Male, James": {"preset": "v2/en_speaker_2", "lang": "en"},
    "3. English - Male, Henry": {"preset": "v2/en_speaker_3", "lang": "en"},
    "4. English - Male, Charles": {"preset": "v2/en_speaker_4", "lang": "en"},
    "5. English - Male, Brian": {"preset": "v2/en_speaker_5", "lang": "en"}, 
    "6. English - Male, Arthur": {"preset": "v2/en_speaker_6", "lang": "en"},
    "7. English - Male, Oliver": {"preset": "v2/en_speaker_7", "lang": "en"},
    "8. English - Male, Felix": {"preset": "v2/en_speaker_8", "lang": "en"},
    "9. English - Female, Venus": {"preset": "v2/en_speaker_9", "lang": "en"},
    "10. English - Male, Theodore": {"preset": "v2/en_speaker_0", "lang": "en"},

    # --- French (Pháp) ---
    "1. French - Female, Alice": {"preset": "v2/fr_speaker_1", "lang": "fr"},
    "2. French - Female, Léa": {"preset": "v2/fr_speaker_2", "lang": "fr"},
    "3. French - Male, Jules": {"preset": "v2/fr_speaker_3", "lang": "fr"},
    "4. French - Male, Ethan": {"preset": "v2/fr_speaker_4", "lang": "fr"},
    "5. French - Female, Louise": {"preset": "v2/fr_speaker_5", "lang": "fr"},
    "6. French - Male, Hugo": {"preset": "v2/fr_speaker_6", "lang": "fr"},
    "7. French - Male, Léo": {"preset": "v2/fr_speaker_7", "lang": "fr"},
    "8. French - Male, Lucas": {"preset": "v2/fr_speaker_8", "lang": "fr"},
    "9. French - Male, Raphaël": {"preset": "v2/fr_speaker_9", "lang": "fr"},
    "10. French - Male, Nathan": {"preset": "v2/fr_speaker_0", "lang": "fr"},

    # --- German (Đức) ---
    "1. German - Male, Lukas": {"preset": "v2/de_speaker_1", "lang": "de"},
    "2. German - Male, Maximilian": {"preset": "v2/de_speaker_2", "lang": "de"},
    "3. German - Female, Hanna": {"preset": "v2/de_speaker_3", "lang": "de"},
    "4. German - Male, Leon": {"preset": "v2/de_speaker_4", "lang": "de"},
    "5. German - Male, Finn": {"preset": "v2/de_speaker_5", "lang": "de"},
    "6. German - Male, Felix": {"preset": "v2/de_speaker_6", "lang": "de"},
    "7. German - Male, Paul": {"preset": "v2/de_speaker_7", "lang": "de"},
    "8. German - Female, Emma": {"preset": "v2/de_speaker_8", "lang": "de"},
    "9. German - Male, Noah": {"preset": "v2/de_speaker_9", "lang": "de"},
    "10. German - Male, Emil": {"preset": "v2/de_speaker_0", "lang": "de"},

    # --- Spanish (Tây Ban Nha) ---
    "1. Spanish - Male, Santiago": {"preset": "v2/es_speaker_1", "lang": "es"},
    "2. Spanish - Male, Javier": {"preset": "v2/es_speaker_2", "lang": "es"},
    "3. Spanish - Male, Mateo": {"preset": "v2/es_speaker_3", "lang": "es"},
    "4. Spanish - Male, Daniel": {"preset": "v2/es_speaker_4", "lang": "es"},
    "5. Spanish - Male, Alejandro": {"preset": "v2/es_speaker_5", "lang": "es"},
    "6. Spanish - Male, Manuel": {"preset": "v2/es_speaker_6", "lang": "es"},
    "7. Spanish - Male, Sebastián": {"preset": "v2/es_speaker_7", "lang": "es"},
    "8. Spanish - Female, Camila": {"preset": "v2/es_speaker_8", "lang": "es"},
    "9. Spanish - Female, Elena": {"preset": "v2/es_speaker_9", "lang": "es"},
    "10. Spanish - Male, Adrián": {"preset": "v2/es_speaker_0", "lang": "es"},

    # --- Italian (Ý) ---
    "1. Italian - Male, Leonardo": {"preset": "v2/it_speaker_1", "lang": "it"},
    "2. Italian - Female, Giulia": {"preset": "v2/it_speaker_2", "lang": "it"},
    "3. Italian - Male, Francesco": {"preset": "v2/it_speaker_3", "lang": "it"},
    "4. Italian - Male, Federico": {"preset": "v2/it_speaker_4", "lang": "it"},
    "5. Italian - Male, Alessandro": {"preset": "v2/it_speaker_5", "lang": "it"},
    "6. Italian - Male, Andrea": {"preset": "v2/it_speaker_6", "lang": "it"},
    "7. Italian - Female, Sofia": {"preset": "v2/it_speaker_7", "lang": "it"},
    "8. Italian - Male, Riccardo": {"preset": "v2/it_speaker_8", "lang": "it"},
    "9. Italian - Female, Vittoria": {"preset": "v2/it_speaker_9", "lang": "it"},
    "10. Italian - Male, Gabriele": {"preset": "v2/it_speaker_0", "lang": "it"},

    # --- Japanese (Nhật Bản) ---
    "1. Japanese - Female, Akari": {"preset": "v2/ja_speaker_1", "lang": "ja"},
    "2. Japanese - Male, Kaito": {"preset": "v2/ja_speaker_2", "lang": "ja"},
    "3. Japanese - Female, Himari": {"preset": "v2/ja_speaker_3", "lang": "ja"},
    "4. Japanese - Female, Sakura": {"preset": "v2/ja_speaker_4", "lang": "ja"},
    "5. Japanese - Female, Hinata": {"preset": "v2/ja_speaker_5", "lang": "ja"},
    "6. Japanese - Male, Hayato": {"preset": "v2/ja_speaker_6", "lang": "ja"},
    "7. Japanese - Female, Misaki": {"preset": "v2/ja_speaker_7", "lang": "ja"},
    "8. Japanese - Female, Rin": {"preset": "v2/ja_speaker_8", "lang": "ja"},
    "9. Japanese - Female, Koharu": {"preset": "v2/ja_speaker_9", "lang": "ja"},
    "10. Japanese - Female, Aoi": {"preset": "v2/ja_speaker_0", "lang": "ja"},

    # --- Korean (Hàn Quốc) ---
    "1. Korean - Male, Ji-ho": {"preset": "v2/ko_speaker_1", "lang": "ko"},
    "2. Korean - Male, Ye-jun": {"preset": "v2/ko_speaker_2", "lang": "ko"},
    "3. Korean - Male, Min-jun": {"preset": "v2/ko_speaker_3", "lang": "ko"},
    "4. Korean - Male, Eun-woo": {"preset": "v2/ko_speaker_4", "lang": "ko"},
    "5. Korean - Male, Seo-joon": {"preset": "v2/ko_speaker_5", "lang": "ko"},
    "6. Korean - Male, Si-woo": {"preset": "v2/ko_speaker_6", "lang": "ko"},
    "7. Korean - Male, Do-yun": {"preset": "v2/ko_speaker_7", "lang": "ko"},
    "8. Korean - Male, Jeong-woo": {"preset": "v2/ko_speaker_8", "lang": "ko"},
    "9. Korean - Male, Ha-joon": {"preset": "v2/ko_speaker_9", "lang": "ko"},
    "10. Korean - Female, Ji-an": {"preset": "v2/ko_speaker_0", "lang": "ko"},

    # --- Chinese (Trung Quốc) ---
    "1. Chinese - Male, Wei": {"preset": "v2/zh_speaker_1", "lang": "zh"},
    "2. Chinese - Male, Zixuan": {"preset": "v2/zh_speaker_2", "lang": "zh"},
    "3. Chinese - Male, Jun": {"preset": "v2/zh_speaker_3", "lang": "zh"},
    "4. Chinese - Female, Mei": {"preset": "v2/zh_speaker_4", "lang": "zh"},
    "5. Chinese - Male, Ming": {"preset": "v2/zh_speaker_5", "lang": "zh"},
    "6. Chinese - Female, Jia": {"preset": "v2/zh_speaker_6", "lang": "zh"},
    "7. Chinese - Female, Yuhan": {"preset": "v2/zh_speaker_7", "lang": "zh"},
    "8. Chinese - Male, Yuze": {"preset": "v2/zh_speaker_8", "lang": "zh"},
    "9. Chinese - Female, Ruoxi": {"preset": "v2/zh_speaker_9", "lang": "zh"},
    "10. Chinese - Male, Lee": {"preset": "v2/zh_speaker_0", "lang": "zh"},

    # --- Portuguese (Bồ Đào Nha) ---
    "1. Portuguese - Male, João": {"preset": "v2/pt_speaker_1", "lang": "pt"},
    "2. Portuguese - Male, Lucas": {"preset": "v2/pt_speaker_2", "lang": "pt"},
    "3. Portuguese - Male, Miguel": {"preset": "v2/pt_speaker_3", "lang": "pt"},
    "4. Portuguese - Male, Gabriel": {"preset": "v2/pt_speaker_4", "lang": "pt"},
    "5. Portuguese - Male, Arthur": {"preset": "v2/pt_speaker_5", "lang": "pt"},
    "6. Portuguese - Male, Rafael": {"preset": "v2/pt_speaker_6", "lang": "pt"},
    "7. Portuguese - Male, Heitor": {"preset": "v2/pt_speaker_7", "lang": "pt"},
    "8. Portuguese - Male, Matheus": {"preset": "v2/pt_speaker_8", "lang": "pt"},
    "9. Portuguese - Male, Davi": {"preset": "v2/pt_speaker_9", "lang": "pt"},
    "10. Portuguese - Male, Gustavo": {"preset": "v2/pt_speaker_0", "lang": "pt"},

    # --- Russian (Nga) ---
    "1. Russian - Male, Alexander": {"preset": "v2/ru_speaker_1", "lang": "ru"},
    "2. Russian - Male, Dmitri": {"preset": "v2/ru_speaker_2", "lang": "ru"},
    "3. Russian - Male, Ivan": {"preset": "v2/ru_speaker_3", "lang": "ru"},
    "4. Russian - Male, Nikolai": {"preset": "v2/ru_speaker_4", "lang": "ru"},
    "5. Russian - Female, Natalia": {"preset": "v2/ru_speaker_5", "lang": "ru"},
    "6. Russian - Female, Victoria": {"preset": "v2/ru_speaker_6", "lang": "ru"},
    "7. Russian - Male, Vladimir": {"preset": "v2/ru_speaker_7", "lang": "ru"},
    "8. Russian - Male, Sergei": {"preset": "v2/ru_speaker_8", "lang": "ru"},
    "9. Russian - Female, Anastasia": {"preset": "v2/ru_speaker_9", "lang": "ru"},
    "10. Russian - Male, Artem": {"preset": "v2/ru_speaker_0", "lang": "ru"},

    # --- Turkish (Thổ Nhỹ Kỳ) ---
    "1. Turkish - Male, Yusuf": {"preset": "v2/tr_speaker_1", "lang": "tr"},
    "2. Turkish - Male, Ali": {"preset": "v2/tr_speaker_2", "lang": "tr"},
    "3. Turkish - Male, Mehmet": {"preset": "v2/tr_speaker_3", "lang": "tr"},
    "4. Turkish - Female, Elif": {"preset": "v2/tr_speaker_4", "lang": "tr"},
    "5. Turkish - Female, Ecrin": {"preset": "v2/tr_speaker_5", "lang": "tr"},
    "6. Turkish - Male, Emir": {"preset": "v2/tr_speaker_6", "lang": "tr"},
    "7. Turkish - Male, Ahmed": {"preset": "v2/tr_speaker_7", "lang": "tr"},
    "8. Turkish - Male, Kerem": {"preset": "v2/tr_speaker_8", "lang": "tr"},
    "9. Turkish - Male, Ali": {"preset": "v2/tr_speaker_9", "lang": "tr"},
    "10. Turkish - Male, Eymen": {"preset": "v2/tr_speaker_0", "lang": "tr"},

    # --- Hindi (Ấn Độ) ---
    "1. Hindi - Male, Rohan": {"preset": "v2/hi_speaker_1", "lang": "hi"},
    "2. Hindi - Male, Kabir": {"preset": "v2/hi_speaker_2", "lang": "hi"},
    "3. Hindi - Female, Diya": {"preset": "v2/hi_speaker_3", "lang": "hi"},
    "4. Hindi - Female, Priya": {"preset": "v2/hi_speaker_4", "lang": "hi"},
    "5. Hindi - Male, Aarav": {"preset": "v2/hi_speaker_5", "lang": "hi"},
    "6. Hindi - Male, Ishaan": {"preset": "v2/hi_speaker_6", "lang": "hi"},
    "7. Hindi - Male, Vivaan": {"preset": "v2/hi_speaker_7", "lang": "hi"},
    "8. Hindi - Male, Reyan": {"preset": "v2/hi_speaker_8", "lang": "hi"},
    "9. Hindi - Female, Tara": {"preset": "v2/hi_speaker_9", "lang": "hi"},
    "10. Hindi - Female, Zara": {"preset": "v2/hi_speaker_0", "lang": "hi"},
}

LANGUAGE_NATIVE_NAMES = {
    "en": "🇬🇧 Anh 🇬🇧",
    "fr": "🇫🇷 Pháp 🇫🇷",
    "de": "🇩🇪 Đức 🇩🇪",
    "es": "🇪🇸 Tây Ban Nha 🇪🇸",
    "it": "🇮🇹 Ý 🇮🇹",
    "ja": "🇯🇵 Nhật Bản 🇯🇵",
    "ko": "🇰🇷 Hàn Quốc 🇰🇷",
    "zh": "🇨🇳 Trung Quốc 🇨🇳",
    "pt": "🇵🇹 Bồ Đào Nha 🇵🇹",
    "ru": "🇷🇺 Nga 🇷🇺",
    "tr": "🇹🇷 Thổ Nhĩ Kỳ 🇹🇷",
    "hi": "🇮🇳 Ấn Độ 🇮🇳",
}

import time

class Timer:
    """Một lớp helper đơn giản để đo lường thời gian thực thi."""
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """Bắt đầu đếm giờ."""
        self.start_time = time.time()

    def stop(self):
        """Dừng đếm giờ."""
        self.end_time = time.time()

    def elapsed_formatted(self):
        """
        Tính toán và trả về thời gian đã trôi qua dưới dạng chuỗi đã được định dạng.
        Ví dụ: "1 phút 25 giây", "5.3 giây".
        """
        if self.start_time is None or self.end_time is None:
            return "Chưa xác định"
        
        elapsed_seconds = self.end_time - self.start_time
        
        minutes = int(elapsed_seconds // 60)
        seconds = elapsed_seconds % 60
        
        if minutes > 0:
            return f"{minutes} phút {seconds:.1f} giây"
        else:
            return f"{seconds:.1f} giây"

def prompt_for_audio_settings(ask_for_speed=False, ask_for_stability=False, ask_for_bass_boost=True):
    """
    Hiển thị lời nhắc để người dùng cấu hình các thông số âm thanh.
    Hàm này có thể hỏi về Tốc độ, Độ ổn định, và Âm trầm một cách linh hoạt.
    
    Returns:
        dict: Một dictionary chứa các giá trị đã được cấu hình.
    """
    settings = {
        'speed': None,
        'stability': None,
        'bass_boost': 0
    }

    # Giá trị mặc định hiển thị cho người dùng
    defaults = {
        'speed': 1.0,
        'stability': 2.0,
        'bass_boost': 0
    }

    # --- Hỏi về Tốc độ (nếu được yêu cầu) ---
    if ask_for_speed:
        while True:
            prompt = f"\n -> Nhập tốc độ nói (ví dụ: 0.9, 1.2). Mặc định [{defaults['speed']}] nhấn (Enter)): "
            speed_input = input(prompt).strip()
            if speed_input == '00': return None # Tín hiệu thoát
            if not speed_input:
                settings['speed'] = None
                break # Người dùng nhấn Enter -> chấp nhận mặc định và thoát vòng lặp
            try:
                settings['speed'] = float(speed_input)
                break # Nhập đúng -> gán giá trị và thoát vòng lặp
            except ValueError:
                print(f"    ❌ Lỗi: Vui lòng chỉ nhập số. Hãy thử lại.")

    # --- Hỏi về Độ ổn định (với vòng lặp validation) ---
    if ask_for_stability:
        while True:
            prompt = f"\n -> Nhập độ ổn định (ví dụ: 2.0, 2.5). Mặc định [{defaults['stability']}] nhấn (Enter)): "
            cfg_input = input(prompt).strip()
            if cfg_input == '00': return None # Tín hiệu thoát
            if not cfg_input:
                settings['stability'] = None
                break # Người dùng nhấn Enter -> chấp nhận mặc định và thoát vòng lặp
            try:
                settings['stability'] = float(cfg_input)
                break # Nhập đúng -> gán giá trị và thoát vòng lặp
            except ValueError:
                print(f"    ❌ Lỗi: Vui lòng chỉ nhập số. Hãy thử lại.")
    
    # --- Hỏi về Âm trầm (với vòng lặp validation) ---
    if ask_for_bass_boost:
        # Giới hạn trong khoảng 0-20
        BASS_BOOST_MIN, BASS_BOOST_MAX = 0, 20
        while True:
            prompt = f"\n -> Nhập mức tăng âm trầm ({BASS_BOOST_MIN}-{BASS_BOOST_MAX}). Mặc định [{defaults['bass_boost']}] nhấn (Enter)): "
            bass_input = input(prompt).strip()
            if bass_input == '00': return None # Tín hiệu thoát
            if not bass_input:
                settings['bass_boost'] = 0
                break # Người dùng nhấn Enter -> chấp nhận mặc định và thoát vòng lặp
            try:
                value = int(bass_input)
                if BASS_BOOST_MIN <= value <= BASS_BOOST_MAX:
                    settings['bass_boost'] = value
                    break # Nhập đúng và trong khoảng -> gán giá trị và thoát vòng lặp
                else:
                    print(f"    ❌ Lỗi: Giá trị phải nằm trong khoảng từ {BASS_BOOST_MIN} đến {BASS_BOOST_MAX}. Hãy thử lại.")
            except ValueError:
                print(f"    ❌ Lỗi: Vui lòng chỉ nhập số nguyên. Hãy thử lại.")

    return settings