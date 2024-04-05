from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = value.name.split('.')[-1]  # Get the file extension
    if ext not in ['svg', 'png', 'jpg', 'jpeg']:
        raise ValidationError('Unsupported file extension. Allowed extensions are: .svg, .png, .jpg, .jpeg')
