from rest_framework import serializers

from .models import Content,Exercise,Announcement

class OutPutExerciseSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField("get_course")

    class Meta:
        model = Exercise
        fields = ("course","title", "file", "text","deadline")

    def get_course(self, exercise):
        
        return exercise.course.title
    


class OutPutAnnouncementSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField("get_course")

    class Meta:
        model = Announcement
        fields = ("course","title", "text")

    def get_course(self, content):
        
        return content.course.title
    

class OutPutContentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField("get_course")

    class Meta:
        model = Content
        fields = ("course","title", "file", "text")

    def get_course(self, content):
        
        return content.course.title