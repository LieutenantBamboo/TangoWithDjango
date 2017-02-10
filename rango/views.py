from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if (form.is_valid()):
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def index(request):
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, 'rango/about.html')


def register(request):
    # Boolean whether registration was successful, false by default
    registered = False

    # If POST, process data
    if request.method == 'POST':
        # Attempt to grab information from the raw input data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save user data to database
            user = user_form.save()

            # Hashes the user password and updates it with the save method
            user.set_password(user.password)
            user.save()

            # Holds back the saving of the profile model
            # until data integrity is confirmed
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user supply a profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Save the UserProfile model instance
            profile.save()

            # Show the user registration was successful
            registered = True
        else:
            # Invalid form(s): Print errors to console/log
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the tempalte depending on the context
    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # Requests information using getter
        # methods that return 'None' if no info
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticates information
        user = authenticate(username=username, password=password)

        if user:

            # If active
            if user.is_active:
                # Logs user in, sends back to homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # Warns the user that their account is inactive
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details
            print("Bad login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid username or password")

    # If not POST (positng details), then it's GET, therefore login form is displayed
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
