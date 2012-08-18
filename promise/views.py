from django.shortcuts import render_to_response


def home(request):
    template = 'home.html'
    context = {}
    return render_to_response(template, context)
