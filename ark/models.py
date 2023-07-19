import uuid
import os
import hashlib

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import models

class Naan(models.Model):
    naan = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.naan}"


class User(AbstractUser):
    naan = models.ForeignKey(Naan, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.username


class Key(models.Model):
    key = models.CharField(max_length=4096, primary_key=True)

    @classmethod
    def generate_api_key(cls, naan_id):
        try:
            naan_instance = Naan.objects.get(naan=naan_id)
        except Naan.DoesNotExist:
            raise ValueError("Naan instance with the provided ID does not exist.")

        api_key = uuid.uuid4()
        key_inst = Key(active=True, naan=naan_instance)
        key_inst.set_password(str(api_key))
        key_inst.save()
        return key_inst, api_key

    def set_password(self, raw_password):
        # Hash the raw password before storing it in the database
        self.key = make_password(raw_password)

    def check_password(self, raw_password):
        # Check if the provided raw password matches the hashed password in the database
        return check_password(raw_password, self.key)

    naan = models.ForeignKey(Naan, on_delete=models.CASCADE)
    active = models.BooleanField()

    def __str__(self):
        return f"Key-{self.naan.naan}-{self.key.hex[:8]}..."


class Shoulder(models.Model):
    shoulder = models.CharField(max_length=50)
    naan = models.ForeignKey(Naan, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.naan.naan}{self.shoulder}"


class Ark(models.Model):
    ark = models.CharField(primary_key=True, max_length=200, editable=False)
    naan = models.ForeignKey(Naan, on_delete=models.DO_NOTHING, editable=False)
    shoulder = models.CharField(max_length=50, editable=False)
    assigned_name = models.CharField(max_length=100, editable=False)
    url = models.URLField(default="", blank=True)
    metadata = models.TextField(default="", blank=True)

    # Frick specific fields here:
    title = models.TextField(default="", blank=True)
    type = models.TextField(default="", blank=True)
    rights = models.TextField(default="", blank=True)
    identifier = models.TextField(default="", blank=True)
    format = models.TextField(default="", blank=True)
    relation = models.TextField(default="", blank=True)
    source = models.TextField(default="", blank=True)

    COLUMN_METADATA = {
        'title': {
            'property': "http://purl.org/dc/elements/1.1/title",
            'type': "xsd:string",
        },
        'type': {
            'property': 'http://purl.org/dc/elements/1.1/type',
            'type': "xsd:string",
        },
        'rights': {
            'property': 'http://purl.org/dc/elements/1.1/rights',
            'type': "xsd:string",
        },
        'identifier': {
            'property': 'http://purl.org/dc/elements/1.1/identifier',
            'type': "xsd:string",
        },
        'format': {
            'property': 'http://purl.org/dc/elements/1.1/format',
            'type': "xsd:string",
        },
        'relation': {
            'property': 'http://purl.org/dc/elements/1.1/relation',
            'type': 'xsd:anyURI'
        },
        'source': {
            'property': 'http://purl.org/dc/elements/1.1/source',
            'type': 'xsd:anyURI'
        },
        'url': {
            'property': 'https://schema.org/url',
            'type': 'xsd:anyURI'
        }
    }

    def clean(self):
        expected_ark = f"{self.naan.naan}{self.shoulder}{self.assigned_name}"
        if self.ark != expected_ark:
            raise ValidationError(f"expected {expected_ark} got {self.ark}")

    def __str__(self):
        return f"ark:/{self.ark}"
