# Công Cụ Giọng Nói AI Đa Năng

Đây là một công cụ dòng lệnh (CLI) mạnh mẽ được xây dựng bằng Python, tích hợp nhiều mô hình AI hàng đầu để cung cấp một bộ giải pháp toàn diện về giọng nói. Ứng dụng cho phép tạo giọng nói, nhân bản giọng nói và phiên âm audio với giao diện tương tác, thân thiện.

Các công nghệ AI cốt lõi bao gồm:
- **`suno/bark`**: Dùng cho việc tạo giọng nói (Text-to-Speech) đa dạng.
- **`F5-TTS`**: Dùng cho chức năng nhân bản giọng nói (Voice Cloning) chất lượng cao.
- **`OpenAI-Whisper`**: Dùng cho việc chuyển đổi giọng nói thành văn bản (Transcribe) chính xác.

Công cụ này được phát triển bởi **Justin Nguyen 🇻🇳**.

## ✨ Tính Năng Nổi Bật

- **Nghe Thử Giọng Nói (Box Voice):** Một menu tương tác cho phép người dùng nghe thử và khám phá hàng trăm giọng nói khác nhau từ nhiều ngôn ngữ của mô hình Bark.
- **Tạo Giọng Nói (File TTS):** Tự động quét các file `.txt` trong thư mục `Input`, xử lý chúng theo thứ tự và lưu kết quả vào thư mục `Output`.
- **Nhân Bản Giọng Nói (Voice Cloning):** Sử dụng mô hình F5-TTS, cho phép bạn sao chép một giọng nói bất kỳ từ một file âm thanh mẫu và dùng giọng đó để đọc một văn bản mới.
- **Chuyển Giọng Nói Thành Văn Bản (Transcribe Audio):** Tích hợp OpenAI Whisper để tự động phiên âm các file âm thanh (`.mp3`, `.wav`) thành file văn bản (`.txt`), với tùy chọn nhiều model có độ chính xác khác nhau.

## 🚀 Cài Đặt

Để chạy được công cụ này, máy tính của bạn cần đáp ứng các yêu cầu sau.

### Yêu Cầu Hệ Thống

- **Python:** Phiên bản **3.11** được khuyến nghị để đảm bảo tương thích với tất cả các thư viện.
- **Pip:** Trình quản lý gói của Python.
- **FFmpeg:** Một công cụ xử lý đa phương tiện cần thiết.
  - **Trên macOS (dùng Homebrew):** `brew install ffmpeg`
  - **Trên Windows:** Tải về từ [trang chủ FFmpeg](https://ffmpeg.org/download.html) và thêm vào biến môi trường PATH.

### Các Bước Cài Đặt

1.  **Tạo và kích hoạt môi trường ảo:** (Rất khuyến khích)
    ```bash
    # Đảm bảo bạn đang sử dụng đúng phiên bản python
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
    Tất cả các gói phụ thuộc đã được liệt kê trong file `requirements.txt` (hoặc `pyproject.toml`). Chạy lệnh sau:
    ```bash
    pip install -r requirements.txt
    ```
    *Lưu ý: Để tối ưu hóa cho GPU NVIDIA, hãy đảm bảo bạn đã cài đặt phiên bản PyTorch hỗ trợ CUDA theo hướng dẫn trên trang chủ PyTorch.*

## ⚙️ Hướng Dẫn Sử Dụng

Sau khi cài đặt thành công, bạn có thể khởi chạy công cụ bằng một lệnh duy nhất.

1.  **Chạy ứng dụng:**
    ```bash
    python3 main.py 
    ```
    *(Hoặc tên file thực thi chính của bạn)*

    Chương trình sẽ khởi động, tải các mô hình AI cần thiết (có thể mất vài phút ở lần chạy đầu tiên) và hiển thị menu chính.

2.  **Các Chức Năng Chính:**
    - **[1]. Nghe thử giọng nói (Box Voice):**
      - Hiển thị menu chọn ngôn ngữ, sau đó là danh sách các giọng nói có sẵn để bạn nghe thử.
    - **[2]. Tạo giọng nói (Text To Speech):**
      - Đặt các file `.txt` của bạn vào thư mục `Input`.
      - Chương trình sẽ tự động tìm và xử lý tất cả các file.
    - **[3]. Nhân bản giọng nói (Clone Voice):**
      - Đặt một file âm thanh mẫu (`.wav` hoặc `.mp3`) và một file `.txt` chứa nội dung của audio đó vào thư mục `Voice`.
      - Đặt các file văn bản bạn muốn đọc bằng giọng đã nhân bản vào thư mục `Input`.
    - **[4]. Chuyển giọng nói thành văn bản (Transcribe Audio):**
      - Cung cấp một menu để bạn chọn độ chính xác của model Whisper.
      - Đặt các file âm thanh (`.mp3`, `.wav`) vào thư mục `Input`.
      - Công cụ sẽ tự động tạo ra các file `.txt` tương ứng trong thư mục `Output`.
    - **[5]. Thông tin & Giới thiệu (About):**
      - Hiển thị thông tin về người phát triển và các công nghệ đã sử dụng.
    - **[0]. Thoát chương trình (Exit).**


---
## ❤️ Ủng Hộ Tác Giả

Công cụ này là kết quả của nhiều giờ nghiên cứu và phát triển tâm huyết, được bảo hộ bởi bản quyền. Tác giả hoan nghênh việc sử dụng công cụ cho các mục đích khác nhau, tuy nhiên xin vui lòng tuân thủ các điều khoản dưới đây:
  - Đối với mục đích sử dụng cá nhân, nghiên cứu hoặc học thuật: Nếu bạn thấy công cụ hữu ích, một khoản đóng góp để ủng hộ dự án sẽ là nguồn động viên to lớn, giúp tác giả có thêm nguồn lực để duy trì và phát triển các tính năng mới.
  - Đối với mục đích kinh doanh hoặc thương mại: Mọi hình thức tích hợp vào sản phẩm, cung cấp dịch vụ hoặc sử dụng nhằm tạo ra lợi nhuận đều yêu cầu phải có giấy phép sử dụng (license). Vui lòng liên hệ trực tiếp với tác giả để trao đổi và mua giấy phép phù hợp.
Sự ủng hộ của bạn, dù qua hình thức đóng góp hay mua giấy phép, đều là sự công nhận quý giá cho công sức và tâm huyết đã đầu tư vào dự án.

Xin chân thành cảm ơn!

| Kênh | Thông Tin |
| :--- | :--- |
| 🏦 **MB Bank** | **STK:** `079 88888 88888` <br> **Tên:** NGUYEN DUC HUY |
| 📱 **Momo** | `0982 579 098` |
| 🌐 **PayPal** | KZN2CVN5QM9EN |

## 📬 Thông Tin Liên Lạc

- **Telegram:** [@Justin_Nguyen_SG](https://t.me/Justin_Nguyen_SG)