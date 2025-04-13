from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, ProfileUpdateForm, OptionalPasswordChangeForm, RoomForm, TeamForm
from .models import Room, Rool
from .models import Team, Task
from django.contrib import messages
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

from django.utils import timezone
User = get_user_model()

def home(request):
    return render(request, 'html/home.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'html/login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'html/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        password_form = OptionalPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            if password_form.is_valid() and password_form.cleaned_data.get("new_password1"):
                password_form.save()
                update_session_auth_hash(request, password_form.user)
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
        password_form = OptionalPasswordChangeForm(user)

    return render(request, 'html/profile.html', {
        'form': form,
        'password_form': password_form,
        'user_profile': user,
    })

@login_required
def room_list(request):
    query = request.GET.get('q', '').strip()
    user_rooms = Room.objects.filter(rools__user=request.user).distinct()
    if query:
        user_rooms = user_rooms.filter(name__icontains=query)

    context = {
        'rooms': user_rooms,
        'query': query,
    }
    return render(request, 'html/rooms.html', context)

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            Rool.objects.create(room=room, user=request.user, role='admin')
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'html/create_room.html', {'form': form})

@login_required
def create_team(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.room = room
            team.created_by = request.user
            team.save()
            team.members.add(request.user)
            return redirect('room_detail', room_id=room.id)
    else:
        form = TeamForm()
    return render(request, 'html/create_team.html', {'form': form, 'room': room})

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    role_obj = Rool.objects.filter(room=room, user=request.user).first()
    user_role = role_obj.role if role_obj else 'user'

    if request.method == "POST":
        if 'assign_moderator' in request.POST and user_role == 'admin':
            user_id = request.POST.get('moderator_user_id')
            rool = Rool.objects.filter(room=room, user_id=user_id).first()
            if rool:
                rool.role = 'moderator'
                rool.save()
                messages.success(request, 'Пользователь назначен модератором.')
        # Создание команды
        if 'create_team' in request.POST:
            team_name = request.POST.get('team_name')
            if team_name:
                Team.objects.create(name=team_name, room=room, created_by=request.user)
                messages.success(request, 'Команда создана.')

        # Удаление команды
        elif 'delete_team' in request.POST:
            team_id = request.POST.get('delete_team_id')
            Team.objects.filter(id=team_id, room=room).delete()
            messages.success(request, 'Команда удалена.')

        # Добавление пользователя в команду
        elif 'add_to_team' in request.POST:
            team_id = request.POST.get('team_id')
            user_id = request.POST.get('user_id')
            team = Team.objects.get(id=team_id)
            user = User.objects.get(id=user_id)
            team.members.add(user)
            messages.success(request, f'{user.username} добавлен в команду.')

        # Создание задачи
        elif 'create_task' in request.POST:
            deadline_str = request.POST.get('deadline')
            deadline = parse_datetime(deadline_str) if deadline_str else None
            Task.objects.create(
                title=request.POST.get('task_title'),
                description=request.POST.get('task_description'),
                room=room,
                team_id=request.POST.get('team_id') or None,
                assigned_to_id=request.POST.get('assigned_to') or None,
                deadline=deadline
            )
            messages.success(request, 'Задача создана.')

        # Редактирование задачи
        elif 'edit_task' in request.POST:
            task = Task.objects.get(id=request.POST.get('task_id'))
            task.title = request.POST.get('task_title')
            task.description = request.POST.get('task_description')
            task.status = request.POST.get('new_status')
            task.assigned_to_id = request.POST.get('assigned_to') or None
            deadline_str = request.POST.get('deadline')
            task.deadline = parse_datetime(deadline_str) if deadline_str else None
            task.save()
            messages.success(request, 'Задача обновлена.')

        # Удаление задачи
        elif 'delete_task' in request.POST:
            Task.objects.filter(id=request.POST.get('task_id')).delete()
            messages.success(request, 'Задача удалена.')

        # Обычный пользователь меняет статус задачи
        elif 'update_status' in request.POST:
            task = Task.objects.get(id=request.POST.get('task_id'))
            task.status = request.POST.get('new_status')
            task.save()
            messages.success(request, 'Статус задачи обновлен.')

        # Добавление пользователя в комнату
        elif 'add_user' in request.POST:
            username = request.POST.get('username')
            user = User.objects.filter(username=username).first()
            if user:
                Rool.objects.create(user=user, room=room, role='user')
                messages.success(request, f'Пользователь {username} добавлен.')

    teams = Team.objects.filter(room=room)
    tasks = Task.objects.filter(room=room)
    users = Rool.objects.filter(room=room)
    all_users = User.objects.all()

    return render(request, 'html/room_detail.html', {
        'room': room,
        'user_role': user_role,
        'teams': teams,
        'tasks': tasks,
        'users': users,
        'all_users': all_users,
    })


@login_required
def user_autocomplete(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)[:5]
    data = [{'username': u.username} for u in users]
    return JsonResponse(data, safe=False)