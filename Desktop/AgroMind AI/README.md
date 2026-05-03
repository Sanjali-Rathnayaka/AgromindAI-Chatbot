# 🌾 AgroMind AI — Smart Farming Chatbot

> An intelligent agricultural advisor chatbot built for Sri Lanka farmers, powered by a machine learning crop recommendation model and the Groq LLM API.

---

## ✨ Features

- 🤖 **AI-Powered Advice** — Conversational crop guidance via LLaMA 3.3 70B (Groq)
- 🌱 **Crop Recommendations** — Based on N, P, K, temperature, humidity, pH, and rainfall
- 🗺️ **Sri Lanka–Specific** — Covers wet, dry, intermediate, and hill country farming zones
- 💬 **Quick Suggestions** — One-tap pills for common farming questions
- 🌙 **Dark Agro Theme** — Elegant green-and-gold UI
- 🔒 **Secure Backend** — API key stays server-side; never exposed to the browser

---

## 🖼️ Preview

![AgroMind AI Screenshot](docs/screenshot.png)

---

## 🗂️ Project Structure

```
agromind-ai/
├── app.py               # Flask backend (API proxy + static serving)
├── static/
│   └── index.html       # Chatbot frontend (single-page app)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/agromind-ai.git
cd agromind-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your environment

```bash
cp .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=gsk_your_actual_key_here
PORT=5000
FLASK_DEBUG=false
```

> 🔑 Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Place the frontend

Move (or copy) the chatbot HTML file into the `static/` folder:

```bash
mkdir -p static
cp agromind_chatbot.html static/index.html
```

### 6. Run the server

```bash
python app.py
```

Open your browser at **http://localhost:5000** 🎉

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the chatbot frontend |
| `POST` | `/api/chat` | Send a message and receive an AI reply |
| `GET` | `/api/crops` | Returns the list of supported crops |
| `GET` | `/api/health` | Health check — returns `{"status": "ok"}` |

### `POST /api/chat`

**Request body:**
```json
{
  "messages": [
    { "role": "user", "content": "What crops suit sandy loam soil?" },
    { "role": "assistant", "content": "For sandy loam soil..." },
    { "role": "user", "content": "What about the rainfall requirement?" }
  ]
}
```

**Response:**
```json
{
  "reply": "Rice typically needs 150–200 mm of rainfall per growing season..."
}
```

---

## 🌾 Supported Crops

Rice · Maize · Chickpea · Kidney Beans · Pigeon Peas · Moth Beans · Mung Bean · Black Gram · Lentil · Pomegranate · Banana · Mango · Grapes · Watermelon · Muskmelon · Apple · Orange · Papaya · Coconut · Cotton · Jute · Coffee

---

## 📦 Dependencies

```
flask
flask-cors
requests
python-dotenv
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🌍 Deployment

### Deploy to Render (free tier)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set **Build Command:** `pip install -r requirements.txt`
5. Set **Start Command:** `python app.py`
6. Add environment variable: `GROQ_API_KEY` = your key
7. Click **Deploy** ✅

### Deploy to Railway

```bash
railway login
railway init
railway up
railway variables set GROQ_API_KEY=gsk_your_key
```

### Deploy with Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t agromind-ai .
docker run -p 5000:5000 --env-file .env agromind-ai
```

---

## 🔐 Security Notes

- **Never commit your `.env` file** — it's listed in `.gitignore`
- The original HTML file had the Groq API key hard-coded in JavaScript (visible to anyone). This backend moves the key server-side so it's never exposed to the browser.
- For production, consider rate-limiting the `/api/chat` endpoint.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — ultra-fast LLM inference
- [LLaMA 3.3 70B](https://ai.meta.com/llama/) by Meta
- Sri Lanka Department of Agriculture — crop data inspiration
- Built with ❤️ for Sri Lanka's farming community
