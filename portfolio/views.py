from django.shortcuts import render
import requests
from django.http import Http404
from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView,TemplateView
from django.views import View
from portfolio.models import AboutMe,Experience,Education,Project,YoutubeVideo
from portfolios import settings
from django.contrib import messages

def index(request):
    videos = YoutubeVideo.objects.order_by('create_at')[:3]
    about_me = AboutMe.objects.select_related('user').first()
    context = {
        'videos': videos,
        'about_me': about_me,
    }
    return render(request, 'index.html', context)



# class Homepage(View):
#     def get(self, request, id):
#         blog = AboutMe.objects.get(id=id)
#         return render(request, 'home.html')
    
#     def post(self, request):
#         return redirect(request, 'home.html')



class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_me = AboutMe.objects.select_related('user').first()
        context['about_me'] = about_me
        context['experiences'] = Experience.objects.filter(about_me=context['about_me'])
        context['educations'] = Education.objects.filter(about_me=context['about_me'])
        context['social_media'] = about_me.social_media if about_me else {}
        return context

class CredentialsView(TemplateView):
    template_name = 'credentials.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        about_me = AboutMe.objects.select_related('user').first()

        context['about_me'] = about_me
        context['experiences'] = Experience.objects.filter(about_me=about_me) if about_me else []
        context['educations'] = Education.objects.filter(about_me=about_me) if about_me else []
        context['social_media'] = about_me.social_media if about_me else {}
        context['skills'] = about_me.skills.all() if about_me else []
        return context


class WorksView(ListView):
    model = Project
    template_name = 'works.html'
    context_object_name = 'projects'


    def get_queryset(self):
        return Project.objects.prefetch_related('images').order_by('year')


class WorkDetailView(DetailView):
    model = Project
    template_name = 'work-details.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.prefetch_related('images').order_by('year')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        try:
            return Project.objects.prefetch_related('images').get(slug=slug)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")


class ContactView(View):
    def get(self, request):
        context = {}
        about_me = AboutMe.objects.select_related('user').first()

        if about_me and about_me.social_media:
            social_media_dict = about_me.social_media  # JSONField, Python dict
            # dictni listga aylantiramiz va faqat 2 ta elementini olamiz
            social_media_items = list(social_media_dict.items())[:2]
            context['social_media'] = social_media_items
        else:
            context['social_media'] = []
        return render(request, 'contact.html', context)

    def post(self, request):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')


        bot_token = settings.BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        telegram_message = f"**New Contact Message**\n\nName: {full_name}\nEmail: {email}\nMessage: {message_content}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": telegram_message,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            messages.success(request, "Your message has been sent successfully.")
        else:
            messages.error(request, "Failed to send your message. Please try again later.")

        return redirect('/')
    
class YoutubeVideoListView(View):
    
    def get(self, request):
        videos = YoutubeVideo.objects.order_by('create_at')
        context = {
            'videos': videos
        }

        return render(request, 'service.html', context)

# class YoutubeVideoDetailView(DetailView):
#     model = YoutubeVideo
#     template_name = "service.html"
#     context_object_name = "video"
