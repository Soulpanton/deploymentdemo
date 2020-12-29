from django.db import models
import re


class UserManager(models.Manager):

    def login_validator(self, formInfo):
        errors = {}

        email_found_database = User.objects.filter(
            email=formInfo["login_email"])

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(formInfo['login_email']) < 1:
            errors['loginEmailRequired'] = "Must enter an email"

        elif not EMAIL_REGEX.match(formInfo['login_email']):
            errors['correctPatternEmailRequired'] = "Your email needs to be in proper format"

        elif len(email_found_database) < 1:
            errors['email_not_found'] = "This email was not found on our database, please verify your email or register"

        try:
            password_found_database = User.objects.get(
                email=formInfo["login_email"])
        except:
            return errors

        if len(formInfo['login_password']) < 1:
            errors['loginPasswordRequired'] = "You must enter a password"

        elif len(formInfo['login_password']) < 8:
            errors['loginPasswordMinLength'] = "Your password should be a least 8 characters long"

        elif password_found_database.password != formInfo['login_password']:
            errors["pass_not_match"] = "Your password do not match the registered password for that Email"

        return errors

    def registration_validator(self, formInfo):
        errors = {}
        email_already_taken = User.objects.filter(email=formInfo["form_email"])
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(formInfo['form_name']) < 2:
            errors['nameRequired'] = "First Name is required for Registration"

        if len(formInfo['form_last']) < 2:
            errors['lastNameRequired'] = "Last name is required for Registration"

        if len(formInfo['form_email']) < 1:
            errors['emailRequired'] = "Must enter an email"

        elif not EMAIL_REGEX.match(formInfo['form_email']):
            errors['correctPatternEmailRequired'] = "Your email needs to be in proper format"

        if len(email_already_taken) > 0:
            errors['taken_email'] = "This email has already been used for another User, please select another email or Login"

        if len(formInfo['form_password']) < 1:
            errors['passwordRequired'] = "You must enter a password"

        elif len(formInfo['form_password']) < 8:
            errors['passwordMinLength'] = "Your password should be a least 8 characters long"

        if len(formInfo['form_confirmation']) < 1:
            errors['confirmationRequired'] = "You must confirm your password for verification"
        elif formInfo['form_confirmation'] != formInfo['form_password']:
            errors['passwordDoNotMatch'] = "Your passwords did not match please try again"

        return errors

    def edit_validator(self, formInfo):
        errors = {}
        email_already_taken = User.objects.filter(email=formInfo["edit_email"])
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(formInfo['edit_first']) < 1:
            errors['nameEditRequired'] = "First Name is required for Update"

        if len(formInfo['edit_last']) < 1:
            errors['lastNameRequired'] = "Last name is required for Registration"

        if len(formInfo['edit_email']) < 1:
            errors['emailRequired'] = "Must enter an email"

        elif not EMAIL_REGEX.match(formInfo['edit_email']):
            errors['correctPatternEmailRequired'] = "Your email needs to be in proper format"

        if len(email_already_taken) > 0:
            errors['taken_email'] = "This email has already been used for another User, please select another email to update"

        return errors


class QuoteManager(models.Manager):
    def addQuote_validator(self, formInfo):
        errors = {}

        if len(formInfo['quote_author']) < 3:
            errors['mustHaveAuthor'] = "Your Author needs at least 3 Characters"

        if len(formInfo['quote_content']) < 10:
            errors['content_less_10'] = "The book's descriptions must be at least 5 characters long"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    # liked_quotes = a list of quotes a given user likes
    # quotes_uploaded = a list of books uploaded by a given user

    def __str__(self):
        return f"<User object: {self.first_name} ({self.id})> "


class Quote(models.Model):
    author = models.CharField(max_length=255, null=True)
    content = models.CharField(max_length=255)
    posted_by = models.ForeignKey(
        User, related_name="quotes_uploaded", on_delete=models.CASCADE)
    likers = models.ManyToManyField(User, related_name="liked_quotes")
    objects = QuoteManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
