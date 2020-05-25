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

    image_file = models.TextField()
    variety = models.TextField(choices=VARIETY_CHOICES)


    def __str__(self):
        return "Variety=" + self.variety + " and File=" + self.image_file