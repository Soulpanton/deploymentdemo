from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render(request, "login_registration.html")


def login(request):
    login_validator = User.objects.login_validator(request.POST)

    if len(login_validator) > 0:
        for key, value in login_validator.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email_found_database = User.objects.filter(
            email=request.POST['login_email'])
        request.session['loggedInId'] = email_found_database[0].id
    return redirect('/quotes')


def register(request):
    validator_errors = User.objects.registration_validator(request.POST)

    if len(validator_errors) > 0:
        for key, value in validator_errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        new_user = User.objects.create(first_name=request.POST['form_name'], last_name=request.POST['form_last'],
                                       email=request.POST['form_email'], password=request.POST['form_password'])
        request.session['loggedInId'] = new_user.id

    return redirect('/quotes')


def quotes_list(request):
    # if "loggedInId" not in request.session:
    #     return redirect('/')

    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'allQuotes': Quote.objects.all(),
        'allUsers': User.objects.all()
    }
    return render(request, "quotes_page.html", context)


def add_quote(request):
    errors_from_quote_validator = Quote.objects.addQuote_validator(
        request.POST)

    if len(errors_from_quote_validator) > 0:
        for key, value in errors_from_quote_validator.items():
            messages.error(request, value)
        return redirect('/quotes')

    else:
        new_quote = Quote.objects.create(
            author=request.POST['quote_author'], content=request.POST['quote_content'], posted_by=User.objects.get(id=request.session['loggedInId']))
        return redirect('/quotes')


def all_their_quotes(request, userId):
    context = {
        "thisUser": User.objects.get(id=userId),



    }
    return render(request, "user_quotes.html", context)


def like(request, quoteId):
    Quote.objects.get(id=quoteId).likers.add(
        User.objects.get(id=request.session['loggedInId']))
    return redirect('/quotes')


def delete(request, quoteId):
    to_delete = Quote.objects.get(id=quoteId)
    to_delete.delete()
    return redirect('/quotes')


def edit(request, userId):
    context = {
        "thisUser": User.objects.get(id=request.session['loggedInId'])
    }
    return render(request, "myAccount.html", context)


def update(request, thisUserId):
    update_validator_errors = User.objects.edit_validator(request.POST)

    if len(update_validator_errors) > 0:
        for key, value in update_validator_errors.items():
            messages.error(request, value)
        return redirect(f'/edit/{thisUserId}')

    else:
        userUpdate = User.objects.get(id=thisUserId)
        userUpdate.first_name = request.POST['edit_first']
        userUpdate.last_name = request.POST['edit_last']
        userUpdate.email = request.POST['edit_email']
        userUpdate.save()
    return redirect("/quotes")


def logout(request):
    request.session.clear()
    return redirect('/')
