# Face Unlock Web App

A real-time face authentication system using your browser camera, FastAPI backend, and InsightFace for facial recognition.

---

## 📌 Features

* Live webcam preview in browser
* Capture and send face image to backend for verification
* Face embedding comparison using InsightFace
* Unlocks access if the face matches a known image
* Clean frontend with Tailwind CSS and theme toggle
* FastAPI-powered backend with color-coded terminal logs

---

## 💻 Tech Stack

* **Frontend**: HTML, JavaScript, Tailwind CSS
* **Backend**: Python, FastAPI, OpenCV, InsightFace

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/face_unlock_app.git
cd face_unlock_app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ Use **Python 3.10** or compatible (InsightFace may not support latest versions like 3.13+)

### 4. Add Your Face

Place a clear image of your face in the `known_faces/` directory.
Update `main.py` to reference the correct image:

```python
known_img = cv2.imread("known_faces/your_image.jpg")
```

Make sure only one face is visible in the image.

### 5. Run the App

```bash
python main.py
```

Then visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🧪 How It Works

* The app accesses your webcam to display a live feed.
* Clicking **Unlock** captures a frame and sends it to the backend.
* The backend detects a face and compares it to the known one.
* If similarity exceeds the threshold, access is granted.

---

## 📚 Citations & References

* InsightFace: [https://github.com/deepinsight/insightface](https://github.com/deepinsight/insightface)
* FastAPI: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
* OpenCV: [https://opencv.org](https://opencv.org)
* Tailwind CSS: [https://tailwindcss.com](https://tailwindcss.com)
* Base notebook adapted from Personate AI task: [Google Colab](https://colab.research.google.com/drive/1b7ifOAlPJnX5ImJM1qVtQXd5T4Dp0_Zf)

---
