from django.shortcuts import render ,redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.

    
def logout_details(request):
    
    logout(request)

    return redirect('login')



def signup_details(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        
    else:
        form = UserCreationForm()

    return render (request, 'registration/signup.html', {"form":form})

#BUNLARI YANİ LOGIN i djangonun kendi defaultndan kullandım 


# def login_details(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             user = form.get_user()  #Eğer form geçerliyse doğrulanan User nesnesini alıyoruz.
#             login(request, user)
#             return redirect('CategoryPage')   #normalde home a gitmesini isterim ama şu an yok 
        
#     else :
#         form = AuthenticationForm()

#     return render(request, 'registration/login.html', {"form":form})
    