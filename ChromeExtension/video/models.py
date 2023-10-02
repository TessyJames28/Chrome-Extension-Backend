from django.db import models

# Create your models here.
class VideoFile(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self. title
    
    
class VideoChunk(models.Model):
    video = models.ForeignKey(VideoFile, on_delete=models.CASCADE)
    chunk_number = models.PositiveIntegerField()
    chunk_path = models.CharField(max_length=255)
    
    def __str__(self):
        return f"chunk number: {self.chunk_number} and path: {self.chunk_path}"
    
    
class VideoTranscription(models.Model):
    video = models.ForeignKey(VideoFile, on_delete=models.PROTECT)
    transcription = models.TextField()
    description = models.TextField()
    
    def __str__(self):
        return f"The video transcription for {self.video.title}"


class CompleteVideoURL(models.Model):
    video = models.ForeignKey(VideoFile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    embedded_url = models.URLField(max_length=255)
    
    def __str__(self):
        return self.title
