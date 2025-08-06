from django.db import models
from django.contrib.auth.models import AbstractUser


class Society(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    registration_num = models.CharField(max_length=100, unique=True, blank=True, null=True)
   
    
    def __str__(self):
        return self.name
    

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        RESIDENT = "RESIDENT", "Resident"
        SECURITY = "SECURITY", "Security"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.RESIDENT)
    society = models.ForeignKey(Society, on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.email



class Unit(models.Model):
    class UnitType(models.TextChoices):
        ONE_BHK = "1BHK", "1BHK"
        TWO_BHK = "2BHK", "2BHK"
        THREE_BHK = "3BHK", "3BHK"
    

    unit_type = models.CharField(max_length=20, choices=UnitType.choices)
    unit_number = models.CharField(max_length=100)
    building_name = models.CharField(max_length=200, default="Main")
    society = models.ForeignKey(Society, on_delete=models.CASCADE) 
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_units')
    residents = models.ManyToManyField(User, related_name='residing_in', blank=True)
    
    def __str__(self):
        return f"{self.building_name} - {self.unit_number} ({self.society.name})"

    class Meta:
        # Ensures that a unit number is unique within its building and society
        unique_together = ('society', 'building_name', 'unit_number')
     
     
     
        
class Notice(models.Model):
    """Represents an announcement or notice for a society."""
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, help_text="The user who posted the notice")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, help_text="Only published notices will be visible to residents.")
    notice_image = models.ImageField(upload_to='noticeboard_images/', default='noticeboard_images/defaultphoto.jpg', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        # Order notices by the most recent first
        ordering = ['-created_at']
    
    
    
        
class Complaint(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        
        
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)
    
    
    #user who created the complaint
    raised_by =models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    
    #time stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.title} - ({self.get_status_display()})"
    
    class Meta:
        ordering = ['-created_at']
        
        
class Visitor(models.Model):
    class StatusChoices(models.TextChoices):
        EXPECTED = "EXPECTED", "Expected"
        ARRIVED = "ARRIVED", "Arrived"
        DEPARTED = "DEPARTED", "Departed"

    # visitor details
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True)
    
    # Visit details
    visiting_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visitors")
    expected_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.EXPECTED)

    # Timestamps for security to update
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} (visiting {self.visiting_for.get_full_name()})"

    class Meta:
        ordering = ['-expected_datetime']
        
        
# for community talks...    
class Post(models.Model):
    """representa post on the community feed."""
    content = models.TextField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)


    def __str__(self):
        return f"Post by {self.author.get_full_name()} on {self.created_at.strftime('%d %b %Y')}"

    class Meta:
        ordering = ['-created_at'] # shiow the newest posts fisrt
        
        

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # show oldest comments first

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
        
        
    
    
