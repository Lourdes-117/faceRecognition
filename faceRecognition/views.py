import tempfile
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from deepface import DeepFace
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

@csrf_exempt
def face_recognition(request):
    print("Request received")

    print(request.FILES)

    original_img = request.FILES.get('original_pic')

    print("Original image received")
    current_img = request.FILES.get('current_pic')

    print("Current image received")
    
    if original_img is None or current_img is None:
        print("Invalid input. Both 'original_pic' and 'current_pic' are required.")
        return HttpResponseBadRequest("Invalid input. Both 'original_pic' and 'current_pic' are required.")
    
    print("Processing images")
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_original, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_current:
            print("Temporary files created")

            print(original_img.size)
            print(current_img.size)
            
            # Save images to temporary files
            temp_original.write(original_img.read())
            temp_current.write(current_img.read())
            
            # Make sure to close the files so DeepFace can read them
            temp_original.close()
            temp_current.close()
            
            # Perform the verification with DeepFace
            result = DeepFace.verify(
                temp_original.name,
                temp_current.name
            )

            print("Verification completed") 
            print(request)

        return JsonResponse(result)

    except Exception as e:
        return HttpResponseBadRequest(f"Error processing images: {str(e)}")