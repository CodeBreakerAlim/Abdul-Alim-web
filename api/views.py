from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import Profile, Project, Service, Skill
from .serializers import (
    ContactMessageSerializer,
    ProfileSerializer,
    ProjectSerializer,
    ServiceSerializer,
    SkillSerializer,
)


class ProjectList(generics.ListAPIView):
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectSerializer


class ServiceList(generics.ListAPIView):
    queryset = Service.objects.filter(is_published=True)
    serializer_class = ServiceSerializer


class SkillList(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProfileDetail(APIView):
    def get(self, request):
        profile = Profile.objects.first()
        if profile is None:
            return Response({"detail": "Profile not created yet."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProfileSerializer(profile, context={"request": request}).data)


class ContactCreate(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def create(self, request, *args, **kwargs):
        # লুকানো "website" ঘর: মানুষ এটা দেখে না, স্প্যাম বট পূরণ করে ফেলে
        if request.data.get("website"):
            return Response({"ok": True}, status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msg = serializer.save()

        if settings.CONTACT_NOTIFY_EMAIL:
            send_mail(
                subject=f"New portfolio message from {msg.name}",
                message=f"Name: {msg.name}\nEmail: {msg.email}\n\n{msg.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
                fail_silently=True,  # ইমেইল না গেলেও মেসেজ ডেটাবেজে থাকবে
            )
        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class Health(APIView):
    """হোস্টিং সার্ভিস ঘুম থেকে জাগাতে বা চালু আছে কি না দেখতে।"""

    def get(self, request):
        return Response({"status": "ok"})
