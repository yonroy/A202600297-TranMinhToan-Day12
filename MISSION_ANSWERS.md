#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:** Trần Minh Toàn 
> **Student ID:** A202600297  
> **Date:** 17/4/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:


# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets (API Keys & DB Credentials)**: Mã nguồn chứa trực tiếp `OPENAI_API_KEY` và `DATABASE_URL` (admin/password). Điều này cực kỳ nguy hiểm nếu mã nguồn được đẩy lên GitHub hoặc môi trường công khai.
2. **Thiếu Configuration Management**: Các biến cấu hình như `DEBUG`, `MAX_TOKENS` được fix cứng trong code thay vì đọc từ environment variables (`.env`).
3. **Sử dụng Print thay vì Logging**: Sử dụng lệnh `print` để debug thay vì thư viện logging chuyên nghiệp. Nghiêm trọng hơn, code còn in cả các thông tin nhạy cảm (API Key) ra console.
4. **Thiếu Health Check Endpoints**: Không có các endpoint như `/health` hay `/ready` để các nền tảng (như Railway, Docker) có thể theo dõi trạng thái sống/chết của agent.
5. **Fix cứng Host và Port**: 
   - `host="localhost"`: Khiến ứng dụng chỉ có thể truy cập từ máy nội bộ, không thể truy cập được từ bên ngoài hoặc chạy trong Docker container.
   - `port=8000`: Ngăn cản việc ứng dụng tự động nhận diện Port được cấp bởi các nền tảng Cloud (thường qua biến môi trường `PORT`).
6. **Chế độ Debug trong Production**: `reload=True` được bật trực tiếp trong mã nguồn, điều này gây tốn tài nguyên và tiềm ẩn rủi ro bảo mật nếu chạy trên môi trường thực tế.

### Exercise 1.3: Comparison table
| Feature | Basic (Develop) | Advanced (Production) | Tại sao quan trọng? |
|---------|---------|------------|----------------|
| Config  | Hardcode trực tiếp trong code | Sử dụng Environment Variables (`.env`, `Settings`) | Bảo mật secrets, dễ dàng cấu hình linh hoạt cho từng môi trường (Dev/Staging/Prod) mà không cần sửa code. |
| Health check | Không có | Có `/health` (liveness) và `/ready` (readiness) | Giúp các nền tảng (Railway, Docker) tự động giám sát, restart và điều phối traffic khi agent gặp sự cố. |
| Logging | Sử dụng lệnh `print()` | Structured JSON Logging (`logger.info`) | Dễ dàng gom log và phân tích tự động; tránh in trực tiếp các thông tin nhạy cảm (secrets) ra console. |
| Shutdown | Tắt đột ngột (Kill process) | Graceful Shutdown (lifespan, SIGTERM) | Đảm bảo các request đang xử lý được hoàn tất và đóng các kết nối (DB, Redis) an toàn trước khi dừng hẳn. |
| Networking | `localhost`, fix cứng port | `0.0.0.0`, lấy Port từ environment | Bắt buộc để ứng dụng có thể chạy ổn định trong Container và nhận diện Port được cấp bởi Cloud platform. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11` (Bản phân phối Python chuẩn).
2. Working directory: `/app` (Thư mục gốc cho ứng dụng bên trong container).
3. Tại sao COPY requirements.txt trước? Để tận dụng **Docker Layer Caching**. Nếu `requirements.txt` không đổi, Docker sẽ bỏ qua bước cài đặt dependencies (`pip install`), giúp quá trình build nhanh hơn nhiều.
4. CMD vs ENTRYPOINT khác nhau thế nào?
   - `CMD`: Cung cấp lệnh mặc định và có thể bị ghi đè (override) dễ dàng khi chạy container.
   - `ENTRYPOINT`: Thiết lập lệnh chính không thể bị ghi đè dễ dàng; các tham số truyền vào khi chạy container sẽ được cộng dồn vào sau lệnh này.

### Exercise 2.3: Image size comparison
- Develop: ~1010 MB (Sử dụng python:3.11 full version chứa toàn bộ công cụ build và thư viện)
- Production: ~145 MB (Sử dụng python:3.11-slim và cấu trúc Multi-stage chỉ giữ lại những gì cần thiết để chạy)
- Difference: ~85.6% (Kích thước giảm hơn 6 lần)
## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: deploy-test-production-0731.up.railway.app
- Screenshot: [domain.png](domain.png)

## Part 4: API Security

### Exercise 4.1-4.3: Test results
```
$ curl -H "X-API-Key: demo-key-change-in-production" -X POST -H "Content-Type: application/json" -d '{"question":"hello"}' http://localhost:8000/ask?question=hello
{"question":"hello","answer":"Agent đang hoạt động tốt! (mock response) Hỏi thêm câu hỏi đi nhé."}
Minh Toan@LAPTOP-HCPVVRLO MINGW64 /d/AI engineer/Vinuni/Day 12/Lab/A202600297-TranMinhToan-Day12 (main)
$ curl -H -X POST -H "Content-Type: application/json" -d '{"question":"hello"}' http://localhost:8000/ask?question=hello      
Warning: The provided HTTP header '-X' does not look like a header?
curl: (6) Could not resolve host: POST
{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}
```

### Exercise 4.4: Cost guard implementation
Mục tiêu chính của Cost Guard là tránh các hóa đơn "khủng" bất ngờ từ nhà cung cấp LLM API (như OpenAI, Anthropic). Cách tiếp cận của tôi bao gồm các bước sau:

1. Định nghĩa Đơn giá (Price Tracking): Hệ thống thiết lập bảng giá chi tiết cho từng 1.000 tokens đầu vào (Input) và đầu ra (Output) dựa trên thực tế của model đang dùng (ví dụ: GPT-4o-mini).
2. Quản lý Hạn mức đa tầng (Multi-level Quota):
   - User Budget: Mỗi người dùng được cấp một hạn mức hàng ngày (ví dụ: $1.0/ngày). Nếu vượt quá, hệ thống sẽ chặn request và trả về lỗi 402 Payment Required.
   - Global Budget: Đây là chốt chặn cuối cùng cho toàn bộ hệ thống (ví dụ: $10.0/ngày). Điều này giúp bảo vệ ví tiền của chủ sở hữu Agent nếu có một cuộc tấn công từ nhiều tài khoản khác nhau.
3. Cơ chế Cảnh báo (Smart Warning): Khi người dùng đạt tới ngưỡng 80% hạn mức, hệ thống sẽ tự động ghi log cảnh báo (warning) để admin có thể can thiệp hoặc thông báo cho người dùng nạp thêm tiền/gia hạn.
4. Quy trình 2 bước (Check-then-Record):
   - Bước 1 (Check): Kiểm tra budget trước khi gửi request tới LLM. Nếu hết tiền, không gửi request để tiết kiệm chi phí.
   - Bước 2 (Record): Sau khi nhận phản hồi từ LLM, ghi lại số lượng token thực tế đã dùng vào hệ thống lưu trữ (trong bài Lab là In-memory, trong Production sẽ là Redis để đảm bảo tính Stateless).

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
[Your explanations and test results]
#### 1. Hệ thống giám sát (Health & Readiness checks)
- **Triển khai:** Tạo 2 endpoint `/health` (liveness) và `/ready` (readiness).
- **Ý nghĩa:** Endpoint `/health` giúp Docker/Railway biết container còn sống hay đã treo để tự động khởi động lại. Endpoint `/ready` đảm bảo Agent chỉ nhận traffic khi đã kết nối xong với Redis và Database, tránh lỗi cho người dùng khi app đang khởi động.
#### 2. Tắt ứng dụng an toàn (Graceful Shutdown)
- **Triển khai:** Sử dụng thư viện `signal` để bắt tín hiệu `SIGTERM`.
- **Ý nghĩa:** Khi có lệnh tắt (do update hoặc scale down), Agent sẽ không dừng ngay lập tức mà đợi vài giây để xử lý xong các request đang dang dở và đóng các kết nối Redis/DB an toàn. Điều này giúp hệ thống đạt độ ổn định 99.99%.
#### 3. Thiết kế phi trạng thái (Stateless Design)
- **Triển khai:** Chuyển toàn bộ dữ liệu lịch sử hội thoại (Conversation History) từ RAM của Agent sang lưu trữ tập trung tại **Redis**.
- **Ý nghĩa:** Đây là điều kiện tiên quyết để mở rộng hệ thống (scaling). Dù người dùng bị điều hướng đến bất kỳ Agent instance nào (Agent 1, 2 hay 3), Agent đó đều có thể lấy được lịch sử hội thoại từ Redis để trả lời đúng ngữ cảnh.
#### 4. Cân bằng tải và Khả năng chịu lỗi (Load Balancing & High Availability)
- **Triển khai:** Sử dụng **Nginx** làm Reverse Proxy để điều phối traffic và cấu hình `scale agent=3` trong Docker Compose.
- **Ý nghĩa:** Khi một bản sao Agent bị lỗi hoặc tắt đi, Nginx sẽ tự động phát hiện và chuyển hướng người dùng sang các Agent còn lại, đảm bảo dịch vụ không bao giờ bị gián đoạn (No Downtime).
```

---

### 2. Full Source Code - Lab 06 Complete (60 points)

Your final production-ready agent with all files:

```
your-repo/
├── app/
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── auth.py              # Authentication
│   ├── rate_limiter.py      # Rate limiting
│   └── cost_guard.py        # Cost protection
├── utils/
│   └── mock_llm.py          # Mock LLM (provided)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Full stack
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── .dockerignore            # Docker ignore
├── railway.toml             # Railway config (or render.yaml)
└── README.md                # Setup instructions
```

**Requirements:**
-  All code runs without errors
-  Multi-stage Dockerfile (image < 500 MB)
-  API key authentication
-  Rate limiting (10 req/min)
-  Cost guard ($10/month)
-  Health + readiness checks
-  Graceful shutdown
-  Stateless design (Redis)
-  No hardcoded secrets

---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://your-agent.railway.app

## Platform
Railway / Render / Cloud Run

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
```

##  Pre-Submission Checklist

- [ ] Repository is public (or instructor has access)
- [ ] `MISSION_ANSWERS.md` completed with all exercises
- [ ] `DEPLOYMENT.md` has working public URL
- [ ] All source code in `app/` directory
- [ ] `README.md` has clear setup instructions
- [ ] No `.env` file committed (only `.env.example`)
- [ ] No hardcoded secrets in code
- [ ] Public URL is accessible and working
- [ ] Screenshots included in `screenshots/` folder
- [ ] Repository has clear commit history

---

##  Self-Test

Before submitting, verify your deployment:

```bash
# 1. Health check
curl https://your-app.railway.app/health

# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/your-username/day12-agent-deployment
```

**Deadline:** 17/4/2026

---

##  Quick Tips

1.  Test your public URL from a different device
2.  Make sure repository is public or instructor has access
3.  Include screenshots of working deployment
4.  Write clear commit messages
5.  Test all commands in DEPLOYMENT.md work
6.  No secrets in code or commit history

---

##  Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CODE_LAB.md](CODE_LAB.md)
- Ask in office hours
- Post in discussion forum

---

**Good luck! **
