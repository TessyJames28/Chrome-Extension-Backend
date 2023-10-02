from django.shortcuts import render
from rest_framework import status, generics
from .models import VideoFile, VideoChunk, VideoTranscription, CompleteVideoURL
from .serializers import VideoFileSerializer, VideoChunkSerializer, VideoTranscriptionSerializer, CompleteVideoURLSerializer
from rest_framework.response import Response
from moviepy.editor import VideoFileClip, clips_array
from django.conf import settings
import os

# Create your views here.

class VideoPost(generics.ListCreateAPIView):
    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer
    
    def get(self, request):
        video_files = VideoFile.objects.all()
        serializer = self.serializer_class(video_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        video_chun = self.request.FILES.get('video_chunk')
        chunk_number = self.request.POST.get('chunk_number')
        video_id = self.request.POST.get('video_id')
        
        
        if not (video_chunk and chunk_number is not None and video_id):
            return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            video = VideoFile.objects.get(id=video_id)
        except VideoFile.DoesNotExist:
            video, created = VideoFile.objects.create(
            id = video_id,
            title = title,
            description = description
        )
            
        # decode the video
        video_data_decoded = base64.b64decode(video_chunk)
            
                
        # save the video in a video storage and write to the specified path
        chunk_path = f'meddia/chunks/{video.id}_{chunk_number}.mp4'
                
        with open(chunk_path, 'wb') as destination:
            for data in video_chunk.chunks():
                destination.write(video_data_decoded)
                        
        # Create an instance and store on the database
        video_data = VideoChunk(
            video = video,
            chunk_number = chunk_number,
            chunk_path = chunk_path
        )
                
        video_data.save()
                
        return Response({"message": "Video chunk saved successfully"}, status=status.HTTP_201_CREATED)


class VideoChunkView(generics.ListCreateAPIView):
    queryset = VideoChunk.objects.all()
    serializer_class = VideoChunkSerializer


def combine_video_chunk(video_id):
    try:
        video = VideoFile.objects.get(id=video_id)
    except VideoFile.DoesNotExist:
        return None
    
    video_chunks = VideoChunk.objects.filter(video=video).order_by('chunk_number')
    
    if not video_chunks:
        return None
    
    video_clips = [VideoFileClip(chunk.chunk_path) for chunk in video_chunks]
    
    final_video = clips_array([video_clips])
    
    output_path = f"media/assembled_videos/{video.id}.mpp4"
    final_video.write_videofile(output_path, codec="libx264")
    
    embedded_url = f"/media/assembled_videos/{video.id}.mp4"
    
    complete_video_url = CompletedVideoURL(
        video = video,
        title = video.title,
        # complete_video = final_video,
        embedded_url = embedded_url
    )
    
    complete_video_url.save()
    
    #Delete individual chunk files to save space
    for chunk in video_chunks:
        if os.path.exists(chunk.chunk_path):
            os.remove(chunk.chunk_path)
        chunk.delete()
    
    return embedded_url


class AssembleAndRetreieveVideo(generics.RetrieveAPIView):
    queryset = VideoFile.objects.all()
    serializer_class = CompleteVideoURLSerializer
    
    
    def retrieve(self, request, *args, **kwargs):
        video_id = self.kwargs['pk']
        
        # Generate an embedded URL for the complete video
        embedded_url = combine_video_chunk(video_id)
        
        if not embedded_url:
            return Response({"error": "Video assembly failed or not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            complete_video_url = CompletedVideoURL.objects.get(id=video_id)
        except CompletedVideoURL.DoesNotExist:
            return Response({"error": "Complete video URL not found"})
        
        #serialize the compile url and return it
        serializer = self.serializer_class(complete_video_url)
        serrializer.data['embedded_url'] = embedded_url
         
        return Response(serializer.data)
    
    
class CompleteVideo(generics.ListAPIView):
    queryset = CompleteVideoURL.objects.all()
    serializer_class = CompleteVideoURLSerializer