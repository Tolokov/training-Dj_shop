from django.views.generic import FormView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from Interactive.forms import ContactForm, CustomerForm, AddNewAddressDeliveryForm, Delivery, MailForm
from Interactive.models import Customer, Mail
from Interactive.service import send_mail_to_support
from Shop.models import Cart


class ProfileCreate(LoginRequiredMixin, CreateView):
    """Профиль пользователя с возможностью изменения"""
    model = Customer
    success_url = reverse_lazy('profile')
    template_name = 'pages/profile.html'
    form_class = CustomerForm

    def get_context_data(self, *, object_list=None, **kwargs):
        """Заполнение формы уже имеющимися данными о пользователе"""
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        form_class = CustomerForm(instance=customer)
        context['form'] = form_class
        return context

    def post(self, request, *args, **kwargs):
        """Обновление данных о пользователе"""
        customer = self.request.user.customer
        form = CustomerForm(self.request.POST, self.request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('profile'), permanent=True)


class MailView(CreateView):
    model = Mail
    form_class = MailForm
    success_url = "/"


class ContactFormView(FormView):
    template_name = 'pages/contact-us.html'
    form_class = ContactForm
    success_url = '/contact/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CONTACT US'
        context['contact_selected'] = 'active'
        context['social_networking'] = (
            ('fa-facebook', 'https://www.facebook.com'),
            ('fa-twitter', 'https://twitter.com/'),
            ('fa-google-plus', 'https://www.google.com'),
            ('fa-youtube', 'https://www.youtube.com')
        )
        return context

    def form_valid(self, form):
        """Отправление письма на электронную почту организации"""
        send_mail_to_support(form.cleaned_data)
        return super(ContactFormView, self).form_valid(form)


class DeliveryFormView(LoginRequiredMixin, FormView):
    template_name = 'pages/delivery.html'
    form_class = AddNewAddressDeliveryForm
    success_url = '/delivery/'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['addresses'] = Delivery.objects.filter(user=user_id)
        context['cart_items'] = Cart.objects.filter(user=user_id).select_related('product')
        return context

    def form_valid(self, form):
        form.save()
        print(form.cleaned_data)
        return super(DeliveryFormView, self).form_valid(form)


class DeleteDelivery(View):
    def post(self, request, **kwargs):
        delivery = Delivery.objects.get(id=self.request.POST['addr'])
        delivery.delete()
        return redirect(reverse_lazy('delivery'), permanent=True)
