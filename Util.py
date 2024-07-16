
from PIL import Image 
import io, base64

def save_base64_image(image_data, file_path):
      
    # Extract the base64-encoded data from the image_data string
    encoded_data = image_data.replace("data:image/jpeg;base64,", "")

    img = Image.open(io.BytesIO(base64.decodebytes(bytes(encoded_data, "utf-8"))))

    img.save(file_path, dpi=(300, 300), quality=95)
