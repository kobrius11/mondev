from django.http import JsonResponse


def sidebar_state(request, state=1):
    request.session['sidebar_state'] = state
    return JsonResponse({'state': state})
