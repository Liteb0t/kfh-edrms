from home.models import Document
from django.utils import timezone


def clean_documents():
    print("Cleaning documents...")
    for document in Document.objects.all():
        # print(timezone.now())
        # print(document.delete_at)
        if timezone.now() > document.delete_at:
            print("Deleting {}".format(document.title))
            document.delete()
