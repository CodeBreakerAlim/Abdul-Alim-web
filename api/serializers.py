from rest_framework import serializers

from .models import ContactMessage, Profile, Project, Service, Skill


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["id"]


class ProjectSerializer(serializers.ModelSerializer):
    # ফ্রন্টএন্ডের ProjectCard যে নামে নেয় (live, github), সেই নামেই পাঠানো হচ্ছে
    live = serializers.CharField(source="live_url", read_only=True)
    github = serializers.CharField(source="github_url", read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "problem", "result", "tags", "live", "github", "image"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "title", "description", "icon"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "percent"]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        extra_kwargs = {
            "name": {"max_length": 100},
            "message": {"max_length": 5000},
        }
