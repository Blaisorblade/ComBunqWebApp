from django.shortcuts import render, redirect
from .forms import GenerateKeyForm, decrypt_form
from .installation import installation
from django.utils.encoding import smart_str
from django.http import HttpResponse
# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import json
from .encryption import AESCipher
from pprint import pprint

# from django.http.response import FileResponse

# Create your views here.


def error(request, error=None):  # NOTE: render error pages
    '''
    Views to show error pages. This is not working smooth, need to think of
    another way to show errors.
    '''
    if error == 'not_your_file':
        return render(request, 'BunqAPI/error/notYourFile.html')
    elif error == 'not_logged_in':
        return render(request, 'BunqAPI/error/notLogIn.html')
    else:
        raise Http404


@otp_required  # NOTE: forces the user to log in with 2FA
def generate(request):
    '''
    This is working smooth.
    View that handles the /generate page.
    '''
    if request.method == 'POST':
        formKey = GenerateKeyForm(request.POST)
        if formKey.is_valid():
            print ('\n\nGenerating...\n\n')
            username = request.user.username
            API = formKey.cleaned_data['API']
            encryption_password = formKey.cleaned_data['encryption_password']
            data = installation(username, encryption_password, API)
            encryptedData = data.encrypt()
            response = HttpResponse(
                encryptedData, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('BunqWebApp.json')  # noqa
            return response

    else:
        formKey = GenerateKeyForm()
    return render(request, 'BunqAPI/index.html', {'form': formKey})


@otp_required
def decrypt(request):
    ''''View that handles /decrypt page. However need to think of new way
    to decpyt the file and use it, this is not the right way to do it.
    Well atleast the JS part is a little bit messy.'''
    if request.method == 'POST':
        form = decrypt_form(request.POST)
        try:
            user = User.objects.get(username=request.user)
        except ObjectDoesNotExist:
            print('user does not extist')
            return redirect('./error/not_logged_in')
        else:
            userGUID = user.profile.GUID
            inputData = json.loads(
                request.POST['json'])
            password = request.POST['pass']
            if inputData['userID'] == userGUID:
                p = AESCipher(password)
                data = json.loads(AESCipher.decrypt(p, inputData['secret']))
                return HttpResponse(json.dumps(data, indent=4))
            else:
                return redirect('./error/not_your_file')
            if action == 'register':
                s = session(data)
                try:
                    return HttpResponse(json.dumps(s.register(), indent=4))  # noqa
                except KeyError:
                    return HttpResponse(json.dumps(data, indent=4))
                # print(type(data))
                # return HttpResponse(json.dumps(register(data), indent=4))
            elif action == 'start_session':
                s = session(data)
                return HttpResponse(json.dumps(s.start_session(), indent=4))

    else:
        form = decrypt_form()
    return render(request, 'BunqAPI/decrypt.html', {'form': form})
