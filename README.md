
# Techroom - Discussion Web App

**Techroom** is a full-stack, discussion-based web application built using the Django framework. It allows users to register, log in, create or join study rooms based on various topics, and engage in real-time, message-based discussions. The platform aims to foster knowledge sharing and collaboration among learners.

---

## 🔑 Features

- 🔐 User Authentication (Register / Login / Logout)  
- 🧑‍💻 Custom User Profiles with Avatar Upload  
- 🗂️ Topic-based Study Room Creation and Participation  
- 💬 Real-time Discussion Threads  
- 🔍 Dynamic Filtering and Search (by Room or Topic)  
- 📱 Responsive and Mobile-Friendly UI  
- ⚙️ Django Admin Interface for Superuser Management  

---

## 🛠️ Technologies Used

| Layer       | Stack                      |
|-------------|----------------------------|
| **Backend** | Python, Django             |
| **Frontend**| HTML, CSS, JavaScript      |
| **Database**| PostgreSQL (via pgAdmin)   |
| **Version Control** | Git, GitHub       |

---

## 📁 Project Structure (Key Files)

- `main.html` – Base template (layout and navbar)  
- `login_register.html` – Login & Registration form  
- `room.html` – Discussion room details and chat messages  
- `create-room.html` – Room creation and update form  
- `profile.html` – User profile and activity  
- `models.py` – Custom user model and other DB models  
- `urls.py` – App URL routing  
- `admin.py` – Admin panel setup  

---

## 🚀 Getting Started

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/techroom.git
   cd techroom
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL Database**
   - Create a new database in pgAdmin.
   - Update `DATABASES` settings in `settings.py`.

5. **Run Migrations & Create Superuser**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the App**
   Open `http://127.0.0.1:8000/` in your browser.

---

##  Acknowledgment

This project was developed as part of my learning journey in **Python Full Stack Development**. It demonstrates my skills in Django, database management, RESTful routing, and responsive UI design.
