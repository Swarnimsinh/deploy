from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meetings'
    )

    meeting_date = models.DateField()
    meeting_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.meeting_date}"
    
# ///////////////////    Commerce     //////////////////////////

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User

class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default='Pending'
    )
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()
    
#  //////////////////   Content   //////////////////////////

class Title(models.Model):
    heading = models.CharField(max_length=200)
    sub_heading = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    
    def __str__(self):
        return self.heading
    
class Service(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.ImageField(upload_to="image/")
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    quote = models.TextField()
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    metric = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    def __str__(self):
        return self.name
       
class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/') 
    
    def __str__(self):
        return self.title
       
class Video(models.Model):
    title = models.CharField(max_length=100)
    youtube_url = models.URLField()
    
    def __str__(self):
        return self.title

class WebsiteSettings(models.Model):
    video1 = models.CharField(max_length=500, default='https://www.youtube.com/embed/dQw4w9WgXcQ')
    video2 = models.CharField(max_length=500, default='https://www.youtube.com/embed/ypy4m_L680A')
    video3 = models.CharField(max_length=500, default='https://www.youtube.com/embed/EngW7tLk6r8')
    showHeroTexts = models.BooleanField(default=True)
    
    phase1Label = models.CharField(max_length=200, default='PHASE 01 // INTERVIEW ARCHITECTURE')
    phase1Title = models.CharField(max_length=200, default='We Extract Your Core Narrative')
    phase1Desc = models.TextField(default='Our production team conducts targeted, high-fidelity conversational mappings to gather raw authority assets.')
    
    phase2Label = models.CharField(max_length=200, default='PHASE 02 // RETENTION ASSEMBLY')
    phase2Title = models.CharField(max_length=200, default='Applying High-Performance Cuts')
    phase2Desc = models.TextField(default='Refining auditory beats, adding volt structural graphics, and formatting hooks to capture organic feeds.')
    
    phase3Label = models.CharField(max_length=200, default='PHASE 03 // FULL-SCALE EXPANSION')
    phase3Title = models.CharField(max_length=200, default='The Absolute Distribution Cadence')
    phase3Desc = models.TextField(default='Your brand claims real estate on TikTok, Reels, Shorts, and LinkedIn simultaneously. Scroll down to deploy your engine.')
    
    heroSubtitle = models.TextField(default='', blank=True)
    testimonialSubtitle = models.CharField(max_length=200, default='PARTNER REVIEWS')
    testimonialTitle = models.CharField(max_length=200, default='PROVEN SYSTEM REPUTATION')
    testimonialDescription = models.TextField(default='Discover observations from leaders who scale their presence using our systematic workflows.')
    bookingTitle = models.CharField(max_length=200, default='ALIGN THE FLUID PROCESS')
    bookingSubtitle = models.TextField(default='Book a diagnostic call to map your distribution framework inline instantly.')

    def __str__(self):
        return "Website CMS Settings"