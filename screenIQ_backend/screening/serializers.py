from rest_framework import serializers
from .models import Application


class ScreenCandidateSerializer(serializers.Serializer):
    candidate_name = serializers.CharField(max_length=255)

    job_description = serializers.CharField()

    resume = serializers.CharField()

    def validate_job_description(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError(
                "Job description too short"
            )
        return value

    def validate_resume(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError(
                "Resume too short"
            )
        return value


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'