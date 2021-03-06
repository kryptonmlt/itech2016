from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from game.forms import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from game.models import Account, Alliance
from django.db.models import F
from datetime import datetime, timedelta
import random


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # create account
            a = Account.objects.get_or_create(user=user)[0]
            pic_id = random.randrange(1,5,1)
            a.picture = 'media/portraits/' + str(pic_id) + '.png'
            a.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            return render_to_response(
                'home/index.html',
                {'user_form': user_form, 'errors': user_form.errors},
                context)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render_to_response(
        'home/index.html',
        {'user_form': user_form, 'registered': registered},
        context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/game/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your game account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('home/index.html', {}, context)


def top_stats(request):
    print "loading top stats"

    account_highest_wins = Account.objects.order_by('-wins')[:10]
    account_highest_wins_percentage = Account.objects.order_by((F('wins') / F('defeats')))[:10]
    account_highest_wins_percentage = account_highest_wins_percentage.reverse()
    alliance_score = Alliance.objects.order_by('-all_time_score')[:10]
    context_dict = {'account_highest_wins': account_highest_wins,
                    'account_highest_wins_percentage': account_highest_wins_percentage,
                    'alliance_score': alliance_score}
    print "loaded top stats"
    return render(request, 'home/top_stats.html', context_dict)
