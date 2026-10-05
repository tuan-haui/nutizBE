# Hướng dẫn Test API - YouTube Media Backend

FastAPI tự động sinh tài liệu Swagger UI (Interactive API Docs). Bạn có thể test trực tiếp tất cả các API ngay trên trình duyệt mà không cần cài đặt thêm Postman.

**👉 Truy cập Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)  
*(Đảm bảo server đang chạy trước khi truy cập)*

Dưới đây là các ví dụ sử dụng **cURL** để gọi API trực tiếp từ Terminal.

---

## 1. Health Checks
Kiểm tra xem server và các dependencies (FFmpeg, yt-dlp) đã sẵn sàng chưa.

**GET /api/v1/health**
```bash
curl -X GET "http://localhost:8000/api/v1/health" -H "accept: application/json"
```

**GET /api/v1/health/dependencies**
```bash
curl -X GET "http://localhost:8000/api/v1/health/dependencies" -H "accept: application/json"
```

---

## 2. YouTube Metadata
Lấy thông tin và danh sách formats của một video (Không tốn nhiều tài nguyên, không download).

**GET /api/v1/youtube/info**
```bash
curl -X GET "http://localhost:8000/api/v1/youtube/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" -H "accept: application/json"
```

**POST /api/v1/youtube/formats**
```bash
curl -X POST "http://localhost:8000/api/v1/youtube/formats" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

## 3. Extract Media URL (Nhanh)
Lấy đường link stream trực tiếp (có thời hạn ngắn) từ YouTube. Phù hợp cho việc phát Audio trên FE (Web Audio API) mà không qua download.

**POST /api/v1/youtube/extract**
```bash
curl -X POST "http://localhost:8000/api/v1/youtube/extract" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "type": "audio"}'
```

---

## 4. Karaoke Workflow
API được tối ưu đặc biệt cho nhu cầu tìm kiếm và phát karaoke.

**GET /api/v1/karaoke/search**
```bash
curl -X GET "http://localhost:8000/api/v1/karaoke/search?q=Anh+Trai+Say+Hi" -H "accept: application/json"
```

**POST /api/v1/karaoke/resolve**
```bash
curl -X POST "http://localhost:8000/api/v1/karaoke/resolve" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

## 5. Tải file (Background Job Workflow)
Bởi vì việc tải video mất nhiều thời gian, API sử dụng mô hình Async Worker (Redis Queue). Quá trình sẽ diễn ra theo 3 bước.

### Bước 1: Yêu cầu tải (Nhận về Job ID)
**POST /api/v1/media/audio**
```bash
curl -X POST "http://localhost:8000/api/v1/media/audio" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "format": "mp3", "quality": "192"}'
```
*Kết quả trả về sẽ có dạng: `{"job_id": "xxxxx-xxxx-xxxx", "status": "queued"}`*

### Bước 2: Kiểm tra trạng thái Job
Sử dụng `job_id` nhận được ở Bước 1.

**GET /api/v1/jobs/{job_id}**
```bash
# Thay thế {job_id} bằng ID thực tế
curl -X GET "http://localhost:8000/api/v1/jobs/xxxxx-xxxx-xxxx" -H "accept: application/json"
```
*Nếu status là `completed`, bạn có thể lấy file ở bước tiếp theo.*

### Bước 3: Lấy File Audio/Video hoàn chỉnh
**GET /api/v1/jobs/{job_id}/download**
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/xxxxx-xxxx-xxxx/download" --output my_audio.mp3
```

---

## 6. Chuyển đổi / Trim Audio qua FFmpeg
Áp dụng cho các job tải về đã thành công (có file ở local storage). 

**POST /api/v1/media/audio/trim**
```bash
curl -X POST "http://localhost:8000/api/v1/media/audio/trim" \
     -H "Content-Type: application/json" \
     -d '{"job_id": "ID_CUẢ_JOB_ĐÃ_COMPLETED", "start": 30, "end": 60}'
```
*(Tiếp tục gọi API kiểm tra trạng thái job bằng ID trả về để biết khi nào hoàn thành)*
