from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import NewsStory
from functools import wraps
import json

import logging

logger = logging.getLogger(__name__)


def login_required_json(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'You must be logged in to perform this action.'}, status=401)
    return _wrapped_view

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Check if the user is already authenticated
        if request.user.is_authenticated:
            return HttpResponse('You are already logged in.')
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Welcome! You have been logged in.', status=200)
        else:
            return HttpResponse('Login failed.', status=401)
    else:
        return HttpResponse('Invalid request.', status=400)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        # Check if the user is authenticated before logging out
        if not request.user.is_authenticated:
            return HttpResponse('You are not logged in.')
        
        logout(request)
        return HttpResponse('Goodbye!', status=200)
    else:
        return HttpResponse('Invalid request.', status=400)
    
@csrf_exempt
def stories_view(request):
    #GET STORY SERVICE
    if request.method == 'GET':
        # Get the query parameters from the request
        story_cat = request.GET.get('story_cat', '*')
        story_region = request.GET.get('story_region', '*')
        story_date = request.GET.get('story_date', '*')

        # Filter the stories based on the provided parameters
        stories = NewsStory.objects.all()
        if story_cat != '*':
            stories = stories.filter(category=story_cat)
        if story_region != '*':
            stories = stories.filter(region=story_region)
        if story_date != '*':
            stories = stories.filter(date__gte=story_date)

        # Serialize the stories to JSON
        story_list = [
            {
                'key': story.id,
                'headline': story.headline,
                'story_cat': story.category,
                'story_region': story.region,
                'author': story.author.name,
                'story_date': story.date.strftime('%Y-%m-%d'),
                'story_details': story.details
            }
            for story in stories
        ]

        return JsonResponse({'stories': story_list}, status=200)
    #POST STORY SERVICE
    elif request.method == 'POST':
        if request.user.is_authenticated:
            # Parse the JSON payload
            data = json.loads(request.body)
            headline = data.get('headline')
            category = data.get('category')
            region = data.get('region')
            details = data.get('details')

            # Create a new NewsStory
            try:
                story = NewsStory.objects.create(
                    headline=headline,
                    category=category,
                    region=region,
                    details=details,
                    author=request.user.author
                )
                return JsonResponse({'message': 'Story created.'}, status=201)
            except Exception as e:
                return HttpResponse(f'Service Unavailable: {str(e)}', status=503)
        else:
            return JsonResponse({'error': 'You must be logged in to perform this action.'}, status=503)
    else:
        return HttpResponse('Invalid request method.', status=503)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_story_view(request, key):
    if request.user.is_authenticated:
        try:
            story = NewsStory.objects.get(pk=key)
            story.delete()
            return JsonResponse({'message': 'Story deleted.'}, status=200)
        except ObjectDoesNotExist:
            return HttpResponse('Story not found.', status=503)
    else:
        return JsonResponse({'error': 'You must be logged in to perform this action.'}, status=503)