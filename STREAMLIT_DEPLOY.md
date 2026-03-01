# VibeScan Streamlit App

## 🚀 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud (FREE)

1. **Push to GitHub** (Already done via automation!)

2. **Go to Streamlit Cloud**: https://share.streamlit.io/

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Configure deployment**:
   - Repository: `AbinVarghexe/vibescan`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

6. **Click "Deploy"**

That's it! Your app is live at: `https://vibescen.streamlit.app/`

## ✨ Features

- 🎨 Google-like minimal design
- 📁 Drag & drop file upload
- 📝 Text paste interface
- ⚡ Real-time dependency scanning
- 📊 Beautiful visualizations
- 🔒 Privacy-focused (runs analysis locally)

## 🛠️ Alternative FREE Hosting Options

### 1. Render.com
- Fork repository
- Connect to Render
- Deploy as Web Service
- **URL**: `https://vibescan.onrender.com`

### 2. Railway.app
```bash
railway login
railway init
railway up
```
- **URL**: `https://vibescan.up.railway.app`

### 3. Fly.io
```bash
flyctl launch
flyctl deploy
```
- **URL**: `https://vibescan.fly.dev`

### 4. Hugging Face Spaces
- Create a new Space
- Select "Streamlit" as SDK
- Push code to the space
- **URL**: `https://huggingface.co/spaces/YOUR_USERNAME/vibescan`

## 🌟 Recommended: Streamlit Cloud

**Why?**
- ✅ Completely FREE
- ✅ Automatic deployments from GitHub
- ✅ Built specifically for Streamlit apps
- ✅ SSL certificates included
- ✅ Custom domain support
- ✅ Easy to configure

## 📱 Mobile Responsive

The app is fully responsive and works great on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktops

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- UI behavior

## 🚨 Important Notes

- The app requires internet connection to check npm/PyPI registries
- All scanning happens in real-time
- No data is stored on the server
- Privacy-focused design

## 📚 Documentation

See main [README.md](../README.md) for full documentation.
