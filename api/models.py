from django.core.validators import MaxValueValidator
from django.db import models


class Profile(models.Model):
    """আপনার নিজের তথ্য। শুধু একটা রেকর্ড থাকবে।"""

    full_name = models.CharField(max_length=100, default="Md. Abdul Alim")
    headline = models.CharField(max_length=200, default="Full-stack Web Developer")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="profile/", blank=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, help_text="PDF ফাইল আপলোড করুন")

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(
        max_length=30, blank=True, help_text="দেশের কোডসহ, + ছাড়া। যেমন 8801XXXXXXXXX"
    )
    location = models.CharField(max_length=100, blank=True)

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)

    years_experience = models.PositiveSmallIntegerField(default=0)
    projects_done = models.PositiveSmallIntegerField(default=0)
    happy_clients = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.pk = 1  # সবসময় একটাই রেকর্ড
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Project(models.Model):
    title = models.CharField(max_length=120)
    problem = models.TextField(help_text="ক্লায়েন্টের সমস্যাটা কী ছিল")
    result = models.TextField(help_text="আপনি কী সমাধান দিলেন, ফলাফল কী")
    tags = models.CharField(max_length=200, help_text="কমা দিয়ে লিখুন। যেমন: React, Django, Tailwind")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True)
    order = models.PositiveIntegerField(default=0, help_text="ছোট সংখ্যা আগে দেখাবে")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title


class Service(models.Model):
    ICON_CHOICES = [
        ("monitor", "Monitor (website)"),
        ("shopping-cart", "Shopping cart (e-commerce)"),
        ("server", "Server (backend/API)"),
        ("upload-cloud", "Upload cloud (deployment)"),
        ("code", "Code"),
        ("smartphone", "Smartphone (mobile)"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default="code")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=60)
    percent = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
