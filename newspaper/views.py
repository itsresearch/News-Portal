from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from newspaper.models import Post, Advertisement, Category, Tag, Contact
from django.views.generic import ListView, DetailView, View, CreateView, TemplateView
from django.utils import timezone
from datetime import timedelta
from newspaper.forms import CommentForm, ContactForm, NewsLetterForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger


# Create your views here.
class SidebarMixin:
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        context["popular_posts"]=Post.objects.filter(
            published_at__isnull=False, status="active").order_by("-published_at")[:5]
        
        context["advertisement"]=Advertisement.objects.all().order_by("-created_at").first()

        return context
    
class HomeView(SidebarMixin, ListView):
    model=Post
    template_name="newsportal/home.html"
    context_object_name="posts"
    queryset=Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:4]

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["featured_post"]=(
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )

        one_week_ago=timezone.now()-timedelta(days=7)
        context["weekly_top_posts"]=Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-views_count")[:5]

        return context

class PostListView(SidebarMixin, ListView):
    model=Post
    template_name="newsportal/list/list.html"
    context_object_name="posts"
    paginate_by=1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active").order_by("-published_at")
    
    
class PostDetailView(SidebarMixin, DetailView):
    model=Post
    template_name="newsportal/detail/detail.html"
    context_object_name="post"

    def get_queryset(self):
        query=super().get_queryset()
        query=query.filter(published_at__isnull=False, status="active")
        return query
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        current_post = self.object
        current_post.views_count += 1
        current_post.save()

        context["related_posts"]=Post.objects.filter(
            published_at__isnull=False, status="active", category=self.object.category
        ).order_by("-published_at","-views_count")[:2]
        return context

class CommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get("post")
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("post-detail", pk=post_id)
        else:
            post = Post.objects.get(pk=post_id)
            popular_posts = Post.objects.filter(
                published_at__isnull=False, status="active"
            ).order_by("-published_at")[:5]
            advertisement = Advertisement.objects.order_by("-created_at").first()

            return render(request, "newsportal/detail/detail.html", {
                "post": post,
                "form": form,
                "popular_posts": popular_posts,
                "advertisment": advertisement
            })
        
class PostByCategoryView(SidebarMixin, ListView):
    model=Post
    template_name="newsportal/list/list.html"
    context_object_name="posts"
    paginate_by=1

    def get_queryset(self):
        query=super().get_queryset()
        query=query.filter(
            published_at__isnull=False, status="active", category__id=self.kwargs.get("category_id")
        ).order_by("-published_at")
        return query
    
class CategoryListView(ListView):
    model=Category
    template_name="newsportal/categories.html"
    context_object_name="categories"

class TagListView(ListView):
    model= Tag
    template_name="newsportal/tag.html"
    context_object_name="tags"

class PostByTagView(SidebarMixin, ListView):
    model=Post
    template_name="newsportal/list/list.html"
    context_object_name="posts"
    paginate_by=1

    def get_queryset(self):
        query=super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        query=query.filter(
            published_at__isnull=False, status="active", tag__id=tag_id
        ).order_by("-published_at")
        return query
    
class ContactView(SuccessMessageMixin, CreateView):
    model=Contact
    template_name="newsportal/contact.html"
    form_class=ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"

class AboutView(SidebarMixin, TemplateView):
    template_name = "newsportal/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).count()
        context["total_categories"] = Category.objects.count()
        context["latest_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:3]
        return context

class NewsLetterView(View):
    def post(self, request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax=="XMLHttpRequest":
            form= NewsLetterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                "success": True,
                "message": "You have successfully subscribed to the newsletter.",
            } ,
            status=201,
                )
            else:
                return JsonResponse({
                "success": False,
                "message": "Cannot subscribe to the newsletter.",
            }, 
            status=400)
        else:
            return JsonResponse(
                {
                "success": False,
                "message": "Cannot process. Must be an AJAX XMLHttpRequest.",
                },
                status=400
            )

class PostSearchView(View):
    template_name="newsportal/list/list.html" 
    
    def get(self, request, *args, **kwargs):
        query=request.GET.get("query", "").strip()
        if not query:
            return redirect("post-list")
        post_list=Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query)) & Q(status="active") 
            & Q(published_at__isnull=False)
        ).order_by("-published_at")

        page=request.GET.get("page",1)
        paginate_by=1
        paginator=Paginator(post_list, paginate_by)
        try:
            posts=paginator.page(page)
        except PageNotAnInteger:
            posts=paginator.page(1)

        popular_posts=Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]
        advertisement=Advertisement.objects.all().order_by("-created_at").first()
        
        return render(
            request,
            self.template_name,
            {
                "page_obj": posts,
                "query": query,
                "popular_posts": popular_posts,
                "advertisement": advertisement,
            },
        )
    
