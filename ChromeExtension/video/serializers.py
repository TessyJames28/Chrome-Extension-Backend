from rest_framework import serializers
from .models import VideoFile, VideoChunk, VideoTranscription, CompleteVideoURL


class VideoChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoChunk
        fields = ['video', 'chunk_number', 'chunk_path']
        

class VideoTranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTranscription
        fields = ['id', 'video', 'transcription']
        
        
class CompleteVideoURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompleteVideoURL
        fields = ['id', 'title', 'video', 'embedded_url']
        
        
class VideoFileSerializer(serializers.ModelSerializer):
    videochunk_set = VideoChunkSerializer(many=True, read_only=True, source='videochunk_set.all')
    videotranscription_set = VideoTranscriptionSerializer(many=True, read_only=True, source='videotranscription_set.all')
    completevideourl_set = CompleteVideoURLSerializer(many=True, read_only= True, source='completevideourl_set.all')
    class Meta:
        model = VideoFile
        fields = ['id', 'title', 'description', 'videochunk_set', 'videotranscription_set', 'completevideourl_set']
    