from PIL import Image
from django.shortcuts import render, redirect
from django.http import HttpResponse
import pyrebase

with open("LIVTU_MAIN/firebase.py", 'r') as file:
    exec(file.read())

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage = firebase.storage()

def home(request):
    return render(request, "LIVTU_MAIN/home.html")

def about(request):
    return render(request, "LIVTU_MAIN/about.html")

def teach(request):
    return render(request, "LIVTU_MAIN/teach.html")

def study(request):
    return render(request, "LIVTU_MAIN/study.html")

def terms(request):
    return render(request, "LIVTU_MAIN/legal/terms.html")

def privacy(request):
    return render(request, "LIVTU_MAIN/legal/privacy.html")

def contact(request):
    return render(request, "LIVTU_MAIN/legal/contact.html")

def support(request):
    return render(request, "LIVTU_MAIN/support.html")

def jobs(request):
    return render(request, "LIVTU_MAIN/jobs.html")

def signIn(request):
    return render(request,"LIVTU_MAIN/Login.html")
 
def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    try:
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Wrong Email or Password"
        return redirect('login',{"msg":message})
    uid = str(user['localId'])
    session_id=user['idToken']
    request.session['uid']=uid
    return redirect('home')
 
def logout(request):
    try:
        del request.session['uid']
        return redirect('login')
    except:
        return redirect('login', data={"msg":"Logout Failed"})
 
def signUp(request):
    return render(request,"LIVTU_MAIN/Registration.html")
 
def postsignUp(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    name = request.POST.get('name')
    passwordrepeat = request.POST.get('pass-repeat')
    if(password==passwordrepeat):
        try:
            user=authe.create_user_with_email_and_password(email,password)
            uid = str(user['localId'])
            idtoken = request.session['uid']
            print(uid)
        except:
            return redirect('signup')
        return redirect('login')
    else:
        return redirect('signup',data={"msg":"Passwords not identical. Please try again"})

def reset(request):
	return render(request, "LIVTU_MAIN/Reset.html")

def postReset(request):
	email = request.POST.get('email')
	try:
		authe.send_password_reset_email(email)
		message = "Reset link sent"
		return redirect('home', data={"msg":message})
	except:
		message = "Could not find Email"
		return redirect('reset', data={"msg":message})

def profile(request):
    try:
        request.session['uid']
        userLoggedIn = True
    except:
        userLoggedIn = False
    if userLoggedIn:
        return render(request, "LIVTU_MAIN/profile.html")
    else:
        return redirect('login')

def changeProfile(request):
    try:
        request.session['uid']
        userLoggedIn = True
    except:
        userLoggedIn = False
    if userLoggedIn:
        if request.method == "POST":
            image = request.FILES.get("profilePicture")
            user_id = request.session.get("uid")
            image_path = f"profile_pictures/{user_id}.png"
            if image:
                storage.child(image_path).put(image)
                return redirect('profileEdit')
            else:
                return redirect('profileEdit')
        else:
            return render(request, "LIVTU_MAIN/ChangeProfile.html")
    else:
        return redirect('login')