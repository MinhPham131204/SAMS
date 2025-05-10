from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
import uuid
from io import BytesIO
from PIL import Image
from ai_model.models import Model


@csrf_exempt
@require_http_methods(['POST'])
def predict(request):
    try:
        # return JsonResponse({'error': "Please use local backend for this features"}, status=400)
        # Kiểm tra xem body request có dữ liệu không
        if not request.body:
            return JsonResponse({'error': 'No image data provided'}, status=400)

        # Đọc ảnh từ body request (binary)
        image_data = BytesIO(request.body)
        image = Image.open(image_data)

        # Chuyển đổi ảnh sang chế độ RGB nếu cần
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Lưu ảnh tạm thời để dự đoán
        image_uuid = str(uuid.uuid4())
        input_image_path = f"{image_uuid}_inp.jpg"
        image.save(input_image_path)

        # Đường dẫn lưu ảnh kết quả
        output_image_path = f"{image_uuid}_out.jpg"

        # Gọi hàm predict từ mô hình
        results = Model.predict(
            image_path=input_image_path,
            save_to_path=output_image_path,
            confidence_threshold=0.5,
        )

        # Đọc ảnh kết quả và trả về dưới dạng HTTP response
        with open(output_image_path, "rb") as f:
            image_data = f.read()

        # Xóa file tạm sau khi xử lý
        os.remove(input_image_path)
        os.remove(output_image_path)

        # Trả về ảnh và dữ liệu bounding box
        response = HttpResponse(image_data, content_type="image/jpeg")
        response['Content-Disposition'] = f'inline; filename="{image_uuid}_out.jpg"'
        response['Bounding-Boxes'] = json.dumps(results) # Trả về dữ liệu box trong header
        response['Access-Control-Expose-Headers'] = 'Bounding-Boxes'  # Expose header Bounding-Boxes
        return response

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)