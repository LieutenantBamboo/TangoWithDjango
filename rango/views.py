from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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
        if(form.is_valid()):
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
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')

def register(request):
    # Boolean whether registration was successful, false by default
    registered = False

    # If POST, process data
    if request.method == 'POST':
        # Attempt to grab information from the raw input data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data = request.POST)

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



