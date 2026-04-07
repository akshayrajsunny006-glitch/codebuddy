# ⚡ CodeBuddy — Campus Project Hub

> Premium Django platform for campus collaboration. Find projects, join teams, chat, and manage your campus network.

---

## 🚀 Quick Start

### Linux / Mac
```bash
bash setup.sh
```

### Windows
```bat
setup.bat
```

### Manual
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations auth_app projects social admin_app support
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open → **http://127.0.0.1:8000**

---

## 🔑 Login Credentials

### Admins (both have full admin access)
| Name               | Email                              | Password   |
|--------------------|------------------------------------|------------|
| Mahadev Sai Chandra| mahadevsaichandra777@gmail.com     | admin@123  |
| Akshay Raj Sunny   | akshayrajsunny006@gmail.com        | Akshay@006 |

### Student Accounts (8 pre-loaded users)
| Name           | Email                        | Password   | College            |
|----------------|------------------------------|------------|--------------------|
| Arjun Sharma   | arjun@iitd.ac.in            | arjun123   | IIT Delhi          |
| Priya Mehta    | priya@bits.ac.in            | priya123   | BITS Pilani        |
| Rohan Verma    | rohan@nit.ac.in             | rohan123   | NIT Trichy         |
| Sneha Iyer     | sneha@vit.ac.in             | sneha123   | VIT Vellore        |
| Karan Patel    | karan@iiit.ac.in            | karan123   | IIIT Hyderabad     |
| Ananya Bose    | ananya@jadavpur.ac.in       | ananya123  | Jadavpur University|
| Dev Nair       | dev@manipal.ac.in           | dev123     | Manipal Institute  |
| Riya Kapoor    | riya@srm.ac.in              | riya123    | SRM University     |

---

## 📊 Pre-Loaded Sample Data

- **5 live projects** with full descriptions, tasks, and team members
- **20+ project tasks** spread across To Do / In Progress / Done
- **15+ chat messages** in project rooms
- **6 pending join requests** waiting for approval
- **7 friendships** already formed between users
- **3 pending friend requests** with notifications
- **3 support tickets** open for admin review
- **Notifications** seeded for all major events

### Projects included:
| Project | Owner | Status |
|---------|-------|--------|
| CampusEats — Food Delivery for Hostels | Arjun Sharma | 🟢 Recruiting |
| MindMap AI — Smart Study Assistant | Rohan Verma | 🟢 Recruiting |
| CampusDAO — Decentralized Student Council | Karan Patel | 🔵 In Progress |
| LostFound Campus App | Sneha Iyer | 🟢 Recruiting |
| OpenNotes — Collaborative Study Materials | Priya Mehta | 🟢 Recruiting |

---

## 📁 Structure

```
codebuddy/
├── manage.py
├── requirements.txt
├── setup.sh / setup.bat
├── codebuddy/          # Settings, URLs, context processors
├── apps/
│   ├── auth_app/       # Users, profiles, notifications
│   ├── projects/       # Projects, tasks, chat, join requests
│   ├── social/         # Friends, blocks, reports
│   ├── admin_app/      # Admin panel
│   └── support/        # Support tickets
├── templates/          # 15 premium HTML templates
└── static/
    ├── css/main.css    # 700+ line premium dark UI
    └── js/main.js      # Dropdowns, modals, chat, avatars
```

---

## 🎨 UI Highlights
- Dark glassmorphism, electric indigo/violet palette
- Fonts: **Syne** (display) + **DM Sans** (body)
- 3D hover cards, gradient badges, kanban task board
- Chat bubbles, avatar initials, skill tags, responsive layout
