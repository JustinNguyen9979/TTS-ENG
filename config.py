# config.py

MIN_RAM_GB = 8
MIN_VRAM_GB = 6

# Đoạn văn bản mẫu để nghe thử trong Jukebox
TEXT_SAMPLES = {
    "en": "A very warm welcome to you! It is a genuine pleasure to have you with us today. I sincerely hope you've been having a wonderful day so far and that the rest of your time here is enjoyable and productive.",
    "fr": "Bonjour et bienvenue ! Je suis absolument ravi(e) de vous accueillir parmi nous. J'espère sincèrement que votre journée se déroule bien jusqu'à présent et je vous souhaite de passer un excellent moment en notre compagnie. Comment allez-vous ?",
    "ja": "はじめまして。本日はようこそお越しくださいました。皆様にお会いできて大変光栄に存じます。これから素晴らしい時間を共に過ごせることを心より楽しみにしております。どうぞ、よろしくお願いいたします。",
    "zh": "大家好！非常欢迎各位的光临，我们在此怀着无比激动的心情迎接您的到来。希望您旅途顺利，并能在这里度过一段愉快而难忘的时光。我们期待与您共创美好回忆。",
    # Thêm các ngôn ngữ khác nếu muốn
}

# Danh sách các giọng nói có sẵn
VOICE_PRESETS = {
    "1. English - Male, Drake (Phổ biến)": {"preset": "v2/en_speaker_6", "lang": "en"},
    "2. English - Female, Venus": {"preset": "v2/en_speaker_9", "lang": "en"},
    "3. English - Male, Brian": {"preset": "v2/en_speaker_2", "lang": "en"}, 
    "4. French - Female, Charlotte": {"preset": "v2/fr_speaker_5", "lang": "fr"},
    "5. Japanese - Female, Rin": {"preset": "v2/ja_speaker_3", "lang": "ja"},
    "6. Chinese - Male, Lee": {"preset": "v2/zh_speaker_5", "lang": "zh"},
}

# Tên thư mục cache
CACHE_DIR = "audio_cache"
