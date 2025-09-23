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

- **Hệ điều hành:** macOS hoặc Windows.
- **Python:** Phiên bản **3.11** được khuyến nghị để đảm bảo tương thích.
- **Pip:** Trình quản lý gói của Python.
- **Git:** Cần thiết cho một số thư viện phụ thuộc. Tải về tại [git-scm.com](https://git-scm.com/download/win).
- **GPU (Khuyến nghị):**
  - **NVIDIA:** Card đồ họa hỗ trợ CUDA để tăng tốc xử lý AI.
  - **Apple Silicon (M1/M2/M3):** Hỗ trợ tăng tốc qua MPS.

### Bước 1: Cài đặt FFmpeg (Bắt buộc)

FFmpeg là một công cụ xử lý đa phương tiện cần thiết cho việc đọc và ghi file âm thanh.

#### Trên macOS (dùng Homebrew)
```bash
brew install ffmpeg
```

#### Trên Windows (Hướng dẫn chi tiết)
1.  **Tải FFmpeg:**
    -   Truy cập [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/).
    -   Tìm đến mục **"release builds"** và tải về file `ffmpeg-release-full.7z` hoặc `.zip`.

2.  **Giải nén và Di chuyển:**
    -   Giải nén file vừa tải.
    -   Đổi tên thư mục giải nén thành `ffmpeg` cho gọn.
    -   Di chuyển thư mục `ffmpeg` này vào một nơi cố định, ví dụ như thư mục gốc của ổ `C:\`. Kết quả bạn sẽ có `C:\ffmpeg`.

3.  **Thêm FFmpeg vào biến môi trường PATH:**
    -   Nhấn phím **Windows**, gõ `environment variables`, và chọn **"Edit the system environment variables"**.
    -   Trong cửa sổ mới, nhấn vào **"Environment Variables..."**.
    -   Trong khung **"System variables"**, tìm và chọn biến `Path`, sau đó nhấn **"Edit..."**.
    -   Nhấn **"New"**, sau đó dán đường dẫn đầy đủ đến thư mục `bin` của FFmpeg vào. Ví dụ: **`C:\ffmpeg\bin`**.
    -   Nhấn **OK** trên tất cả các cửa sổ để lưu lại.

4.  **Kiểm tra:**
    -   **Đóng tất cả các cửa sổ terminal và mở lại một cái mới.**
    -   Gõ lệnh `ffmpeg -version`. Nếu bạn thấy thông tin phiên bản hiện ra, bạn đã cài đặt thành công.

### Bước 2: Cài đặt CUDA và PyTorch (Tùy chọn, cho GPU NVIDIA)

Nếu bạn có card đồ họa NVIDIA, việc cài đặt CUDA sẽ giúp tăng tốc độ xử lý lên rất nhiều lần.

1.  **Kiểm tra phiên bản Driver và CUDA được hỗ trợ:**
    -   Mở Command Prompt và gõ lệnh: `nvidia-smi`.
    -   Nhìn vào góc trên bên phải, bạn sẽ thấy phiên bản CUDA tối đa mà driver của bạn hỗ trợ (ví dụ: `CUDA Version: 12.2`). Bạn nên cài đặt phiên bản CUDA bằng hoặc thấp hơn số này.

2.  **Cài đặt NVIDIA CUDA Toolkit:**
    -   Truy cập [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive).
    -   Tìm và tải về phiên bản CUDA phù hợp với máy của bạn (ví dụ: CUDA Toolkit 11.8).
    -   Chạy file cài đặt và làm theo các bước hướng dẫn (chọn "Express installation" là cách dễ nhất).

3.  **Cài đặt PyTorch với CUDA:**
    -   Truy cập trang chủ PyTorch: [pytorch.org](https://pytorch.org/).
    -   Sử dụng công cụ chọn lệnh, ví dụ:
        -   **PyTorch Build:** Stable
        -   **Your OS:** Windows
        -   **Package:** Pip
        -   **Language:** Python
        -   **Compute Platform:** Chọn phiên bản CUDA bạn vừa cài (ví dụ: CUDA 11.8).
    -   Sao chép lệnh được tạo ra. Nó sẽ trông giống như sau:
      ```bash
      pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
      ```
    -   **Quan trọng:** Trước khi chạy lệnh này, hãy gỡ cài đặt phiên bản PyTorch cũ (nếu có): `pip uninstall torch torchvision torchaudio`.
    -   Chạy lệnh cài đặt PyTorch mới trong terminal đã kích hoạt môi trường ảo.

### Bước 3: Cài đặt các thư viện còn lại

1.  **Tạo và kích hoạt môi trường ảo:** (Rất khuyến khích)
    ```bash
    # Đảm bảo bạn đang sử dụng đúng phiên bản python
    python3.11 -m venv venv
    ```
    - **Trên macOS/Linux:**
      ```bash
      # Kích hoạt
      source venv/bin/activate

      # Để thoát sau khi dùng xong
      deactivate
      ```
    - **Trên Windows:**
      ```bash
      # Kích hoạt
      .\venv\Scripts\activate

      # Để thoát sau khi dùng xong
      deactivate
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