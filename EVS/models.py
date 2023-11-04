from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Adjust the max_length as needed

    def __str__(self):
        return self.user.username

class Election(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    


    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='candidates/', null=True, blank=True)
    description = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE, default=1)
    date_of_birth = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=100, null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class VoteBlocks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    Block_Hash = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote by {self.user.username} for {self.candidate.name}"
