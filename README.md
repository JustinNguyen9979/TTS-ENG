# Công Cụ Text-to-Speech Nâng Cao Sử Dụng Suno/Bark

Đây là một công cụ dòng lệnh (CLI) mạnh mẽ được xây dựng bằng Python, cho phép chuyển đổi văn bản thành giọng nói (Text-to-Speech) chất lượng cao bằng cách sử dụng mô hình AI `suno/bark`. Ứng dụng được thiết kế với giao diện tương tác, thân thiện với người dùng và cung cấp nhiều tính năng chuyên nghiệp để tạo và quản lý file âm thanh.

Công cụ này được phát triển bởi **Justin Nguyen 🇻🇳**.

## ✨ Tính Năng Nổi Bật

- **Box Voice Nghe Thử Giọng Nói:** Một menu tương tác cho phép người dùng nghe thử và khám phá hàng trăm giọng nói khác nhau từ nhiều ngôn ngữ.
- **Xử Lý Hàng Loạt (Batch Processing):** Tự động quét các file `.txt` trong thư mục `Input`, xử lý chúng theo thứ tự và lưu kết quả vào thư mục `Output`.
- **Hàng Đợi Thông Minh:** Tự động phát hiện các file mới được thêm vào thư mục `Input` trong quá trình xử lý và thêm chúng vào cuối hàng đợi.
- **Kiểm Tra Phần Cứng:** Tích hợp công cụ chẩn đoán, giúp người dùng kiểm tra thông số hệ thống (CPU, RAM, GPU, VRAM) và xác định xem máy tính có đủ điều kiện để chạy ứng dụng hiệu quả hay không.

## 🚀 Cài Đặt

Để chạy được công cụ này, máy tính của bạn cần đáp ứng các yêu cầu sau.

### Yêu Cầu Hệ Thống

- **Python:** Phiên bản **3.11** được khuyến nghị để đảm bảo tương thích với tất cả các thư viện.
- **Pip:** Trình quản lý gói của Python.
- **FFmpeg:** Một công cụ xử lý đa phương tiện cần thiết cho thư viện `pydub`.
  - **Trên macOS (dùng Homebrew):** `brew install ffmpeg`
  - **Trên Windows:** Tải về từ [trang chủ FFmpeg](https://ffmpeg.org/download.html) và thêm vào biến môi trường PATH.

### Các Bước Cài Đặt

1.  **Tạo và kích hoạt môi trường ảo:** (Rất khuyến khích)
    ```bash
    # Sử dụng đúng phiên bản python 3.11
    python3.11 -m venv venv
    ```
    - **Trên macOS/Linux:**
      ```bash
      source venv/bin/activate
      ```
    - **Trên Windows:**
      ```bash
      .\venv\Scripts\activate
      ```

2.  **Cài đặt các thư viện cần thiết:**
    Tất cả các gói phụ thuộc đã được liệt kê trong file `requirements.txt`. Chạy lệnh sau:
    ```bash
    pip install -r requirements.txt
    ```
    *Lưu ý: Để tối ưu hóa cho GPU NVIDIA, hãy đảm bảo bạn đã cài đặt phiên bản PyTorch hỗ trợ CUDA theo hướng dẫn trên trang chủ PyTorch.*

## ⚙️ Hướng Dẫn Sử Dụng

Sau khi cài đặt thành công, bạn có thể khởi chạy công cụ bằng một lệnh duy nhất.

1.  **Chạy ứng dụng:**
    ```bash
    python3 app.py
    ```
    Chương trình sẽ khởi động, tải mô hình AI (có thể mất vài phút ở lần chạy đầu tiên) và hiển thị menu chính.

2.  **Các Chức Năng Chính:**
    - **1. Nghe thử các giọng nói (Box Voice):**
      - Hiển thị menu chọn ngôn ngữ, sau đó là danh sách các giọng nói có sẵn.
      - Chọn một giọng để nghe thử. Âm thanh sẽ được tạo và lưu vào cache ở lần đầu, và phát ngay lập tức ở những lần sau.
    - **2. Tạo âm thanh từ file (Text To Speech):**
      - Đặt các file `.txt` của bạn (ví dụ: `1_Chapter1.txt`, `2_Chapter2.txt`) vào thư mục `Input`.
      - Chọn chức năng này, chương trình sẽ tự động tìm và xử lý tất cả các file theo thứ tự.
      - File âm thanh đầu ra sẽ được lưu trong thư mục `Output`.
    - **3. Kiểm tra phần cứng:**
      - Hiển thị một báo cáo chi tiết về phần cứng máy tính của bạn và đưa ra kết luận xem máy có đủ điều kiện để chạy mượt mà hay không.
    - **4. Thông tin tác giả:**
      - Hiển thị thông tin về người phát triển và các công nghệ đã được sử dụng.
    - **5. Thoát chương trình.**

## 📂 Cấu Trúc Dự Án

```
project_voice/
│
├── audio_cache/          # Lưu cache 
├── Input/                # Chứa các file .txt đầu vào
├── Output/               # Chứa các file .wav đầu ra
│
├── config.py             # Cấu hình giọng nói, văn bản mẫu, yêu cầu hệ thống
├── tts_utils.py          # Các hàm cốt lõi liên quan đến model TTS
├── box_voice.py          # Logic cho chức năng "Nghe thử"
├── file_tts.py           # Logic cho chức năng "Xử lý hàng loạt"
├── hardware_check.py     # Logic cho chức năng "Kiểm tra phần cứng"
├── ui.py                 # Quản lý giao diện người dùng (banner, menu)
├── about.py              # Logic cho màn hình "Thông tin tác giả"
├── app.py                # Điểm khởi đầu của ứng dụng
└── requirements.txt      # Danh sách các thư viện cần thiết
```

---
## ❤️ Ủng Hộ Tác Giả

Công cụ này được phát triển và duy trì hoàn toàn miễn phí. Nếu bạn thấy nó hữu ích và muốn hỗ trợ tác giả để có thêm động lực phát triển các dự án mã nguồn mở khác, bạn có thể ủng hộ qua các kênh dưới đây. Sự ủng hộ của bạn, dù nhỏ, cũng là một nguồn động viên to lớn.

Xin chân thành cảm ơn!

| Kênh | Thông Tin |
| :--- | :--- |
| 🏦 **MB Bank** | **STK:** `079 88888 88888` <br> **Tên:** NGUYEN DUC HUY |
| 📱 **Momo** | `0982 579 098` |
| 🌐 **PayPal** | KZN2CVN5QM9EN |

## 📬 Thông Tin Liên Lạc

- **Telegram:** [@Justin_Nguyen_SG](https://t.me/Justin_Nguyen_SG)