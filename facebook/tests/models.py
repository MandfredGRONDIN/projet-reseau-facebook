from django.db import models

class JSONImport(models.Model):
    file = models.FileField(upload_to='json_imports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Importé le {self.uploaded_at}"
