# Vistone 🎨✨

**Vistone** is an intelligent web application built with Python and Flask that analyzes portrait images to accurately classify human skin tones according to the **Monk Skin Tone (MST) Scale**. Beyond just skin tone detection, Vistone acts as a personal stylist by providing tailored color recommendations (what to wear and what to avoid) based on color psychology and your unique complexion undertones.

---

## 🚀 Features

- **Advanced Face Detection**: Uses MediaPipe's precise Face Mesh to detect facial landmarks and isolate the most accurate skin samples (cheeks, forehead, nose) while automatically ignoring eyes, mouth, and background.
- **Accurate Tone Classification**: Employs K-Means clustering and LAB color space conversions to dynamically match your skin tone to one of the 10 Monk Skin Tone Scale values.
- **Undertone Analysis**: Analyzes the warmth or coolness of your skin to classify your undertone (Warm, Cool, or Neutral).
- **Personalized Color Palette**: Recommends the best clothing/makeup colors to enhance your natural tone and warns against shades that might clash or wash you out.
- **Color Psychology**: Explains *why* certain colors work for you, breaking down the psychological impact and aesthetic harmony of your recommended colors.

---

## 🛠️ Tech Stack

- **Backend Framework:** [Flask](https://flask.palletsprojects.com/)
- **Computer Vision & ML:** [OpenCV](https://opencv.org/), [MediaPipe](https://mediapipe.dev/)
- **Color Mathematics:** [Colormath](https://python-colormath.readthedocs.io/)
- **Data Processing:** [NumPy](https://numpy.org/)
- **Deployment:** Ready for deployment on [Render](https://render.com/) via Gunicorn.

---

## 💻 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/Vistone.git
   cd Vistone
   ```

2. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   *The app will be available at `http://localhost:5000`*

---

## ☁️ Deployment (Render)

This app is pre-configured to be deployed seamlessly on **Render.com**. 
A `.python-version` file is included to strictly enforce Python 3.10.x, ensuring full compatibility with the heavy machine learning dependencies (like MediaPipe). 
The `requirements.txt` file also includes `gunicorn` and the headless version of OpenCV for headless server compatibility.

**Render Setup:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).