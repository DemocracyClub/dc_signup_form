import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Token, SignupQueue


@csrf_exempt
def email_signup(request):

    # authorize
    if 'HTTP_AUTHORIZATION' not in request.META:
        return HttpResponse(status=403)
    try:
        auth = Token.objects.get(token=request.META['HTTP_AUTHORIZATION'])
    except Token.DoesNotExist:
        return HttpResponse(status=403)

    # save
    body = json.loads(request.body.decode('utf-8'))
    record = SignupQueue(
        email=body['data']['email'],
        data=body['data'],
        mailing_lists=body['mailing_lists']
    )
    record.save()

    return HttpResponse(status=201)
