# config.py

MIN_RAM_GB = 8
MIN_VRAM_GB = 6

# Đoạn văn bản mẫu để nghe thử trong Jukebox
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
    # Thêm các ngôn ngữ khác nếu muốn
}

# Danh sách các giọng nói có sẵn
VOICE_PRESETS = {
    # --- English (1-10) (Anh) ---
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


    # --- French (11-20) (Pháp) ---
    "11. French - Female, Alice": {"preset": "v2/fr_speaker_1", "lang": "fr"},
    "12. French - Female, Léa": {"preset": "v2/fr_speaker_2", "lang": "fr"},
    "13. French - Male, Jules": {"preset": "v2/fr_speaker_3", "lang": "fr"},
    "14. French - Male, Ethan": {"preset": "v2/fr_speaker_4", "lang": "fr"},
    "15. French - Female, Louise": {"preset": "v2/fr_speaker_5", "lang": "fr"},
    "16. French - Male, Hugo": {"preset": "v2/fr_speaker_6", "lang": "fr"},
    "17. French - Male, Léo": {"preset": "v2/fr_speaker_7", "lang": "fr"},
    "18. French - Male, Lucas": {"preset": "v2/fr_speaker_8", "lang": "fr"},
    "19. French - Male, Raphaël": {"preset": "v2/fr_speaker_9", "lang": "fr"},
    "20. French - Male, Nathan": {"preset": "v2/fr_speaker_0", "lang": "fr"},

    # --- German (21-30) (Đức) ---
    "21. German - Male, Lukas": {"preset": "v2/de_speaker_1", "lang": "de"},
    "22. German - Male, Maximilian": {"preset": "v2/de_speaker_2", "lang": "de"},
    "23. German - Female, Hanna": {"preset": "v2/de_speaker_3", "lang": "de"},
    "24. German - Male, Leon": {"preset": "v2/de_speaker_4", "lang": "de"},
    "25. German - Male, Finn": {"preset": "v2/de_speaker_5", "lang": "de"},
    "26. German - Male, Felix": {"preset": "v2/de_speaker_6", "lang": "de"},
    "27. German - Male, Paul": {"preset": "v2/de_speaker_7", "lang": "de"},
    "28. German - Female, Emma": {"preset": "v2/de_speaker_8", "lang": "de"},
    "29. German - Male, Noah": {"preset": "v2/de_speaker_9", "lang": "de"},
    "30. German - Female, Julian": {"preset": "v2/de_speaker_0", "lang": "de"},

    # --- Spanish (31-40) (Tây Ban Nha) ---
    "31. Spanish - Male, Santiago": {"preset": "v2/es_speaker_1", "lang": "es"},
    "32. Spanish - Female, Sofía": {"preset": "v2/es_speaker_2", "lang": "es"},
    "33. Spanish - Male, Mateo": {"preset": "v2/es_speaker_3", "lang": "es"},
    "34. Spanish - Female, Valentina": {"preset": "v2/es_speaker_4", "lang": "es"},
    "35. Spanish - Male, Alejandro": {"preset": "v2/es_speaker_5", "lang": "es"},
    "36. Spanish - Female, Isabella": {"preset": "v2/es_speaker_6", "lang": "es"},
    "37. Spanish - Male, Sebastián": {"preset": "v2/es_speaker_7", "lang": "es"},
    "38. Spanish - Female, Camila": {"preset": "v2/es_speaker_8", "lang": "es"},
    "39. Spanish - Male, Diego": {"preset": "v2/es_speaker_9", "lang": "es"},
    "40. Spanish - Female, Martina": {"preset": "v2/es_speaker_0", "lang": "es"},

    # --- Italian (41-50) (Ý) ---
    "41. Italian - Male, Leonardo": {"preset": "v2/it_speaker_1", "lang": "it"},
    "42. Italian - Female, Giulia": {"preset": "v2/it_speaker_2", "lang": "it"},
    "43. Italian - Male, Francesco": {"preset": "v2/it_speaker_3", "lang": "it"},
    "44. Italian - Female, Sofia": {"preset": "v2/it_speaker_4", "lang": "it"},
    "45. Italian - Male, Alessandro": {"preset": "v2/it_speaker_5", "lang": "it"},
    "46. Italian - Female, Aurora": {"preset": "v2/it_speaker_6", "lang": "it"},
    "47. Italian - Male, Lorenzo": {"preset": "v2/it_speaker_7", "lang": "it"},
    "48. Italian - Female, Ginevra": {"preset": "v2/it_speaker_8", "lang": "it"},
    "49. Italian - Male, Mattia": {"preset": "v2/it_speaker_9", "lang": "it"},
    "50. Italian - Female, Alice": {"preset": "v2/it_speaker_0", "lang": "it"},

    # --- Japanese (51-60) (Nhật Bản) ---
    "51. Japanese - Female, Akari": {"preset": "v2/ja_speaker_1", "lang": "ja"},
    "52. Japanese - Male, Kaito": {"preset": "v2/ja_speaker_2", "lang": "ja"},
    "53. Japanese - Female, Himari": {"preset": "v2/ja_speaker_3", "lang": "ja"},
    "54. Japanese - Female, Sakura": {"preset": "v2/ja_speaker_4", "lang": "ja"},
    "55. Japanese - Male, Sora": {"preset": "v2/ja_speaker_5", "lang": "ja"},
    "56. Japanese - Female, Yui": {"preset": "v2/ja_speaker_6", "lang": "ja"},
    "57. Japanese - Male, Riku": {"preset": "v2/ja_speaker_7", "lang": "ja"},
    "58. Japanese - Female, Rin": {"preset": "v2/ja_speaker_8", "lang": "ja"},
    "59. Japanese - Male, Yuki": {"preset": "v2/ja_speaker_9", "lang": "ja"},
    "60. Japanese - Female, Aoi": {"preset": "v2/ja_speaker_0", "lang": "ja"},

    # --- Korean (61-70) (Hàn Quốc) ---
    "61. Korean - Male, Ji-ho": {"preset": "v2/ko_speaker_1", "lang": "ko"},
    "62. Korean - Female, Ji-woo": {"preset": "v2/ko_speaker_2", "lang": "ko"},
    "63. Korean - Male, Min-jun": {"preset": "v2/ko_speaker_3", "lang": "ko"},
    "64. Korean - Female, Seo-yeon": {"preset": "v2/ko_speaker_4", "lang": "ko"},
    "65. Korean - Male, Seo-joon": {"preset": "v2/ko_speaker_5", "lang": "ko"},
    "66. Korean - Female, Ha-yoon": {"preset": "v2/ko_speaker_6", "lang": "ko"},
    "67. Korean - Male, Do-yun": {"preset": "v2/ko_speaker_7", "lang": "ko"},
    "68. Korean - Female, Seo-ah": {"preset": "v2/ko_speaker_8", "lang": "ko"},
    "69. Korean - Male, Ha-joon": {"preset": "v2/ko_speaker_9", "lang": "ko"},
    "70. Korean - Female, Ji-an": {"preset": "v2/ko_speaker_0", "lang": "ko"},

    # --- Chinese (71-80) (Trung Quốc) ---
    "71. Chinese - Male, Wei": {"preset": "v2/zh_speaker_1", "lang": "zh"},
    "72. Chinese - Female, Lin": {"preset": "v2/zh_speaker_2", "lang": "zh"},
    "73. Chinese - Male, Jun": {"preset": "v2/zh_speaker_3", "lang": "zh"},
    "74. Chinese - Female, Mei": {"preset": "v2/zh_speaker_4", "lang": "zh"},
    "75. Chinese - Male, Ming": {"preset": "v2/zh_speaker_5", "lang": "zh"},
    "76. Chinese - Female, Jia": {"preset": "v2/zh_speaker_6", "lang": "zh"},
    "77. Chinese - Male, Hao": {"preset": "v2/zh_speaker_7", "lang": "zh"},
    "78. Chinese - Female, Fang": {"preset": "v2/zh_speaker_8", "lang": "zh"},
    "79. Chinese - Male, Lee": {"preset": "v2/zh_speaker_9", "lang": "zh"},
    "80. Chinese - Female, Jing": {"preset": "v2/zh_speaker_0", "lang": "zh"},

    # --- Portuguese (81-90) (Bồ Đào Nha) ---
    "81. Portuguese - Male, João": {"preset": "v2/pt_speaker_1", "lang": "pt"},
    "82. Portuguese - Female, Maria": {"preset": "v2/pt_speaker_2", "lang": "pt"},
    "83. Portuguese - Male, Miguel": {"preset": "v2/pt_speaker_3", "lang": "pt"},
    "84. Portuguese - Female, Alice": {"preset": "v2/pt_speaker_4", "lang": "pt"},
    "85. Portuguese - Male, Arthur": {"preset": "v2/pt_speaker_5", "lang": "pt"},
    "86. Portuguese - Female, Helena": {"preset": "v2/pt_speaker_6", "lang": "pt"},
    "87. Portuguese - Male, Heitor": {"preset": "v2/pt_speaker_7", "lang": "pt"},
    "88. Portuguese - Female, Laura": {"preset": "v2/pt_speaker_8", "lang": "pt"},
    "89. Portuguese - Male, Davi": {"preset": "v2/pt_speaker_9", "lang": "pt"},
    "90. Portuguese - Female, Manuela": {"preset": "v2/pt_speaker_0", "lang": "pt"},

    # --- Russian (91-100) (Nga) ---
    "91. Russian - Male, Alexander": {"preset": "v2/ru_speaker_1", "lang": "ru"},
    "92. Russian - Female, Anastasia": {"preset": "v2/ru_speaker_2", "lang": "ru"},
    "93. Russian - Male, Ivan": {"preset": "v2/ru_speaker_3", "lang": "ru"},
    "94. Russian - Female, Sofia": {"preset": "v2/ru_speaker_4", "lang": "ru"},
    "95. Russian - Male, Mikhail": {"preset": "v2/ru_speaker_5", "lang": "ru"},
    "96. Russian - Female, Anna": {"preset": "v2/ru_speaker_6", "lang": "ru"},
    "97. Russian - Male, Dmitri": {"preset": "v2/ru_speaker_7", "lang": "ru"},
    "98. Russian - Female, Maria": {"preset": "v2/ru_speaker_8", "lang": "ru"},
    "99. Russian - Male, Artem": {"preset": "v2/ru_speaker_9", "lang": "ru"},
    "100. Russian - Female, Victoria": {"preset": "v2/ru_speaker_0", "lang": "ru"},

    # --- Turkish (101-110) (Thổ Nhỹ Kỳ) ---
    "101. Turkish - Male, Yusuf": {"preset": "v2/tr_speaker_1", "lang": "tr"},
    "102. Turkish - Female, Zeynep": {"preset": "v2/tr_speaker_2", "lang": "tr"},
    "103. Turkish - Male, Mehmet": {"preset": "v2/tr_speaker_3", "lang": "tr"},
    "104. Turkish - Female, Elif": {"preset": "v2/tr_speaker_4", "lang": "tr"},
    "105. Turkish - Male, Mustafa": {"preset": "v2/tr_speaker_5", "lang": "tr"},
    "106. Turkish - Female, Asya": {"preset": "v2/tr_speaker_6", "lang": "tr"},
    "107. Turkish - Male, Ahmed": {"preset": "v2/tr_speaker_7", "lang": "tr"},
    "108. Turkish - Female, Defne": {"preset": "v2/tr_speaker_8", "lang": "tr"},
    "109. Turkish - Male, Ali": {"preset": "v2/tr_speaker_9", "lang": "tr"},
    "110. Turkish - Female, Miray": {"preset": "v2/tr_speaker_0", "lang": "tr"},

    # --- Hindi (111-120) (Ấn Độ) ---
    "111. Hindi - Male, Rohan": {"preset": "v2/hi_speaker_1", "lang": "hi"},
    "112. Hindi - Female, Diya": {"preset": "v2/hi_speaker_2", "lang": "hi"},
    "113. Hindi - Male, Arjun": {"preset": "v2/hi_speaker_3", "lang": "hi"},
    "114. Hindi - Female, Priya": {"preset": "v2/hi_speaker_4", "lang": "hi"},
    "115. Hindi - Male, Aarav": {"preset": "v2/hi_speaker_5", "lang": "hi"},
    "116. Hindi - Female, Anika": {"preset": "v2/hi_speaker_6", "lang": "hi"},
    "117. Hindi - Male, Vivaan": {"preset": "v2/hi_speaker_7", "lang": "hi"},
    "118. Hindi - Female, Saanvi": {"preset": "v2/hi_speaker_8", "lang": "hi"},
    "119. Hindi - Male, Aditya": {"preset": "v2/hi_speaker_9", "lang": "hi"},
    "120. Hindi - Female, Zara": {"preset": "v2/hi_speaker_0", "lang": "hi"},
}

# Tên thư mục cache
CACHE_DIR = "audio_cache"

LANGUAGE_NATIVE_NAMES = {
    "en": "Anh",
    "fr": "Pháp",
    "de": "Đức",
    "es": "Tây Ban Nha",
    "it": "Ý",
    "ja": "Nhật",
    "ko": "Hàn Quốc",
    "zh": "Trung Quốc",
    "pt": "Bồ Đào Nha",
    "ru": "Nga",
    "tr": "Thổ Nhĩ Kỳ",
    "hi": "Ấn Độ",
}
