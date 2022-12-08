import os.path

from django.core.exceptions import ValidationError



def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] #image[0].jpg[1]
    print(ext)
    valid_extensions_list = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions_list:
        raise ValidationError("Unsupported file extension. Allowed extensions: " + str(valid_extensions_list))
