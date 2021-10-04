from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .forms import EditCustomUserForm


# Create your views here.
@login_required(login_url='/login/')
def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.is_superuser:
        try:
            order_by = request.GET.get('order_by', 'id')
            data = CustomUser.objects.all().order_by(order_by)
            acc = {"acc_info": data}
        except CustomUser.DoesNotExist:
            return HttpResponse("Something went wrong")
        return render(request, 'admin/admin_home.html', acc)
    elif CustomUser.objects.get(pk=request.user.pk).user_type == 'patient':
        return render(request, 'patient/patient_home.html')
    elif CustomUser.objects.get(pk=request.user.pk).user_type == 'pharmacist':
        return render(request, 'pharmacist/pharmacist_home.html')
    elif CustomUser.objects.get(pk=request.user.pk).user_type == 'doctor':
        return render(request, 'doctor/doctor_home.html')

    return redirect(request, 'home.html')


@login_required(login_url='/login/')
def edit_user(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    user_id = kwargs.get('user_id')
    try:
        account = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return HttpResponse("Something went wrong")
    context = {}
    if request.POST:
        form = EditCustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = EditCustomUserForm(request.POST,
                                      initial={
                                          'id': account.pk,
                                          'email': account.email,
                                          'phone_number': account.phone_number,
                                          'full_name': account.full_name,
                                          'address': account.address,
                                          'user_type': account.user_type,
                                          'is_staff': account.is_staff,
                                          'is_active': account.is_active,
                                      }
                                      )
            context['form'] = form
            context['id'] = account.id
    else:
        form = EditCustomUserForm(
                                  initial={
                                      'id': account.pk,
                                      'email': account.email,
                                      'phone_number': account.phone_number,
                                      'full_name': account.full_name,
                                      'address': account.address,
                                      'user_type': account.user_type,
                                      'is_staff': account.is_staff,
                                      'is_active': account.is_active,
                                  })
        context['form'] = form
        context['id'] = account.id
    return render(request, 'admin/edit_user.html', context)
