from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .forms import EditCustomUserForm


# Check which user type and redirect to respective homes
@login_required(login_url='/login/')
def home(request):
    # Check checkbox by default
    context = {
        'id_checkbox': True,
        'email_checkbox': True,
        'full_name_checkbox': True,
        'phone_number_checkbox': True,
        'address_checkbox': True
    }
    # If not logged in, go home
    if not request.user.is_authenticated:
        return redirect('home')
    # Admin
    elif request.user.user_type == 'admin':
        try:
            # If searched
            if request.POST:
                search_bar = request.POST['search_bar']
                context['search_bar'] = search_bar
                return render(request, 'admin/admin_home.html', context)
            # If not searched
            else:
                order_by = request.GET.get('order_by', 'id')
                query = request.GET.get('query')
                data = CustomUser.objects.all().order_by(order_by)
                context['acc'] = data
                context['query'] = query
        except CustomUser.DoesNotExist:
            return HttpResponse("Something went wrong")
        return render(request, 'admin/admin_home.html', context)
    # Patient
    elif request.user.user_type == 'patient':
        return render(request, 'patient/patient_home.html')
    # Pharmacist
    elif request.user.user_type == 'pharmacist':
        return render(request, 'pharmacist/pharmacist_home.html')
    # Doctor
    elif request.user.user_type == 'doctor':
        return render(request, 'doctor/doctor_home.html')

# Only admin can edit users
@login_required(login_url='/login/')
def edit_user(request, *args, **kwargs):
    # If not logged in or not admin, go home
    if not request.user.is_authenticated or not request.user.user_type == 'admin':
        return redirect('home')
    # Get user
    user_id = kwargs.get('user_id')
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse("Something went wrong")
    context = {}
    context['is_superuser'] = user.is_superuser
    # If submitting form
    if request.POST:
        # Get form
        form = EditCustomUserForm(request.POST, instance=user)
        # If form valid, submit
        if form.is_valid():
            form.save()
            return redirect('home')
        # If form not valid, reload with entered values
        else:
            form = EditCustomUserForm(request.POST, instance=user,
                                      initial={
                                          'id': user.pk,
                                          'email': user.email,
                                          'phone_number': user.phone_number,
                                          'full_name': user.full_name,
                                          'address': user.address,
                                          'user_type': user.user_type,
                                          'is_staff': user.is_staff,
                                          'is_active': user.is_active,
                                      }
                                      )
            context['form'] = form
            context['id'] = user.id
    # If getting form
    else:
        # Load with entered values
        form = EditCustomUserForm(instance=user,
                                  initial={
                                      'id': user.pk,
                                      'email': user.email,
                                      'phone_number': user.phone_number,
                                      'full_name': user.full_name,
                                      'address': user.address,
                                      'user_type': user.user_type,
                                      'is_staff': user.is_staff,
                                      'is_active': user.is_active,
                                  })
        context['form'] = form
        context['id'] = user.id
    return render(request, 'admin/edit_user.html', context)

#
@login_required(login_url='/login/')
def search_user(request, *args, **kwargs):
    # If not logged in or not admin, go home
    if not request.user.is_authenticated or not request.user.user_type == 'admin':
        return redirect('home')
    # Get search query stuff
    query = request.GET.get('search_query')
    search_id = request.GET.get('id_checkbox')
    search_email = request.GET.get('email_checkbox')
    search_full_name = request.GET.get('full_name_checkbox')
    search_phone_number = request.GET.get('phone_number_checkbox')
    search_address = request.GET.get('address_checkbox')
    context = {
        'searched': True,
        'query': query,
        'id_checkbox': search_id,
        'email_checkbox': search_email,
        'full_name_checkbox': search_full_name,
        'phone_number_checkbox': search_phone_number,
        'address_checkbox': search_address
    }
    # If searching
    if query:
        try:
            # Empty QuerySet
            all_results = CustomUser.objects.none()
            # If checked id
            if search_id:
                id_results = CustomUser.objects.filter(id__contains=query)
                all_results = all_results | id_results      # Union set
            # If checked email
            if search_email:
                email_results = CustomUser.objects.filter(email__icontains=query)
                all_results = all_results | email_results
            # If checked full name
            if search_full_name:
                full_name_results = CustomUser.objects.filter(full_name__icontains=query)
                all_results = all_results | full_name_results
            # If checked phone number
            if search_phone_number:
                phone_number_results = CustomUser.objects.filter(phone_number__icontains=query)
                all_results = all_results | phone_number_results
            # If checked address
            if search_address:
                address_results = CustomUser.objects.filter(address__icontains=query)
                all_results = all_results | address_results
            # Get order by value
            order_by = request.GET.get('order_by', 'id')
            # Set order
            all_results = all_results.order_by(order_by)
            context['acc'] = all_results
            context['query'] = query
        except CustomUser.DoesNotExist:
            return render(request, 'admin/admin_home.html')
        return render(request, 'admin/admin_home.html', context)
    # If not searching, go home
    else:
        return redirect('home')


@login_required(login_url='/login/')
def delete_user(request, *args, **kwargs):
    # If not logged in or not admin, go home
    if not request.user.is_authenticated or not request.user.user_type == 'admin':
        return redirect('home')
    # Get user id of deleting user
    user_id = kwargs.get('user_id')
    # Try delete, catch DoesNotExist error
    try:
        CustomUser.objects.get(id=user_id).delete()
    except CustomUser.DoesNotExist:
        return HttpResponse(f"User {user_id} does not exist")
    return redirect('home')

