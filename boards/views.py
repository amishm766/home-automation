import RPi.GPIO as GPIO
from boards.forms import SignUpForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from boards.tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

def home(request):
    return HttpResponse('Hello World!!!!!')

def verifyEmail(request):
    return render(request, "verification.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            sendSimpleEmail(request)
            data = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            }
            return render(request, 'account_activation_email.html',data)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activateUser(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'account_activation_invalid.html')

def sendSimpleEmail(request, emailto="am9713490290@gmail.com"):
    res = send_mail("Veryfication Email", "Verification link", "amishm766@gmail.com", [emailto])
    return HttpResponse('%s'%res)
#    email = EmailMessage('Verification Email', 'Body', to=['am9713490290@gmail.com'])
#    email.send()

def auto(request, appliance=None, action=None):
    led = (26,12,16,20)
    ledSts = ['0','0','0','0']
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in led:
        GPIO.setup(pin, GPIO.OUT)

    if True :
        """ check for which appliance the request is created from webpage """
        if appliance == 'led0':
            actuator = led[0]
        elif appliance == 'led1':
            actuator = led[1]
        elif appliance == 'led2':
            actuator = led[2]
        elif appliance == 'led3':
            actuator = led[3]
        else:
            pass

        """ take action on the appliances as per the request"""
        GPIO.output(actuator, GPIO.HIGH) if action == 'ON' else GPIO.output(actuator, GPIO.LOW)

        """ Reading status of the appliances whether ON or OFF """
        for pin in range(len(led)):
            ledSts[pin] = GPIO.input(led[pin])

        """ the values or data that has to be returned to webpage """
        data = {
                'led0' : ledSts[0],
                'led1' : ledSts[1],
                'led2' : ledSts[2],
                'led3' : ledSts[3]
                }

        """ return the data to the html page(index.html) """
        return render(request, "automation.html", data)

    else:
        return redirect(('/'))

def autoPage(request):
    return render(request, 'automation.html')
