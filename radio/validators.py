from django.core.exceptions import ValidationError
 
def valid_extension(value):
    if (not value.name.endswith('.mp3') and
        not value.name.endswith('.wav') and 
        not value.name.endswith('.occ')):
 
        raise ValidationError("Archivos permitidos: .mp3, .wav, .occ")
