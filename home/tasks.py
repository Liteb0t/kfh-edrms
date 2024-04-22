from home.models import Document
from django.utils import timezone


def clean_documents():
    for document in Document.objects.all():
        if timezone.now() > document.delete_at:
            print("Deleting {}".format(document.title))
            document.delete()
