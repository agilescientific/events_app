from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from markdownx.utils import markdownify
import stripe
from django.contrib.auth import get_user_model
from .models import Payment, Amount
from events.models import Event, EventRegistration

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

class PayView(LoginRequiredMixin, TemplateView):
    template_name = 'payhome.html'

    def get(self, request, *args, **kwargs):
        ev = Event.objects.get(slug = self.kwargs['slug'])
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = ev.id))
        if q_reg > 0:
            return HttpResponseRedirect('/event/{}'.format(ev.slug))
        else:
            return super(PayView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        context['custom'] = 'Event registration'
        context['charges'] = Amount.objects.get(event = context['event'])
        context['html_body'] = markdownify(context['charges'].long_description)
        return context

class ChargeView(LoginRequiredMixin, TemplateView):
    template_name = 'charge.html'

    def post(self, request, slug):
        ev = Event.objects.get(slug = self.kwargs['slug'])
        am = Amount.objects.get(event = ev)
        if request.method == 'POST':
            charge = stripe.Charge.create(
                amount=int(am.amount*100),
                currency=str(am.currency).lower(),
                description=am.description,
                source=request.POST['stripeToken']
            )
            print(charge)
            if charge["status"] == "succeeded":
                c, created = Payment.objects.get_or_create(user = self.request.user,
                                                event = ev)
                c.amount = am
                c.stripe_id = request.POST['stripeToken']
                c.save()

                e, created = EventRegistration.objects.get_or_create(
                        event = ev,
                        member = User.objects.get(id=self.request.user.id),
                        )
                e.payment = c
                e.save()
            else:
                return HttpResponseRedirect('/event/{}/charge-error'.format(ev.slug))
        return HttpResponseRedirect('/event/{}/charge'.format(ev.slug))

    def get(self, request, *args, **kwargs):
        ev = Event.objects.get(slug = self.kwargs['slug'])
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = ev.id))
        if q_reg > 0:
            return super(ChargeView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/event/{}'.format(ev.slug))

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        context['custom'] = 'Event registration'
        return context

class ChargeErrorView(LoginRequiredMixin, TemplateView):
    template_name = 'charge_error.html'


    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        context['custom'] = 'Event registration'
        context['html_body'] = "There was an error with the transaction"
        return context