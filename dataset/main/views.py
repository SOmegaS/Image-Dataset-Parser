import json

import threading

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import parser

@csrf_exempt
def rendering(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        classes = body.get("class")
        count = body.get("count")
        print(classes)
        print(count)
        parser.main(100,  dict(zip(classes, map(int, count))))
    return render(request, 'main/index.html')
