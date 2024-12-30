import tempfile
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from deepface import DeepFace
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

@csrf_exempt
def face_recognition(request):
    print("Request received")

    try:
        original_img = BytesIO(request.FILES['original_pic'].read())
        current_img = BytesIO(request.FILES['current_pic'].read())
    except KeyError:
        return HttpResponseBadRequest("Invalid input. Both 'original_pic' and 'current_pic' are required.")
    except Exception as e:
        return HttpResponseBadRequest(f"Error reading image data: {str(e)}")

    print("Processing images")
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=True, suffix=".jpg") as temp_original, \
             tempfile.NamedTemporaryFile(delete=True, suffix=".jpg") as temp_current:
            print("Temporary files created")

            print(original_img.size)
            print(current_img.size)
            
            # Save images to temporary files
            temp_original.write(original_img.getvalue())
            temp_current.write(current_img.getvalue())
            
            # Perform the verification with DeepFace
            result = DeepFace.verify(
                temp_original.name,
                temp_current.name
            )

            # Make sure to close the files so DeepFace can read them
            temp_original.close()
            temp_current.close()

            print("Verification completed") 
            print(request)

        return JsonResponse(result)

    except Exception as e:
        return HttpResponseBadRequest(f"Error processing images: {str(e)}")