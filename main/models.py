from django.db import models

class LeafModel(models.Model):
    ALPHONSO = 'alphonso'
    AMRAPALI = 'amrapali'
    CHAUNSA = 'chaunsa'
    DUSHERI = 'dusheri'
    LANGRA = 'langra'

    VARIETY_CHOICES = [
        (ALPHONSO, 'Alphonso'),
        (AMRAPALI, 'Amrapali'),
        (CHAUNSA, 'Chaunsa'),
        (DUSHERI, 'Dusheri'),
        (LANGRA, 'Langra'),
    ]

    # Model Fields
    original_image = models.TextField(default='')
    is_preprocessed = models.BooleanField(default=False)
    preprocessed_image = models.TextField(default='')
    aspect_ratio = models.FloatField(default=0.0)
    rectangularity = models.FloatField(default=0.0)
    perimeter_ratio = models.FloatField(default=0.0)
    compactness = models.FloatField(default=0.0)
    mean_color = models.CharField(max_length=7, default='#000000')
    vein_area_2_ratio = models.FloatField(default=0.0)
    vein_area_4_ratio = models.FloatField(default=0.0)
    elongation = models.FloatField(default=0.0)
    variety = models.TextField(choices=VARIETY_CHOICES)


    def __str__(self):
        return self.original_image