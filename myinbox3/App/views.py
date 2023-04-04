import os
import openai
from django.shortcuts import render, redirect

from decouple import config #hide secrets
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control  # Clear after logout
from django.contrib import messages  # return messages
from django.http import HttpResponseRedirect, HttpResponse  # redirect the pages
from django.core.paginator import Paginator  # Pagination
from django.db.models import Q  # Global Search
from datetime import datetime  # to get Today's message
from django.core.mail import EmailMultiAlternatives, send_mail, BadHeaderError  # Send mails
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import logout  # To auto logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models import query_utils
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import SignUpForm, Customerform, EmailForm
from .models import Chat, Customer


# =========== FRONT END ===================
def home(request):
    return render(request, "home.html")


def sendMessage(request):
    if request.method == "POST":
        form = Customerform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Message send successfully! ")
            return HttpResponseRedirect('/')
    else:
        form = Customerform()
    return render(request, 'home.html', {'form': form})

# ============ BACK END =================


@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inbox(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_customer_list = Customer.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q) | Q(
                subject__icontains=q) | Q(status__icontains=q) | Q(message__icontains=q)
        ).order_by('-created_at')
    else:
        all_customer_list = Customer.objects.all().order_by('-created_at')

    paginator = Paginator(all_customer_list, 10)
    page = request.GET.get('page')
    all_customer = paginator.get_page(page)

    # Messages counter
    # Total
    total = Customer.objects.all().count()
    # Read
    read = Customer.objects.filter(status='Read')
    # Unread
    unread = Customer.objects.filter(status='Pending')
    # Today
    base = datetime.now().date()
    today = Customer.objects.filter(created_at__gt=base)

    context = {'customers': all_customer, 'total': total,
               'read': read, 'unread': unread, 'today': today}
    return render(request, "inbox.html", context)


@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteMessage(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    messages.success(request, "Message deleted successfully !")
    return HttpResponseRedirect('/inbox')

# View message individually


@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Customers(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if customer != None:
        return render(request, "customer.html", {'customer': customer})


@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def markAsRead(request):
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.POST.get('id'))
        if customer != None:
            customer.status = request.POST.get('status')
            customer.save()
            messages.success(request, "Message marked as read!")
            return HttpResponseRedirect('/inbox')


def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        company = "Reply from OurProject"
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email = form.cleaned_data["email"]
            cc = form.cleaned_data["cc"]
            files = request.FILES.getlist("attach")
            html_content = render_to_string("email.html", {
                                            'subject': subject, 'content': message, 'email': email, 'cc': cc, 'files': files})
            text_content = strip_tags(html_content)

            mails = EmailMultiAlternatives(
                subject, text_content, company, [email], [cc])

            # mail = EmailMessage(subject, message, company, [email], [cc])
            for f in files:
                mails.attach(f.name, f.read(), f.content_type)
            mails.attach_alternative(html_content, "text/html")
            mails.send()
            messages.success(request, "Reply sent successfully !")
            return HttpResponseRedirect('/inbox')
        else:
            messages.error(request, "Invalid email")
            return HttpResponseRedirect('/inbox')
    else:
        form = EmailForm()
        return render(request, {'form': form})


def AutoLogoutUser(request):
    logout(request)
    request.user = None
    messages.info(request, ".")  # The argument can't be empty
    return HttpResponseRedirect('/')

############  ERRORS ###########


def E_500(request):
    return render(request, 'e500.html')


def E_404(request, exception):
    return render(request, 'e404.html')


def About(request):
    return render(request, 'about.html')


def Profile(request):
    return render(request, 'profiles.html')


def Feedback(request):
    return render(request, 'feedback.html')

# BOT views
# Sending of request and saving it in our model


@login_required(login_url='login')
def AiChat(request):
    # Form verification
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        ai_response = generate_response(user_input)
        # Saving both user_input and ai_response in the database
        Chat.objects.create(user=request.user,
                            user_input=user_input, ai_response=ai_response)

    else:
        # if user did not enter any input nothing should be sent
        user_input = ''
        ai_response = None
    # Displaying the chat history base on user
    chat_history = Chat.objects.filter(
        user=request.user).order_by('-timestamp')

    context = {
        'user_input': user_input,
        'chatbot_response': ai_response,
        'chat_history': chat_history,

    }
    return render(request, 'bot.html', context)


# Generating response from openai Library
# Use the OpenAI API to generate a response
openai.api_key=config('MY_API_KEY')


def generate_response(user_input):
    prompt = (f"User: {user_input}")
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message.strip()

# Clear chat


def clear_chat(request):
    # clear the 'name' field for all records in the 'MyModel' model
    Chat.objects.all().delete()
    return redirect('bot')

def forget_info(request):
     return render(request, "registration/reset_password.html")

# Reset Password View
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(query_utils.Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'OurProject',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'project.nasra@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/reset_password.html", context={"password_reset_form":password_reset_form})