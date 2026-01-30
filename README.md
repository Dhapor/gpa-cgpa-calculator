# 🎓 CGPA Calculator with User Authentication

An enhanced GPA/CGPA calculator for university students with user accounts, data persistence, and historical record tracking.

## ✨ New Features Added

### 🔐 User Authentication
- **Sign Up**: Create your personal account
- **Login**: Secure access to your data
- **Password Hashing**: SHA-256 encryption for security

### 💾 Data Storage
- **SQLite Database**: Local database for storing all your records
- **Automatic Saving**: Every semester is saved to your account
- **Complete History**: Access all your past semesters anytime

### 📊 Enhanced Features
- **Add New Semester**: Record courses with grades and units
- **View My Records**: See all your academic history organized by year
- **Auto-filled CGPA**: Your current CGPA auto-populates in "What Do I Need" feature
- **Export Records**: Download complete academic transcripts
- **Real-time CGPA**: Overall CGPA calculated from all semesters

## 🚀 How to Run Locally

1. **Install Streamlit** (if you haven't already):
   ```bash
   pip install streamlit
   ```

2. **Run the app**:
   ```bash
   streamlit run cgpa_calculator_with_auth.py
   ```

3. **The database will be created automatically** when you first run the app!

## 📦 Deploying to Streamlit Cloud

### Step 1: Prepare Your GitHub Repository

1. Create a new repository on GitHub
2. Upload these files:
   - `cgpa_calculator_with_auth.py` (your main app)
   - `requirements.txt`
   - Your images (optional): `SS.jpg`, `RR.jpg`, `smiling-woman-with-afro-posing-pink-sweater.jpg`

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Select the branch (usually `main`)
5. Set main file path: `cgpa_calculator_with_auth.py`
6. Click "Deploy"!

### Important Notes:
- The database file (`cgpa_calculator.db`) will be created automatically
- **Database persistence**: The database resets when the app restarts on Streamlit Cloud's free tier
- For permanent storage, consider upgrading to cloud database (see below)

## 🔒 Security Features

✅ Password hashing (SHA-256)
✅ Unique usernames and emails
✅ Session-based authentication
✅ No plain-text password storage

## 📖 How to Use

### First Time Users:
1. Click "Sign Up" tab
2. Create your account with username, email, and password
3. Login with your credentials

### Adding Semesters:
1. Go to "Add New Semester"
2. Enter academic year (e.g., 2023/2024)
3. Select semester (First/Second/Summer)
4. Add all your courses with grades and units
5. Click "Save Semester" - done! ✅

### Viewing Records:
1. Go to "View My Records"
2. See all semesters organized by year
3. Expand any semester to see course details
4. Export complete records as .txt file

### Planning Ahead:
1. Go to "What Do I Need To Get?"
2. Your current CGPA auto-fills (or enter manually)
3. Enter units for next 2 semesters
4. Set target CGPA
5. Get 3 different strategies to achieve your goal!

## 🗄️ Database Structure

The app uses SQLite with 3 tables:

1. **users**: Stores user accounts
2. **semesters**: Stores semester-level data (GPA, units, year)
3. **courses**: Stores individual course details

## 🔄 Upgrading to Cloud Database (Optional)

If you want permanent data storage that doesn't reset, you can upgrade to:

### Option 1: Supabase (Recommended - Easiest)
- Free tier available
- PostgreSQL database
- Built-in authentication
- [Tutorial here](https://docs.streamlit.io/knowledge-base/tutorials/databases/supabase)

### Option 2: Firebase
- Google's cloud database
- Free tier available
- [Tutorial here](https://blog.streamlit.io/streamlit-firestore/)

### Option 3: MongoDB Atlas
- NoSQL database
- Free tier available

**I can help you migrate to any of these if needed!**

## 🐛 Troubleshooting

### Images not showing?
- Make sure image files are in the same directory as the app
- Or remove the image loading code (lines with `st.image()`)
- The app will work fine without images

### Database resets on Streamlit Cloud?
- This is normal for the free tier
- Upgrade to a cloud database for persistence
- Or use Streamlit Cloud's paid tier with persistent storage

### Can't login after creating account?
- Make sure you're using the exact username and password
- Passwords are case-sensitive

## 💡 Tips

- Add semesters as you complete them to track progress
- Use "What Do I Need" feature to plan your grades
- Download semester reports for your records
- Keep your password safe - there's no recovery feature yet!

## 👨‍💻 Built By

**Datapsalm & Victoria**

📧 Contact: datapsalm@gmail.com

---

## 📝 License

Free to use for educational purposes. If you improve it, give credit! 😊

---

**Need help?** Feel free to reach out via email!
