from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Fish, Lure
from .forms import FeedingForm



# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def fish_index(request):
  fish = Fish.objects.filter(user=request.user)
  return render(request, 'fish/index.html', { 'fish': fish })

@login_required
def fish_detail(request, fish_id):
  fish = Fish.objects.get(id=fish_id)
  lures_fish_doesnt_have = Lure.objects.exclude(id__in = fish.lures.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'fish/detail.html', {
    'fish': fish, 'feeding_form': feeding_form,
    'lures': lures_fish_doesnt_have
  })

class FishCreate(LoginRequiredMixin, CreateView):
  model = Fish
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class FishUpdate(LoginRequiredMixin, UpdateView):
  model = Fish
  fields = ['breed', 'description', 'age']

class FishDelete(LoginRequiredMixin, DeleteView):
  model = Fish
  success_url = '/fish/'

@login_required
def add_feeding(request, fish_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the fish_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.fish_id = fish_id
    new_feeding.save()
  return redirect('detail', fish_id=fish_id)

class LureList(LoginRequiredMixin, ListView):
  model = Lure

class LureDetail(LoginRequiredMixin, DetailView):
  model = Lure

class LureCreate(LoginRequiredMixin, CreateView):
  model = Lure
  fields = '__all__'

class LureUpdate(LoginRequiredMixin, UpdateView):
  model = Lure
  fields = ['name', 'color']

class LureDelete(LoginRequiredMixin, DeleteView):
  model = Lure
  success_url = '/lures/'

@login_required
def assoc_lure(request, fish_id, lure_id):
  # Note that you can pass a lure's id instead of the whole object
  Fish.objects.get(id=fish_id).lures.add(lure_id)
  return redirect('detail', fish_id=fish_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)