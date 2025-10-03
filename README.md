# AI Poet – Poem & Image Generator

A **Streamlit app** that generates a **poem and an image** based on a user-provided topic using the **OpenAI API**.
It combines **text generation** (GPT-3) and **image generation** (DALL·E) to create unique poetic experiences.

---

## 🚀 Features

* **AI-Powered Poetry** – Generate creative poems based on any topic.
* **AI Image Generation** – Produces an image that visually represents the input.
* **Regeneration Options** – Refresh poem or image independently.
* **Interactive UI** – Clean interface with animations and styled output.

---

## 🛠️ Tech Stack

* **Frontend/UI:** [Streamlit](https://streamlit.io/)
* **AI Backend:** [OpenAI API](https://platform.openai.com/) (Text-Davinci-003 & DALL·E)
* **Language:** Python

---

## 📂 Project Structure

```
Poem-Image-Generator/
├── poem_app.py          # Main Streamlit app
├── requirements.txt     # Python dependencies
```

---

## ⚙️ Installation & Setup

1. **Clone repository**

   ```bash
   git clone <repo-url>
   cd Poem-Image-Generator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API key**

   * Create a `.streamlit/secrets.toml` file:

     ```toml
     api_secret = "your-openai-api-key"
     ```

4. **Run Streamlit app**

   ```bash
   streamlit run poem_app.py
   ```

   The app will be available at:

   ```
   http://localhost:8501
   ```

---

## 🎨 Usage

* Enter a **topic/keyword** (e.g., *sunset, love, adventure*).
* The app generates a **poem and a matching image**.
* Use **Regenerate Image** or **Regenerate Poem** to refresh results.

---

## 👨‍💻 Author

* **Built by [Dave Fagarita](https://github.com/Deyb12)**

---

## 📜 License

This project is for **educational purposes only**.
You may modify and use it for learning or experiments.
