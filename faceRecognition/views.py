import json
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from deepface import DeepFace
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def face_recognition(request):
    # Ensure the request method is POST
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method. Only POST is allowed.")
    
    try:
        # Parse the JSON data from the request body
        # body_unicode = request.body.decode('utf-8')
        data = json.loads(request.body)

        # Extract the variables
        original_img = data.get('original_img')
        current_img = data.get('current_img')
        if original_img is None or current_img is None:
            return HttpResponseBadRequest("Invalid input. Both 'original_img' and 'current_img' are required.")

        # Check if both variables are present and are strings
        if isinstance(original_img, str) and isinstance(current_img, str):
            # Process the images or perform some operation
            # For now, we just return the values in the response

            result = DeepFace.verify(original_img, current_img)
            return JsonResponse(result)

        else:
            return HttpResponseBadRequest("Invalid input. Both 'original_img' and 'current_img' should be strings.")

    except:
        return HttpResponseBadRequest("Invalid JSON format.")