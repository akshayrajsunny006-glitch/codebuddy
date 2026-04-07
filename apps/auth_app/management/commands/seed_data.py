"""
CodeBuddy — Rich Demo Data Seed
Creates real-looking users, projects, tasks, messages, friends, notifications.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.auth_app.models import User, UserProfile, Notification
from apps.projects.models import Project, ProjectMember, JoinRequest, Message, ProjectTask
from apps.social.models import FriendRequest, Friendship
from apps.support.models import SupportTicket
import datetime


USERS = [
    # (full_name, email, password, college, year, skills, bio, available)
    ("Arjun Sharma",    "arjun@iitd.ac.in",      "arjun123",   "IIT Delhi",         "3rd", "Python, Django, PostgreSQL, REST APIs",             "Backend dev obsessed with clean architecture. Love competitive programming.", True),
    ("Priya Mehta",     "priya@bits.ac.in",       "priya123",   "BITS Pilani",       "2nd", "React, TypeScript, Tailwind CSS, Figma",            "Frontend + UI/UX. I turn wireframes into pixel-perfect products.", True),
    ("Rohan Verma",     "rohan@nit.ac.in",        "rohan123",   "NIT Trichy",        "4th", "Machine Learning, PyTorch, Computer Vision, Python","Final year ML researcher. Published 2 papers on CV.", False),
    ("Sneha Iyer",      "sneha@vit.ac.in",        "sneha123",   "VIT Vellore",       "3rd", "Flutter, Dart, Firebase, Mobile Dev",               "Mobile-first developer. Built 4 apps on Play Store.", True),
    ("Karan Patel",     "karan@iiit.ac.in",       "karan123",   "IIIT Hyderabad",    "2nd", "Blockchain, Solidity, Web3, Node.js",               "Crypto native. Building the decentralized future one smart contract at a time.", True),
    ("Ananya Bose",     "ananya@jadavpur.ac.in",  "ananya123",  "Jadavpur University","4th","NLP, Transformers, HuggingFace, Python",             "NLP researcher. Working on Bengali language models.", False),
    ("Dev Nair",        "dev@manipal.ac.in",      "dev123",     "Manipal Institute", "1st", "C++, DSA, Competitive Programming",                 "First year, already cleared ICPC regionals. Code is life.", True),
    ("Riya Kapoor",     "riya@srm.ac.in",         "riya123",    "SRM University",    "3rd", "DevOps, Docker, Kubernetes, AWS, CI/CD",            "Cloud & infra nerd. Love automating everything.", True),
]

PROJECTS = [
    {
        "owner_idx": 0,  # Arjun
        "title": "CampusEats — Food Delivery for Hostels",
        "teaser": "Swiggy, but only for campus canteens",
        "description": "A hyper-local food delivery platform connecting hostel students to campus canteens and tiffin services. Real-time order tracking, group orders, and canteen dashboards.",
        "full_description": "Tech stack: Django REST + React + WebSockets for live tracking. We need a solid mobile-responsive frontend dev and someone who can handle the canteen-side dashboard. Phase 1: MVP in 6 weeks. Phase 2: Payment integration via Razorpay.",
        "skills": "React, Django, WebSockets, PostgreSQL",
        "max_size": 5,
        "difficulty": "intermediate",
        "status": "recruiting",
        "members": [1, 7],  # Priya, Riya
        "tasks": [
            ("Design order flow UI", "Figma prototype + React implementation", "in_progress", 1),
            ("Build canteen dashboard", "Admin panel for canteen owners", "todo", None),
            ("WebSocket order tracking", "Real-time status updates", "todo", 0),
            ("Setup Docker + CI/CD", "Containerize app for deployment", "done", 7),
        ],
        "messages": [
            (0, "Hey team! Let's ship the MVP before semester ends 🚀"),
            (1, "I've pushed the Figma designs to the shared folder, check them out"),
            (7, "Docker setup is done, CI pipeline is running green ✅"),
            (0, "Amazing! Priya can you start on the order flow component this week?"),
            (1, "On it! Should be done by Thursday"),
        ],
        "requests": [(3, "I've built a similar delivery app for my college fest. Would love to contribute the mobile UI!")],
    },
    {
        "owner_idx": 2,  # Rohan
        "title": "MindMap AI — Smart Study Assistant",
        "teaser": "GPT-4 tutor that actually understands your syllabus",
        "description": "An AI study assistant that ingests your course PDFs and generates personalized quizzes, explains concepts, creates mind maps, and tracks your weak areas over time.",
        "full_description": "Using LangChain + GPT-4 + Chroma vector DB. The core RAG pipeline is built. Now need: a clean React chat UI, backend APIs for session management, and a data viz layer for progress tracking. This is a final-year project but I want to open-source it.",
        "skills": "React, Python, LangChain, OpenAI API, FastAPI",
        "max_size": 4,
        "difficulty": "advanced",
        "status": "recruiting",
        "members": [5],  # Ananya
        "tasks": [
            ("RAG pipeline integration", "Connect LangChain to PDF corpus", "done", 2),
            ("Chat UI with message history", "React component with markdown rendering", "in_progress", None),
            ("Progress dashboard", "Charts showing weak topics over time", "todo", None),
            ("Deploy to Vercel + Railway", "Frontend + backend hosting", "todo", None),
        ],
        "messages": [
            (2, "Core ML pipeline is ready. Accuracy on test set is 87% 🎯"),
            (5, "Great! I can help fine-tune the NLP parts. Have experience with similar models."),
            (2, "That would be amazing. Check the /models folder for current architecture."),
        ],
        "requests": [(1, "Love this idea! I can build the React chat interface — done similar for a chatbot project last semester.")],
    },
    {
        "owner_idx": 4,  # Karan
        "title": "CampusDAO — Decentralized Student Council",
        "teaser": "Vote on college decisions with NFT-based governance",
        "description": "Replace the opaque student council with a transparent DAO. Students vote on budget allocation, event approvals, and rule changes using token-weighted governance on Polygon.",
        "full_description": "Smart contracts are 70% done on Polygon testnet. Need frontend devs for the voting UI and a backend for off-chain data indexing. This could become a standard for every college in India.",
        "skills": "Solidity, React, Web3.js, The Graph, Node.js",
        "max_size": 6,
        "difficulty": "advanced",
        "status": "in_progress",
        "members": [6, 0],  # Dev, Arjun
        "tasks": [
            ("Governance smart contract", "ERC20 voting token + proposal system", "done", 4),
            ("Frontend voting dashboard", "React + wagmi wallet connection", "in_progress", None),
            ("The Graph indexer", "Index on-chain events for fast queries", "todo", 0),
            ("Whitepaper & pitch deck", "For college administration approval", "in_progress", 4),
        ],
        "messages": [
            (4, "Contracts are deployed on Polygon testnet! 🎉 Address: 0x1a2b..."),
            (0, "Impressive! I'll start on The Graph subgraph this weekend"),
            (6, "I can help with the frontend, familiar with wagmi"),
            (4, "Perfect team. Let's ship this before elections next month!"),
        ],
        "requests": [],
    },
    {
        "owner_idx": 3,  # Sneha
        "title": "LostFound Campus App",
        "teaser": "Never lose your ID card again",
        "description": "A Flutter app for reporting and finding lost items on campus. AI-powered image matching helps connect lost items to their owners automatically.",
        "full_description": "The Flutter app is 60% done. Need help with the ML image similarity backend (TensorFlow/ONNX) and cloud storage setup. Also need someone to handle push notifications.",
        "skills": "Flutter, Python, TensorFlow, Firebase, FastAPI",
        "max_size": 4,
        "difficulty": "intermediate",
        "status": "recruiting",
        "members": [2],  # Rohan
        "tasks": [
            ("Flutter UI — report lost item", "Form + camera + location picker", "done", 3),
            ("Image similarity ML model", "TF model to match item photos", "in_progress", 2),
            ("Firebase push notifications", "Alert when potential match found", "todo", None),
            ("Admin moderation panel", "Web dashboard to verify matches", "todo", None),
        ],
        "messages": [
            (3, "UI for reporting is done! Working on the matching algorithm now."),
            (2, "I'll integrate the CV model this week. Have a pretrained ResNet we can fine-tune."),
            (3, "Perfect! Let me know if you need the image schema."),
        ],
        "requests": [(7, "I can set up the Firebase + cloud infra for this. Also can help with the CI/CD pipeline.")],
    },
    {
        "owner_idx": 1,  # Priya
        "title": "OpenNotes — Collaborative Study Materials",
        "teaser": "Wikipedia for your college syllabus",
        "description": "A platform where students collaboratively write, edit, and rate study notes for every subject. Think Wikipedia meets Notion, built for Indian engineering syllabi.",
        "full_description": "Stack: Next.js frontend, Django backend, PostgreSQL. Need 2 more devs and someone who can set up the rich text editor (Tiptap/ProseMirror). Great beginner-friendly project with good documentation.",
        "skills": "React, Next.js, Django, PostgreSQL, Tiptap",
        "max_size": 5,
        "difficulty": "beginner",
        "status": "recruiting",
        "members": [6],  # Dev
        "tasks": [
            ("Rich text editor integration", "Tiptap setup with custom extensions", "in_progress", 1),
            ("Note rating system", "Upvote/downvote + quality score", "todo", None),
            ("Subject taxonomy", "Tree of subjects, chapters, topics", "done", 6),
            ("Search & filter", "Full-text search across all notes", "todo", None),
        ],
        "messages": [
            (1, "Welcome Dev! Your DSA knowledge will be super useful for search optimizations"),
            (6, "Happy to be here! Already set up the subject tree structure 🌳"),
            (1, "That was fast! Let's sync tomorrow on the editor component."),
        ],
        "requests": [(0, "Great beginner-friendly project. I can handle the Django REST APIs."),
                     (5, "Would love to contribute. I can work on the NLP-based auto-tagging feature.")],
    },
]

TICKETS = [
    (0, "Can't upload profile picture", "bug", "When I try to upload a photo larger than 2MB the page just refreshes with no error message."),
    (1, "Add dark mode toggle", "feature", "The dark theme is great but it would be nice to have a toggle in the navbar for users who prefer light mode."),
    (3, "Project deletion without warning", "bug", "I accidentally clicked delete on my project and it was gone immediately. Please add a confirmation dialog."),
]


class Command(BaseCommand):
    help = 'Seed rich demo data with real users, projects, tasks, messages, and social connections'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🌱 Seeding CodeBuddy with rich demo data...\n'))

        # ── ADMINS ─────────────────────────────────────────────────────
        ADMINS = [
            ('mahadevsaichandra777@gmail.com', 'admin@123',  'Mahadev Sai Chandra'),
            ('akshayrajsunny006@gmail.com',    'Akshay@006', 'Akshay Raj Sunny'),
        ]
        for admin_email, admin_pass, admin_name in ADMINS:
            admin, created = User.objects.get_or_create(
                email=admin_email,
                defaults=dict(
                    full_name=admin_name,
                    role='admin',
                    is_staff=True,
                    is_superuser=True,
                    college_name='Admin',
                    skills='Django, Python, System Admin',
                    bio='Platform administrator for CodeBuddy.',
                )
            )
            if created:
                admin.set_password(admin_pass)
                admin.save()
                UserProfile.objects.get_or_create(user=admin)
                self.stdout.write(self.style.SUCCESS(f'  ✅ Admin created: {admin_email}'))
            else:
                if admin.role != 'admin':
                    admin.role = 'admin'
                    admin.is_staff = True
                    admin.is_superuser = True
                    admin.save()
                self.stdout.write(f'  ℹ️  Admin exists: {admin_email}')

        # ── USERS ──────────────────────────────────────────────────────
        user_objs = []
        for full_name, email, password, college, year, skills, bio, available in USERS:
            u, created = User.objects.get_or_create(
                email=email,
                defaults=dict(
                    full_name=full_name,
                    college_name=college,
                    year_of_study=year,
                    skills=skills,
                    bio=bio,
                    available_now=available,
                    reputation_score=round(3.5 + (hash(email) % 30) / 20, 1),
                )
            )
            if created:
                u.set_password(password)
                u.save()
                UserProfile.objects.get_or_create(user=u)
                self.stdout.write(self.style.SUCCESS(f'  ✅ User: {email} / {password}'))
            else:
                self.stdout.write(f'  ℹ️  User exists: {email}')
            user_objs.append(u)

        # ── PROJECTS ───────────────────────────────────────────────────
        project_objs = []
        for i, pd in enumerate(PROJECTS):
            owner = user_objs[pd['owner_idx']]
            proj, created = Project.objects.get_or_create(
                title=pd['title'],
                defaults=dict(
                    owner=owner,
                    teaser=pd['teaser'],
                    description=pd['description'],
                    full_description=pd['full_description'],
                    required_skills=pd['skills'],
                    max_team_size=pd['max_size'],
                    difficulty=pd['difficulty'],
                    status=pd['status'],
                    is_active=True,
                    privacy_level='public',
                )
            )
            if created:
                # Owner member
                ProjectMember.objects.get_or_create(project=proj, user=owner, defaults={'role': 'Owner'})
                # Other members
                for midx in pd['members']:
                    m = user_objs[midx]
                    ProjectMember.objects.get_or_create(project=proj, user=m, defaults={'role': 'Member'})
                # Tasks
                for title, desc, status, assignee_idx in pd['tasks']:
                    assignee = user_objs[assignee_idx] if assignee_idx is not None else None
                    ProjectTask.objects.create(project=proj, title=title, description=desc, status=status, assignee=assignee)
                # Messages
                for uidx, content in pd['messages']:
                    msg_user = user_objs[uidx]
                    Message.objects.create(project=proj, user=msg_user, content=content)
                # Join Requests
                for ridx, msg in pd['requests']:
                    requester = user_objs[ridx]
                    JoinRequest.objects.get_or_create(project=proj, user=requester, defaults={'message': msg, 'status': 'pending'})
                    Notification.objects.create(
                        user=owner,
                        type='join_request',
                        content=f'{requester.full_name} requested to join "{proj.title}"',
                        link=f'/projects/{proj.id}/'
                    )
                self.stdout.write(self.style.SUCCESS(f'  ✅ Project: {pd["title"]}'))
            else:
                self.stdout.write(f'  ℹ️  Project exists: {pd["title"]}')
            project_objs.append(proj)

        # ── FRIENDSHIPS ────────────────────────────────────────────────
        friend_pairs = [(0,1),(0,7),(1,3),(2,5),(3,7),(4,6),(1,2)]
        for a, b in friend_pairs:
            u1, u2 = user_objs[a], user_objs[b]
            if not Friendship.objects.filter(user1=u1, user2=u2).exists() and \
               not Friendship.objects.filter(user1=u2, user2=u1).exists():
                Friendship.objects.create(user1=u1, user2=u2)
                FriendRequest.objects.get_or_create(from_user=u1, to_user=u2, defaults={'status': 'accepted'})

        # Pending friend requests
        pending_pairs = [(5,0),(6,1),(7,4)]
        for a, b in pending_pairs:
            u1, u2 = user_objs[a], user_objs[b]
            if not FriendRequest.objects.filter(from_user=u1, to_user=u2).exists():
                FriendRequest.objects.create(from_user=u1, to_user=u2, status='pending')
                Notification.objects.create(
                    user=u2,
                    type='friend_request',
                    content=f'{u1.full_name} sent you a friend request.',
                    link='/social/people/'
                )

        self.stdout.write(self.style.SUCCESS(f'  ✅ Friendships & requests seeded'))

        # ── SUPPORT TICKETS ────────────────────────────────────────────
        for uidx, subject, category, message in TICKETS:
            u = user_objs[uidx]
            SupportTicket.objects.get_or_create(user=u, subject=subject, defaults={
                'category': category, 'message': message, 'status': 'open'
            })
        self.stdout.write(self.style.SUCCESS(f'  ✅ Support tickets seeded'))

        # ── NOTIFICATIONS ──────────────────────────────────────────────
        Notification.objects.get_or_create(
            user=user_objs[0],
            content='Your project "CampusEats" now has 3 members! 🎉',
            defaults={'type': 'general', 'is_read': False}
        )
        Notification.objects.get_or_create(
            user=user_objs[2],
            content='Priya Mehta applied to join MindMap AI — check the join requests.',
            defaults={'type': 'join_request', 'is_read': False}
        )

        # ── SUMMARY ────────────────────────────────────────────────────
        self.stdout.write('\n' + '='*55)
        self.stdout.write(self.style.SUCCESS('✅  CodeBuddy seeded successfully!\n'))
        self.stdout.write('🌐  URL:  http://127.0.0.1:8000\n')
        self.stdout.write('─'*55)
        self.stdout.write(self.style.WARNING('  ADMIN LOGINS'))
        self.stdout.write(f'  📧  mahadevsaichandra777@gmail.com   🔑  admin@123')
        self.stdout.write(f'  📧  akshayrajsunny006@gmail.com      🔑  Akshay@006\n')
        self.stdout.write(self.style.WARNING('  STUDENT ACCOUNTS'))
        for full_name, email, password, college, *_ in USERS:
            self.stdout.write(f'  📧  {email:<35} 🔑  {password}')
        self.stdout.write('─'*55)
        self.stdout.write(f'  {User.objects.count()} users  ·  {Project.objects.count()} projects  ·  {ProjectTask.objects.count()} tasks  ·  {Message.objects.count()} messages')
        self.stdout.write('='*55 + '\n')
