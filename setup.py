#!/usr/bin/env python
"""
CodeBuddy Setup Script
Run this once to initialize the database and create the admin user.

Usage:
    python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codebuddy.settings')

def main():
    print("=" * 55)
    print("  ⚡ CodeBuddy — Setup Script")
    print("=" * 55)

    # Setup Django
    django.setup()

    from django.core.management import call_command
    from apps.auth_app.models import User, UserProfile

    print("\n📦 Running migrations...")
    call_command('makemigrations', '--noinput', verbosity=0)
    call_command('migrate', '--noinput', verbosity=1)

    print("\n👤 Creating admin user...")
    admin_email = 'mahadevsaichandra777@gmail.com'
    admin_password = 'password'

    if not User.objects.filter(email=admin_email).exists():
        admin = User.objects.create_user(
            email=admin_email,
            password=admin_password,
            full_name='Admin User',
            role='admin',
            is_staff=True,
            is_superuser=True,
        )
        UserProfile.objects.create(user=admin)
        print(f"  ✅ Admin created: {admin_email} / {admin_password}")
    else:
        print(f"  ℹ️  Admin already exists: {admin_email}")

    print("\n🌱 Creating sample data...")
    create_sample_data()

    print("\n" + "=" * 55)
    print("  ✅ Setup complete!")
    print("=" * 55)
    print("\n🚀 Start the server:")
    print("   python manage.py runserver")
    print("\n🌐 Open: http://localhost:8000")
    print("   Admin login: mahadevsaichandra777@gmail.com / password")
    print()


def create_sample_data():
    from apps.auth_app.models import User, UserProfile
    from apps.projects.models import Project, ProjectMember

    # Sample students
    students = [
        {'email': 'alice@campus.edu', 'full_name': 'Alice Chen', 'skills': 'React, TypeScript, UI/UX', 'college_name': 'MIT', 'year_of_study': '3rd', 'available_now': True, 'bio': 'Frontend dev passionate about beautiful interfaces'},
        {'email': 'bob@campus.edu', 'full_name': 'Bob Patel', 'skills': 'Python, ML, TensorFlow', 'college_name': 'Stanford', 'year_of_study': '4th', 'available_now': True, 'bio': 'ML researcher building AI tools for students'},
        {'email': 'carol@campus.edu', 'full_name': 'Carol Martinez', 'skills': 'Node.js, AWS, DevOps', 'college_name': 'UC Berkeley', 'year_of_study': '2nd', 'available_now': False, 'bio': 'Backend engineer and cloud architecture enthusiast'},
        {'email': 'dave@campus.edu', 'full_name': 'Dave Kim', 'skills': 'iOS, Swift, Figma', 'college_name': 'CMU', 'year_of_study': '1st', 'available_now': True, 'bio': 'Mobile developer with an eye for design'},
    ]

    created_users = []
    for s in students:
        if not User.objects.filter(email=s['email']).exists():
            u = User.objects.create_user(
                email=s['email'],
                password='password123',
                full_name=s['full_name'],
                skills=s['skills'],
                college_name=s['college_name'],
                year_of_study=s['year_of_study'],
                available_now=s['available_now'],
                bio=s['bio'],
            )
            UserProfile.objects.create(user=u)
            created_users.append(u)
            print(f"  ✅ Created user: {u.full_name} ({u.email})")

    # Sample projects
    if User.objects.filter(email='alice@campus.edu').exists():
        alice = User.objects.get(email='alice@campus.edu')
        bob = User.objects.get(email='bob@campus.edu') if User.objects.filter(email='bob@campus.edu').exists() else None

        projects_data = [
            {
                'owner': alice,
                'title': 'CampusAI Study Assistant',
                'teaser': 'AI-powered tool to help students study smarter',
                'description': 'Building an intelligent study assistant that uses NLP to summarize lecture notes, generate practice questions, and track student progress.',
                'required_skills': 'Python ML React',
                'difficulty': 'intermediate',
                'status': 'recruiting',
                'max_team_size': 4,
            },
            {
                'owner': bob if bob else alice,
                'title': 'Campus Event Hub',
                'teaser': 'Centralizing all campus events in one beautiful app',
                'description': 'A mobile-first platform where students discover, RSVP, and share campus events — clubs, workshops, hackathons, and more.',
                'required_skills': 'React Native Firebase',
                'difficulty': 'beginner',
                'status': 'recruiting',
                'max_team_size': 5,
            },
            {
                'owner': alice,
                'title': 'Peer Tutoring Marketplace',
                'teaser': 'Connect students who need help with those who can teach',
                'description': 'A platform for peer tutoring sessions — schedule, pay, and review tutors within your campus network.',
                'required_skills': 'Django PostgreSQL Stripe',
                'difficulty': 'advanced',
                'status': 'in_progress',
                'max_team_size': 3,
            },
        ]

        for pd in projects_data:
            if not Project.objects.filter(title=pd['title']).exists():
                p = Project.objects.create(**pd)
                ProjectMember.objects.create(project=p, user=pd['owner'], role='Owner')
                print(f"  ✅ Created project: {p.title}")


if __name__ == '__main__':
    main()
