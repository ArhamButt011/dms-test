from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    ext = value.name.split('.')[-1]  # Get the file extension
    if ext not in ['svg', 'png', 'jpg', 'jpeg']:
        raise ValidationError('Unsupported file extension. Allowed extensions are: .svg, .png, .jpg, .jpeg')
# def validate_pdf_file_extension(value):
#     ext = os.path.splitext(value.name)[1]  # Get the file extension
#     valid_extensions = ['.pdf']
#     if not ext.lower() in valid_extensions:
#         raise ValidationError('Unsupported file extension. Only PDF files are allowed.')