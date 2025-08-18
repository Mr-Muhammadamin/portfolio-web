from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django.utils.text import slugify


class CostumUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'


class AboutMe(models.Model):

    user = models.OneToOneField(CostumUser, on_delete=models.CASCADE)
    about_me = HTMLField(null=True, blank=True,help_text='Write about yourself here')
    image = models.ImageField(upload_to='about_me/image', null=True, blank=True)
    skills = models.ManyToManyField('Skill', blank=True,null=True,help_text='Select your skills')
    my_name = models.CharField(max_length=100,help_text='Your name')
    social_media = models.JSONField(null=True, blank=True,help_text='Add your social media links here e.g {"facebook":"https://www.facebook.com/yourname"}')



    def __str__(self):
        return self.my_name
    
    @property
    def get_two_social_media(self):
        return dict(list(self.social_media.items())[:2])

class Education(models.Model):

    about_me = models.ForeignKey(AboutMe, on_delete=models.CASCADE)
    start_year = models.CharField(max_length=4,help_text='Start year of your education ,e.g 2019')
    end_year = models.CharField(max_length=4,help_text='End year of your education ,e.g 2023')
    degree = models.CharField(max_length=100,help_text='Your degree, e.g Bachelor of Science')
    university = models.CharField(max_length=100,help_text='Your university, e.g University of California')
    description = HTMLField(help_text='Write about your education here')

    def __str__(self):
        return f"{self.degree} at {self.university} ({self.start_year} - {self.end_year})"

class Experience(models.Model):

    about_me = models.ForeignKey(AboutMe, on_delete=models.CASCADE)
    start_year = models.CharField(max_length=4,help_text='Start year of your experience ,e.g 2019')
    end_year = models.CharField(max_length=4,help_text='End year of your experience ,e.g 2023')
    position = models.CharField(max_length=100,help_text='Your position, e.g Software Developer')
    company = models.CharField(max_length=100,help_text='Your company, e.g Google')
    description = HTMLField(help_text='Write about your experience here')

    def __str__(self):
        return f"{self.position} at {self.company} ({self.start_year} - {self.end_year})"

class Skill(models.Model):

    name = models.CharField(max_length=100,help_text='Your skill, e.g Python',unique=True)

    def __str__(self):
        return self.name
    
class Project(models.Model):

    title = models.CharField(max_length=100,help_text='Your project title')
    year = models.CharField(max_length=4,help_text='Year of your project ,e.g 2023')
    client = models.CharField(max_length=100,help_text='Your client, e.g Google')
    service = models.CharField(max_length=100,help_text='Your service, e.g Web Development')
    project_type = models.CharField(max_length=100,help_text='Your project type, e.g Full Stack')
    description = HTMLField(null=True,blank=True,help_text='Write about your project here')
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return F"{self.title} ({self.year})"
    

class ProjectImage(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='project/image',help_text='Uploade your project image')

    def __str__(self):
        return f"Image for {self.project.title}"
    

class YoutubeVideo(models.Model):

    title = models.CharField(max_length=100,help_text='Enter YouYube title')
    link = models.URLField(help_text='Video URL')
    thumbnail = models.ImageField(upload_to='image/youtube_thumbnail',help_text='Youtube video thumbnail')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title