\# FastAPI YouTube Media Backend — Development Plan



\## 1. Mục tiêu



Xây dựng một Backend Python sử dụng \*\*FastAPI\*\* làm media service cho ứng dụng karaoke `iloveu.studio`.



Backend chịu trách nhiệm:



\- Tương tác với YouTube thông qua `yt-dlp`.

\- Lấy metadata video.

\- Extract thông tin các media format.

\- Lấy URL stream phù hợp.

\- Download audio/video khi cần.

\- Convert media bằng FFmpeg.

\- Quản lý các tác vụ xử lý media nặng theo dạng background job.

\- Cung cấp REST API cho Angular FE.

\- Không expose trực tiếp logic `yt-dlp` cho browser.

\- Có khả năng mở rộng sang các nguồn media khác mà `yt-dlp` hỗ trợ.



\---



\# 2. Kiến trúc tổng thể



```text

&#x20;                        ┌─────────────────────┐

&#x20;                        │     Angular FE      │

&#x20;                        │    iloveu.studio    │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   │ HTTPS / REST API

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │      FastAPI        │

&#x20;                        │    Media Service    │

&#x20;                        ├─────────────────────┤

&#x20;                        │                     │

&#x20;                        │ YouTube API         │

&#x20;                        │ Download API        │

&#x20;                        │ Stream API          │

&#x20;                        │ Audio API           │

&#x20;                        │ Job API             │

&#x20;                        └───────┬──────┬──────┘

&#x20;                                │      │

&#x20;                   ┌────────────┘      └──────────────┐

&#x20;                   ▼                                   ▼

&#x20;             ┌───────────┐                       ┌───────────┐

&#x20;             │  yt-dlp   │                       │  FFmpeg   │

&#x20;             └─────┬─────┘                       └─────┬─────┘

&#x20;                   │                                   │

&#x20;                   ▼                                   ▼

&#x20;               YouTube                            Media files

```



\---



\# 3. Công nghệ



\## Backend



\- Python 3.12+

\- FastAPI

\- Uvicorn

\- Pydantic v2

\- yt-dlp

\- FFmpeg



\## Optional



\- Redis

\- Celery / RQ / Dramatiq

\- PostgreSQL

\- S3 / MinIO

\- Docker



\## Development



\- pytest

\- httpx

\- ruff

\- mypy

\- pre-commit



\---



\# 4. Project structure



```text

youtube-media-api/

│

├── app/

│   ├── main.py

│   │

│   ├── api/

│   │   ├── router.py

│   │   └── v1/

│   │       ├── youtube.py

│   │       ├── media.py

│   │       └── jobs.py

│   │

│   ├── core/

│   │   ├── config.py

│   │   ├── logging.py

│   │   └── security.py

│   │

│   ├── schemas/

│   │   ├── youtube.py

│   │   ├── media.py

│   │   └── job.py

│   │

│   ├── services/

│   │   ├── youtube\_service.py

│   │   ├── ytdlp\_service.py

│   │   ├── ffmpeg\_service.py

│   │   └── job\_service.py

│   │

│   ├── workers/

│   │   └── media\_worker.py

│   │

│   └── utils/

│       ├── filename.py

│       └── validation.py

│

├── tests/

│   ├── test\_youtube.py

│   ├── test\_media.py

│   └── test\_health.py

│

├── downloads/

├── temp/

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

```



\---



\# 5. API versioning



Tất cả API sử dụng:



```text

/api/v1

```



Ví dụ:



```text

GET /api/v1/youtube/info

POST /api/v1/youtube/extract

POST /api/v1/media/audio

POST /api/v1/media/video

```



\---



\# 6. Health API



\## GET `/api/v1/health`



Response:



```json

{

&#x20; "status": "ok",

&#x20; "service": "youtube-media-api",

&#x20; "version": "1.0.0"

}

```



\## GET `/api/v1/health/dependencies`



Kiểm tra:



\- yt-dlp

\- FFmpeg

\- filesystem

\- Redis nếu sử dụng

\- storage nếu sử dụng



Response:



```json

{

&#x20; "status": "ok",

&#x20; "dependencies": {

&#x20;   "yt\_dlp": "ok",

&#x20;   "ffmpeg": "ok",

&#x20;   "storage": "ok"

&#x20; }

}

```



\---



\# 7. YouTube APIs



\## 7.1. Get video information



\### GET



```text

/api/v1/youtube/info?url={youtube\_url}

```



Ví dụ:



```text

/api/v1/youtube/info?url=https://www.youtube.com/watch?v=xxxxx

```



Response:



```json

{

&#x20; "id": "xxxxx",

&#x20; "title": "Example Song",

&#x20; "description": "...",

&#x20; "duration": 245,

&#x20; "thumbnail": "https://...",

&#x20; "channel": {

&#x20;   "id": "...",

&#x20;   "name": "..."

&#x20; },

&#x20; "view\_count": 100000,

&#x20; "upload\_date": "20261005",

&#x20; "webpage\_url": "https://www.youtube.com/watch?v=xxxxx"

}

```



Không download media.



\---



\# 8. Extract available formats



\## POST



```text

/api/v1/youtube/formats

```



Request:



```json

{

&#x20; "url": "https://www.youtube.com/watch?v=xxxxx"

}

```



Response:



```json

{

&#x20; "video\_id": "xxxxx",

&#x20; "formats": \[

&#x20;   {

&#x20;     "format\_id": "18",

&#x20;     "ext": "mp4",

&#x20;     "resolution": "360p",

&#x20;     "fps": 30,

&#x20;     "filesize": 12345678,

&#x20;     "has\_video": true,

&#x20;     "has\_audio": true

&#x20;   },

&#x20;   {

&#x20;     "format\_id": "140",

&#x20;     "ext": "m4a",

&#x20;     "abr": 129,

&#x20;     "has\_video": false,

&#x20;     "has\_audio": true

&#x20;   }

&#x20; ]

}

```



Mục đích:



\- FE biết media có những format nào.

\- Không cần download.

\- Không cần expose toàn bộ object của yt-dlp.



\---



\# 9. Extract media URL



\## POST



```text

/api/v1/youtube/extract

```



Request:



```json

{

&#x20; "url": "https://www.youtube.com/watch?v=xxxxx",

&#x20; "type": "audio"

}

```



`type`:



```text

audio

video

best

```



Response:



```json

{

&#x20; "video\_id": "xxxxx",

&#x20; "title": "Example Song",

&#x20; "duration": 245,

&#x20; "media": {

&#x20;   "url": "https://...",

&#x20;   "type": "audio",

&#x20;   "format": "m4a",

&#x20;   "mime\_type": "audio/mp4",

&#x20;   "duration": 245

&#x20; }

}

```



Lưu ý:



URL được trả về có thể là URL stream có thời hạn.



FE không nên lưu URL này lâu dài.



\---



\# 10. Karaoke Audio API



Mục tiêu chính:



```text

YouTube

&#x20;  ↓

yt-dlp

&#x20;  ↓

Audio stream

&#x20;  ↓

Angular

&#x20;  ↓

Karaoke / Web Audio API

```



\## POST



```text

/api/v1/karaoke/audio

```



Request:



```json

{

&#x20; "url": "https://www.youtube.com/watch?v=xxxxx"

}

```



Response:



```json

{

&#x20; "video\_id": "xxxxx",

&#x20; "title": "Karaoke Song",

&#x20; "duration": 245,

&#x20; "audio\_url": "https://..."

}

```



\---



\# 11. Download Audio



\## POST



```text

/api/v1/media/audio

```



Request:



```json

{

&#x20; "url": "https://www.youtube.com/watch?v=xxxxx",

&#x20; "format": "mp3",

&#x20; "quality": "192"

}

```



Supported:



```text

mp3

m4a

wav

opus

```



Backend:



```text

yt-dlp

&#x20;  ↓

download audio

&#x20;  ↓

FFmpeg

&#x20;  ↓

output file

```



Response:



```json

{

&#x20; "job\_id": "job\_123",

&#x20; "status": "queued"

}

```



Không nên giữ HTTP connection trong lúc download lâu.



\---



\# 12. Download Video



\## POST



```text

/api/v1/media/video

```



Request:



```json

{

&#x20; "url": "https://www.youtube.com/watch?v=xxxxx",

&#x20; "quality": "720p",

&#x20; "format": "mp4"

}

```



Response:



```json

{

&#x20; "job\_id": "job\_456",

&#x20; "status": "queued"

}

```



\---



\# 13. Job API



Các thao tác download/convert nên sử dụng asynchronous job.



\## GET



```text

/api/v1/jobs/{job\_id}

```



Response:



```json

{

&#x20; "job\_id": "job\_123",

&#x20; "status": "processing",

&#x20; "progress": 67,

&#x20; "filename": "song.mp3"

}

```



Status:



```text

queued

processing

completed

failed

cancelled

```



\---



\# 14. Download completed file



\## GET



```text

/api/v1/jobs/{job\_id}/download

```



Backend trả file:



```text

Content-Type: audio/mpeg

```



Hoặc:



```text

video/mp4

```



\---



\# 15. Cancel job



\## DELETE



```text

/api/v1/jobs/{job\_id}

```



Response:



```json

{

&#x20; "job\_id": "job\_123",

&#x20; "status": "cancelled"

}

```



\---



\# 16. FFmpeg processing API



Sau khi có media, backend có thể hỗ trợ:



\## Convert audio



```text

POST /api/v1/media/convert/audio

```



Ví dụ:



```json

{

&#x20; "job\_id": "job\_123",

&#x20; "format": "mp3",

&#x20; "bitrate": "192k"

}

```



\## Extract audio from video



```text

POST /api/v1/media/extract-audio

```



\## Normalize audio



```text

POST /api/v1/media/audio/normalize

```



\## Trim audio



```text

POST /api/v1/media/audio/trim

```



Request:



```json

{

&#x20; "job\_id": "job\_123",

&#x20; "start": 10,

&#x20; "end": 60

}

```



\---



\# 17. Search API



Không sử dụng YouTube Data API nếu mục tiêu là tránh API key.



Có thể dùng yt-dlp để hỗ trợ search/extraction tùy extractor.



\## GET



```text

/api/v1/youtube/search?q={keyword}

```



Response:



```json

{

&#x20; "query": "Anh Trai Say Hi karaoke",

&#x20; "items": \[

&#x20;   {

&#x20;     "id": "...",

&#x20;     "title": "...",

&#x20;     "duration": 240,

&#x20;     "thumbnail": "...",

&#x20;     "channel": "...",

&#x20;     "url": "https://www.youtube.com/watch?v=..."

&#x20;   }

&#x20; ]

}

```



\### Lưu ý



Search bằng yt-dlp cần được kiểm thử kỹ theo thời điểm triển khai vì khả năng và hành vi của YouTube/extractor có thể thay đổi.



Nếu search trở thành chức năng trọng yếu, có thể bổ sung một search provider riêng.



\---



\# 18. API dành riêng cho Karaoke



Sau khi core API ổn định, xây layer:



```text

/api/v1/karaoke

```



Các endpoint:



```text

GET  /karaoke/search

GET  /karaoke/song/{id}

POST /karaoke/resolve

GET  /karaoke/audio/{id}

```



Ví dụ:



```text

GET /api/v1/karaoke/search?q=...

```



Backend trả về dữ liệu đã được chuẩn hóa cho FE.



FE không cần biết yt-dlp tồn tại.



\---



\# 19. Service layer



Không gọi `yt-dlp` trực tiếp từ router.



Sai:



```python

@app.get("/youtube/info")

def info(url):

&#x20;   ...

&#x20;   yt\_dlp.YoutubeDL(...)

```



Nên:



```text

Router

&#x20;  ↓

YouTubeService

&#x20;  ↓

YtDlpService

&#x20;  ↓

yt-dlp

```



Ví dụ:



```python

class YoutubeService:



&#x20;   def \_\_init\_\_(self, ytdlp\_service):

&#x20;       self.ytdlp = ytdlp\_service



&#x20;   def get\_info(self, url):

&#x20;       return self.ytdlp.extract\_info(url)

```



\---



\# 20. YtDlpService



Đây là abstraction quan trọng nhất.



```python

class YtDlpService:



&#x20;   def get\_info(self, url):

&#x20;       ...



&#x20;   def get\_formats(self, url):

&#x20;       ...



&#x20;   def extract\_audio(self, url):

&#x20;       ...



&#x20;   def extract\_video(self, url):

&#x20;       ...



&#x20;   def download\_audio(self, url, options):

&#x20;       ...



&#x20;   def download\_video(self, url, options):

&#x20;       ...

```



Không để các router phụ thuộc trực tiếp vào yt-dlp.



Lợi ích:



```text

FastAPI

&#x20;  ↓

YtDlpService

&#x20;  ↓

yt-dlp

```



Sau này có thể thay:



```text

yt-dlp

&#x20;  ↓

another extractor

```



mà không phải sửa toàn bộ API.



\---



\# 21. Error handling



Chuẩn hóa error response.



```json

{

&#x20; "error": {

&#x20;   "code": "YOUTUBE\_VIDEO\_UNAVAILABLE",

&#x20;   "message": "The requested video is unavailable.",

&#x20;   "details": null

&#x20; }

}

```



Các error code:



```text

INVALID\_URL

UNSUPPORTED\_URL

VIDEO\_NOT\_FOUND

VIDEO\_UNAVAILABLE

VIDEO\_PRIVATE

VIDEO\_AGE\_RESTRICTED

EXTRACTION\_FAILED

DOWNLOAD\_FAILED

FFMPEG\_FAILED

STORAGE\_ERROR

JOB\_NOT\_FOUND

JOB\_CANCELLED

TIMEOUT

```



\---



\# 22. Security



Không cho client truyền tùy ý command vào FFmpeg hoặc yt-dlp.



Không làm:



```text

/api/download?command=...

```



Chỉ nhận:



```json

{

&#x20; "url": "...",

&#x20; "format": "mp3"

}

```



Validate:



\- URL

\- format

\- quality

\- filename

\- output path



Không cho phép:



```text

../../etc/passwd

```



hoặc arbitrary filesystem path.



\---



\# 23. Rate limiting



YouTube extraction/download có thể khá nặng.



Thiết lập:



```text

IP

&#x20;↓

Rate limiter

&#x20;↓

FastAPI

```



Ví dụ:



```text

GET /youtube/info

20 requests/minute



POST /media/audio

5 requests/minute

```



Có thể dùng Redis nếu deploy nhiều instance.



\---



\# 24. Caching



Metadata có thể cache.



Ví dụ:



```text

YouTube URL

&#x20;    ↓

SHA256

&#x20;    ↓

Redis

```



Cache:



```text

video metadata

formats

thumbnail

duration

```



Không nên cache stream URL quá lâu vì URL có thể expire.



\---



\# 25. Storage



Giai đoạn đầu:



```text

Local filesystem

```



Sau đó:



```text

FastAPI

&#x20;  ↓

Object Storage

&#x20;  ↓

S3 / MinIO

```



Ví dụ:



```text

bucket/

&#x20;├── audio/

&#x20;├── video/

&#x20;└── temp/

```



Không nên giữ file download vĩnh viễn trên container.



\---



\# 26. Background processing



\### Phase 1



Có thể sử dụng:



```python

BackgroundTasks

```



cho tác vụ đơn giản.



\### Phase 2



Dùng:



```text

FastAPI

&#x20;  ↓

Redis

&#x20;  ↓

Worker

&#x20;  ↓

yt-dlp / FFmpeg

```



Ví dụ:



```text

&#x20;               ┌─────────────┐

&#x20;               │  FastAPI    │

&#x20;               └──────┬──────┘

&#x20;                      │

&#x20;                      ▼

&#x20;                   Redis

&#x20;                      │

&#x20;                      ▼

&#x20;                 Media Worker

&#x20;                 │          │

&#x20;                 ▼          ▼

&#x20;               yt-dlp      FFmpeg

```



Đây là kiến trúc nên hướng tới nếu app có nhiều user.



\---



\# 27. Docker



Docker image cần có:



```text

Python

FastAPI

yt-dlp

FFmpeg

```



Ví dụ:



```dockerfile

FROM python:3.12-slim



WORKDIR /app



RUN apt-get update \\

&#x20;   \&\& apt-get install -y ffmpeg \\

&#x20;   \&\& rm -rf /var/lib/apt/lists/\*



COPY requirements.txt .



RUN pip install --no-cache-dir -r requirements.txt



COPY app ./app



CMD \["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

```



\---



\# 28. Environment variables



`.env.example`



```env

APP\_NAME=youtube-media-api

APP\_ENV=development



PORT=8080



TEMP\_DIR=/tmp/media

DOWNLOAD\_DIR=/app/downloads



REDIS\_URL=redis://redis:6379/0



MAX\_DOWNLOAD\_SIZE\_MB=500

JOB\_TIMEOUT\_SECONDS=600



CORS\_ORIGINS=http://localhost:4200

```



\---



\# 29. CORS



Development:



```text

http://localhost:4200

```



Production:



```text

https://iloveu.studio

```



Không dùng:



```text

allow\_origins=\["\*"]

```



ở production nếu API có chức năng download/process.



\---



\# 30. Logging



Log:



```text

request\_id

job\_id

video\_id

operation

duration

status

error

```



Ví dụ:



```text

INFO job=job\_123 video=abc operation=audio\_download status=processing

INFO job=job\_123 progress=45

INFO job=job\_123 status=completed

```



Không log:



\- Cookie

\- Token

\- Authorization header

\- Sensitive credentials



\---



\# 31. Testing



Test các trường hợp:



\### URL



```text

valid YouTube URL

invalid URL

unsupported URL

```



\### Video



```text

normal video

private video

deleted video

age-restricted video

live video

shorts

playlist

```



\### Download



```text

audio mp3

audio m4a

video mp4

invalid format

```



\### FFmpeg



```text

convert

extract audio

trim

normalize

```



\---



\# 32. Development roadmap



\## Phase 1 — Basic API



\- \[ ] Setup Python

\- \[ ] Setup FastAPI

\- \[ ] Setup Pydantic

\- \[ ] Setup Uvicorn

\- \[ ] Health API

\- \[ ] CORS

\- \[ ] Configuration

\- \[ ] Logging



\---



\## Phase 2 — yt-dlp



\- \[ ] Install yt-dlp

\- \[ ] Implement YtDlpService

\- \[ ] Get video info

\- \[ ] Get formats

\- \[ ] Extract audio URL

\- \[ ] Extract video URL

\- \[ ] Error handling



Endpoints:



```text

GET  /api/v1/youtube/info

POST /api/v1/youtube/formats

POST /api/v1/youtube/extract

```



\---



\## Phase 3 — Download



\- \[ ] Audio download

\- \[ ] Video download

\- \[ ] Temporary storage

\- \[ ] File cleanup

\- \[ ] Download status



Endpoints:



```text

POST   /api/v1/media/audio

POST   /api/v1/media/video

GET    /api/v1/jobs/{id}

GET    /api/v1/jobs/{id}/download

DELETE /api/v1/jobs/{id}

```



\---



\## Phase 4 — FFmpeg



\- \[ ] Install FFmpeg

\- \[ ] Audio conversion

\- \[ ] Video conversion

\- \[ ] Extract audio

\- \[ ] Trim

\- \[ ] Normalize

\- \[ ] Format conversion



\---



\## Phase 5 — Karaoke API



\- \[ ] Karaoke search

\- \[ ] Song metadata

\- \[ ] Resolve media

\- \[ ] Audio endpoint

\- \[ ] Thumbnail

\- \[ ] Duration

\- \[ ] Song information DTO



\---



\## Phase 6 — Async Worker



\- \[ ] Redis

\- \[ ] Job queue

\- \[ ] Worker

\- \[ ] Progress tracking

\- \[ ] Cancellation

\- \[ ] Retry

\- \[ ] Timeout



\---



\## Phase 7 — Storage



\- \[ ] S3/MinIO

\- \[ ] Upload output

\- \[ ] Signed URL

\- \[ ] Automatic cleanup

\- \[ ] TTL



\---



\## Phase 8 — Production



\- \[ ] Docker

\- \[ ] HTTPS

\- \[ ] Rate limiting

\- \[ ] Authentication

\- \[ ] Monitoring

\- \[ ] Error tracking

\- \[ ] Health checks

\- \[ ] Resource limits

\- \[ ] CI/CD



\---



\# 33. API tổng hợp cuối cùng



```text

/api/v1

│

├── /health

│   ├── GET /

│   └── GET /dependencies

│

├── /youtube

│   ├── GET  /info

│   ├── POST /formats

│   ├── POST /extract

│   └── GET  /search

│

├── /karaoke

│   ├── GET  /search

│   ├── GET  /song/{id}

│   └── POST /resolve

│

├── /media

│   ├── POST /audio

│   ├── POST /video

│   ├── POST /convert/audio

│   ├── POST /extract-audio

│   ├── POST /audio/trim

│   └── POST /audio/normalize

│

└── /jobs

&#x20;   ├── GET    /{job\_id}

&#x20;   ├── GET    /{job\_id}/download

&#x20;   └── DELETE /{job\_id}

```



\---



\# 34. Nguyên tắc quan trọng



\### Không biến FastAPI thành một proxy YouTube đơn thuần



Không nên:



```text

Angular

&#x20; ↓

FastAPI

&#x20; ↓

YouTube

&#x20; ↓

stream toàn bộ video

&#x20; ↓

FastAPI

&#x20; ↓

Angular

```



Điều này làm server phải gánh bandwidth rất lớn.



Ưu tiên:



```text

Angular

&#x20;  ↓

FastAPI

&#x20;  ↓

yt-dlp

&#x20;  ↓

resolve media

&#x20;  ↓

Angular nhận URL phù hợp

```



Khi cần download/convert:



```text

Angular

&#x20;  ↓

FastAPI

&#x20;  ↓

Job

&#x20;  ↓

Worker

&#x20;  ↓

yt-dlp + FFmpeg

&#x20;  ↓

Object Storage

&#x20;  ↓

Signed URL

&#x20;  ↓

Angular

```



\---



\# 35. Kiến trúc mục tiêu cho iloveu.studio



```text

&#x20;                        iloveu.studio

&#x20;                             │

&#x20;                        Angular FE

&#x20;                             │

&#x20;               ┌─────────────┴─────────────┐

&#x20;               │                           │

&#x20;               ▼                           ▼

&#x20;         YouTube Player              FastAPI API

&#x20;               │                           │

&#x20;               │                    ┌──────┴──────┐

&#x20;               │                    │             │

&#x20;               │                    ▼             ▼

&#x20;               │                 yt-dlp        Redis

&#x20;               │                    │             │

&#x20;               │                    │             ▼

&#x20;               │                    │          Worker

&#x20;               │                    │             │

&#x20;               │                    │       ┌─────┴─────┐

&#x20;               │                    │       ▼           ▼

&#x20;               │                    │    yt-dlp      FFmpeg

&#x20;               │                    │                    │

&#x20;               │                    │                    ▼

&#x20;               │                    │               S3 / MinIO

&#x20;               │                    │

&#x20;               └────────────────────┴──────────────┐

&#x20;                                                    ▼

&#x20;                                              Angular App

&#x20;                                                    │

&#x20;                                          Web Audio API

&#x20;                                                    │

&#x20;                                 ┌──────────────────┼──────────────────┐

&#x20;                                 ▼                  ▼                  ▼

&#x20;                             Microphone          Echo               Reverb

&#x20;                                 │

&#x20;                                 ▼

&#x20;                             Recorder

&#x20;                                 │

&#x20;                                 ▼

&#x20;                          Vocal recording

```



\---



\# 36. MVP nên làm trước



Không cần làm toàn bộ hệ thống ngay.



MVP đầu tiên chỉ cần:



```text

1\. FastAPI

2\. yt-dlp

3\. FFmpeg

4\. GET /youtube/info

5\. POST /youtube/formats

6\. POST /youtube/extract

7\. POST /media/audio

8\. GET /jobs/{id}

9\. GET /jobs/{id}/download

10\. Docker

```



Sau khi Angular tích hợp ổn định mới thêm:



```text

Redis

Worker

S3/MinIO

Authentication

Rate limiting

Karaoke API

Search

```



Mục tiêu của MVP:



```text

Angular

&#x20;  ↓

FastAPI

&#x20;  ↓

yt-dlp

&#x20;  ↓

YouTube

&#x20;  ↓

FFmpeg

&#x20;  ↓

Audio/Video

&#x20;  ↓

Angular

```



Đây sẽ là nền tảng backend media dùng chung cho toàn bộ `iloveu.studio`, thay vì viết riêng từng API phục vụ một tính năng.



