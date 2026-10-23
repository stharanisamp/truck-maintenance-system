# 🚀 Truck Maintenance System - Vercel Hosting Guide

இந்த வழிகாட்டி (Guide) மூலம் உங்கள் Truck Maintenance System ப்ராஜெக்ட்டை **Vercel**-ல் 100% பிழையின்றி (zero errors) host செய்யலாம்.

---

## 📌 1. நாம் செய்துள்ள மாற்றங்கள் (Key Adaptations Made)

1. **Vercel Serverless Entry Point (`api/index.py`)**:
   - Vercel Python runtime-க்கு தேவையான WSGI bridge உருவாக்கப்பட்டுள்ளது.
2. **Vercel Routing (`vercel.json`)**:
   - Static files Edge CDN வழியாகவும், application requests `api/index.py` வழியாகவும் route செய்யப்படுகிறது.
3. **250MB Function Limit Optimization (`requirements.txt`)**:
   - Vercel-ன் 250MB Lambda வரம்பை தாண்டும் 1.5GB `torch` மற்றும் `easyocr` தொகுப்புக்கு பதிலாக, வேகமான **Google Gemini Vision API** OCR இணைக்கப்பட்டுள்ளது (இது தமிழ் & ஆங்கில கையெழுத்து மெமோக்களை மிக துல்லியமாக வாசிக்கும்).
   - `opencv-python-headless` மற்றும் PostgreSQL-க்கான `psycopg2-binary` சேர்க்கப்பட்டுள்ளது.
4. **Read-Only Filesystem Handling (`config.py` & `app.py`)**:
   - Vercel serverless-ல் `/tmp/uploads` பயன்படுத்தப்பட்டு, dynamic uploads `/static/uploads/...` URL வழியாக எந்தவித link முறிவும் இன்றி render செய்யப்படுகிறது.
5. **Deployment Exclusion (`.vercelignore`)**:
   - தேவையில்லாத பெரிய cache மற்றும் docs கோப்புகள் Vercel bundle-ல் சேராமல் தடுக்கப்பட்டுள்ளது.

---

## 🛠️ 2. Vercel Dashboard-ல் சேர்க்க வேண்டிய Environment Variables

Vercel-ல் Project Settings -> **Environment Variables** பகுதிக்கு சென்று கீழ்வரும் மாறிகளை சேர்க்கவும் (பார்க்க: [.env.vercel.example](file:///c:/Users/ELCOT/Desktop/truck%20maintenance%20system/.env.vercel.example)):

| Variable Name | Value / விளக்கம் |
| :--- | :--- |
| `SECRET_KEY` | `truck-secret-key-prod-antigravity-2026` |
| `DATABASE_URL` | Supabase அல்லது Neon-ல் பெறப்பட்ட PostgreSQL URL (எ.கா: `postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`) |
| `GEMINI_API_KEY` | Google AI Studio-வில் இலவசமாக பெறப்பட்ட API Key ([aistudio.google.com](https://aistudio.google.com/)) |
| `GEMINI_MODEL` | `gemini-1.5-flash` |
| `MAIL_ID` | `stharanisamp@gmail.com` |
| `PASS` | `hlidlayyqocnsubr` |
| `MAIL_SERVER` | `smtp.gmail.com` |
| `MAIL_PORT` | `587` |
| `MAIL_USE_TLS` | `True` |
| `MAIL_DEFAULT_SENDER`| `stharanisamp@gmail.com` |

> [!TIP]
> **Free Cloud Database:**
> Vercel ஒரு stateless serverless platform என்பதால், உங்கள் லாரி, மெமோ, டிரைவர் விவரங்கள் நிரந்தரமாக சேமிக்கப்பட [Supabase](https://supabase.com/) அல்லது [Neon](https://neon.tech/)-ல் ஒரு இலவச PostgreSQL database தொடங்கி அதன் `DATABASE_URL`-ஐ Vercel-ல் கொடுக்க வேண்டும்.

---

## 📤 3. Deploy செய்யும் 2 எளிய வழிகள்

### வழிமுறை A: GitHub வழியாக (பரிந்துரைக்கப்படுகிறது)

1. உங்கள் ப்ராஜெக்ட் ஃபோல்டரில் Git-ஐ initialize செய்யவும்:
   ```bash
   git init
   git add .
   git commit -m "Vercel serverless setup complete"
   ```
2. GitHub-ல் ஒரு புதிய Repository உருவாக்கி push செய்யவும்:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/truck-maintenance-system.git
   git branch -M main
   git push -u origin main
   ```
3. [vercel.com](https://vercel.com/)-க்கு சென்று **Add New...** -> **Project** கிளிக் செய்து உங்கள் GitHub repo-வை Import செய்யவும்.
4. **Environment Variables**-ல் மேலே உள்ள மதிப்புகளை கொடுத்து **Deploy** கிளிக் செய்யவும்!

---

### வழிமுறை B: Vercel CLI வழியாக

1. Terminal-ல் Vercel CLI-ஐ install செய்யவும்:
   ```bash
   npm install -g vercel
   ```
2. இந்த ஃபோல்டரில் நின்று commands இயக்கவும்:
   ```bash
   vercel
   ```
3. Prompt கேட்கும்போது settings-ஐ confirm செய்து `vercel --prod` கொடுத்து Deploy செய்யவும்.

---

## 🔑 Default Login Credentials (முதல் முறை திறக்கும் போது)
- **Fleet Owner (Admin)**: `stharanisamp@gmail.com` / `admin123`
- **Driver**: `murugan@truck.com` / `driver123`
