import os
import tempfile
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from deepface import DeepFace
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

@csrf_exempt
def face_recognition(request):
    print("Request received")

    try:
        # Read the image files into BytesIO objects
        original_img_io = BytesIO(request.FILES['original_pic'].read())
        current_img_io = BytesIO(request.FILES['current_pic'].read())

        # Reset the file pointer to the beginning
        original_img_io.seek(0)
        current_img_io.seek(0)
    except KeyError:
        return HttpResponseBadRequest("Invalid input. Both 'original_pic' and 'current_pic' are required.")
    except Exception as e:
        return HttpResponseBadRequest(f"Error reading image data: {str(e)}")

    print("Processing images")
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_original, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_current:
            print("Temporary files created")

            # Save images to temporary files
            temp_original.write(original_img_io.read())
            temp_current.write(current_img_io.read())

            # Log the file paths
            print(f"Original image path: {temp_original.name}")
            print(f"Current image path: {temp_current.name}")

            # Close the files to ensure data is written
            # temp_original.flush()
            # temp_current.flush()

        # Check if files exist
        if not os.path.exists(temp_original.name) or not os.path.exists(temp_current.name):
            print("Temporary files do not exist.")
            return HttpResponseBadRequest("Error creating temporary files.")

        # Perform the verification with DeepFace
        try:
            result = DeepFace.verify(
                temp_original.name, #/var/folders/pp/89v1_1616v9gdvcfvfxc2z680000gn/T/tmpe4o67se5.jpg
                temp_current.name #/var/folders/pp/89v1_1616v9gdvcfvfxc2z680000gn/T/tmp9rjrtlo3.jpg
            )

            # Close the BytesIO objects
            # original_img_io.close()
            # current_img_io.close()

            print("Verification completed")
            print(result)
            return JsonResponse(result)
        except Exception as e:
            print(f"Error during DeepFace verification: {str(e)}")
            return HttpResponseBadRequest(f"Error during verification: {str(e)}")

    except Exception as e:
        return HttpResponseBadRequest(f"Error processing images: {str(e)}")