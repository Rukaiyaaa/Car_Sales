from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from car.models import Car


# Add post using class based view
@method_decorator(login_required, name='dispatch')
class AddCarCreateView(CreateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'add_car.html'
    success_url = reverse_lazy('add_car')
    def form_valid(self, form):
        return super().form_valid(form)



# Editing post using class based view
@method_decorator(login_required, name='dispatch')
class EditCarView(UpdateView):
    model = models.Car
    form_class = forms.CarForm
    template_name = 'add_car.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('homepage')


@login_required
def delete_post(request, id):
    post = models.Post.objects.get(pk=id)
    post.delete()
    return redirect('homepage')


# Deleting post using class based view
@method_decorator(login_required, name='dispatch')
class DeleteCarView(DeleteView):
    model = models.Car
    template_name = 'delete_car.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'


class DetailCarView(DetailView):
    model = models.Car
    pk_url_kwarg = 'id'
    template_name = 'car_details.html'

    
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    

@login_required
def buy_car(request, id):
    car = get_object_or_404(Car, pk=id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        return redirect('detail_car', id=id)
    else:
        return render(request, 'car_detail.html', {'car': car, 'error': 'This car is out of stock'})

    