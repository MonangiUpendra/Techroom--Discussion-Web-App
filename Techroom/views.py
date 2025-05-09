from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm, CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Message  
from .models import User
from .forms import UserForm



# Room Detail View
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = Message.objects.filter(room=room)
    
    # ✅ Add user to participants when they enter the room
    if request.user.is_authenticated:
        room.participants.add(request.user)

    participants = room.participants.all()  # Now participants will be updated

    print(participants)  # Debugging step

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    return render(request, 'base/room.html', {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    })

def userprofile(request, pk):
    profile_user = User.objects.get(id=pk)
    rooms = profile_user.room_set.all()
    room_messages = profile_user.message_set.all()
    topics = Topic.objects.all()
    
    context = {
        'profile_user': profile_user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
    }
    return render(request, 'base/profile.html', context)


# Create Room View
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics=Topic.objects.all()
    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    return render(request, 'base/room_form.html', {'form': form,'topics':topics})

# Home Page View
def home(request):
    query = request.GET.get('q', '')  
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ) if query else Room.objects.all().order_by('-created_at')

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=query))


    return render(request, 'base/home.html', {'rooms': rooms, 'topics': topics, 'room_count': room_count,'room_messages':room_messages})

# Update Room View
@login_required(login_url='login')
def updateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        messages.error(request, "You are not allowed to perform this action!")
        return redirect('home')

    form = RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.method == "POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')

    return render(request, 'base/room_form.html', {'form': form,'topics':topics,'room':room})

# Delete Room View
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        messages.error(request, "You are not allowed to perform this action!")
        return redirect('home')

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

# Login View
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)  # Check if using email or username
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'base/login_register.html', {'page': 'login'})

# Logout View
def logoutUser(request):
    logout(request)
    return redirect('home')

# Register View

def registerpage(request):
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)  # ✅ Add request.FILES for avatar
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    context = {'form': form, 'page': 'register'}
    return render(request, 'base/login_register.html', context)






@login_required(login_url='login')
def deletemessage(request, pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed here')
    if request.method == "POST":
        room = message.room  # ✅ Get the actual room instance
        message.delete()  # ✅ Delete the message, not the room

        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})



@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            login(request, user)  # Re-login after password change
            return redirect('home')

    return render(request, 'base/update-user.html', {'form': form})


def topicspage(request):
    query = request.GET.get('q', '')
    
    if query:
        topics = Topic.objects.filter(name__icontains=query)
    else:
        topics = Topic.objects.all()
        
    total_count = Topic.objects.count()  # optional: for "All (total)" display

    return render(request, 'base/topics.html', {
        'topics': topics,
        'total_count': total_count  # optional
    })

def activitypage(request):
    room_messages=Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})