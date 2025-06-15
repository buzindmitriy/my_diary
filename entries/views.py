from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Entry, Tag
from .forms import EntryForm

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'entries/entry_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        tag_slug = self.request.GET.get('tag')

        qs = Entry.objects.filter(author=self.request.user)

        if tag_slug:
            try:
                tag = Tag.objects.get(slug=tag_slug)
                qs = qs.filter(tags=tag)
            except Tag.DoesNotExist:
                qs = Entry.objects.none()

        if query:
            qs = qs.filter(title__icontains=query) | qs.filter(content__icontains=query)

        return qs.distinct().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['current_tag'] = self.request.GET.get('tag', '')
        context['query'] = self.request.GET.get('q', '')
        return context

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'

    def get(self, request, *args, **kwargs):
        entry = self.get_object()
        if entry.author != request.user and not request.user.is_superuser:
            raise PermissionDenied("Вы не можете просматривать чужие записи")
        return super().get(request, *args, **kwargs)

class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('entry_list')

class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    template_name = 'entries/entry_form.html'
    fields = ['title', 'content', 'tags', 'image', 'is_private']
    success_url = reverse_lazy('entry_list')

    def test_func(self):
        entry = self.get_object()
        return entry.author == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав редактировать эту запись")


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'entries/entry_delete.html'
    success_url = reverse_lazy('entry_list')

    def test_func(self):
        entry = self.get_object()
        return entry.author == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав удалить эту запись")
