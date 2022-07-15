from django.shortcuts import render
from inspector.models import Terceros, Profile
from ordenacion.models import Contrato, Contra1, Vendedores
from .models import Rsmusic, Generos
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import RadicaEncForm, RadicaDetalleForm, DetalleMovimientosFormSet, RsmusicForm
from datetime import date
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View
import mutagen
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
# Create your views here.

class RsmusicList(LoginRequiredMixin, TemplateView):
    login_url = 'generales:login'
    model=Rsmusic
    template_name="radio/rsmusic_list.html"
    context_object_name="rsmusic" 
    def get_context_data(self, **kwargs):
        hoy = date.today()
        mes_actual = hoy.month
        ano_actual = hoy.year
        context = super().get_context_data(**kwargs)
        lista = Rsmusic.objects.filter(sede=self.request.user.profile.sede).order_by('nombre')
        context['rsmusic'] = lista
        context['sede'] = self.request.user.profile.sede

        return context

class RsmusicNew(LoginRequiredMixin, generic.CreateView):
    permission_required = 'Rsmusic.add_rsmusic'
    model = Rsmusic
    login_url = 'generales:login'
    template_name = 'radio/rsmusic_new.html'
    form_class = RsmusicForm
    success_url = reverse_lazy('radio:rsmusic_list')

    def get(self, request, *args, **kwargs):

        ctx = {
            'nombre': ' ',
            'interprete': ' ',
            'autor': ' ',
            'ano': ' ',
            'likes': ' ',
            'genero': ' ',
            'arc_audio': ''
        }

        self.object = None
        form = RsmusicForm(initial=ctx)

        return self.render_to_response( 
            self.get_context_data(
                form=form,
                sede=self.request.user.profile.sede
            )
        )

    def post(self, request, *args, **kwargs):
        form = RsmusicForm(request.POST, request.FILES)
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        print(form.errors)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", form.cleaned_data["arc_audio"])
        self.object = form.save(commit=False)
        self.object.sede = self.request.user.profile.sede
        hours, mins, seconds, ms = open_audio(self.object.arc_audio)
        self.object.tiempo = '{}:{}:{}'.format(hours, mins, seconds)
        self.object.tiempo_ms = int(ms)
        self.object = form.save()
    
        return HttpResponseRedirect(reverse_lazy("radio:rsmusic_list"))

    def form_invalid(self, form):
        self.object=form
        return self.render_to_response(
            self.get_context_data(
                form=form,
                sede=self.request.user.profile.sede
            )
        )

class RadicarList(LoginRequiredMixin, TemplateView):
    login_url = 'generales:login'
    model=Contrato
    template_name="radio/lista_radicaciones.html"
    context_object_name="radicaciones" 
    def get_context_data(self, **kwargs):
        hoy = date.today()
        mes_actual = hoy.month
        ano_actual = hoy.year
        context = super().get_context_data(**kwargs)
        lista = Contrato.objects.filter(sede=self.request.user.profile.sede).order_by('-id').values('id','fecha',\
            'idagencia__rzn_social','producto','no_publicidad','asesor_comercial',\
                'fecha_inicio','fecha_final','presupuesto_cliente','valor_bruto',\
                    'porc_descuento','valor_neto','orden_provicional','sede',\
                        'nit_cliente__nit','nit_cliente__rzn_social','nit_anunciante__rzn_social','usuario')[:500]
        context['radicaciones'] = lista
        context['sede'] = self.request.user.profile.sede

        return context

class RadicaForm(LoginRequiredMixin, generic.CreateView):
    permission_required = 'Contrato.add_contrato'
    model = Contrato
    login_url = 'generales:login'
    template_name = 'radio/radio_radica_form.html'
    form_class = RadicaEncForm
    success_url = reverse_lazy('radio:lista_radicaciones')

    def get(self, request, *args, **kwargs):

        ctx = {
            'no_publicidad': '',
            'nit_cliente': '',
            'nit_anunciante': '',
            'idagencia': '',
            'producto': '',
            'asesor_comercial': '',
            'fecha_inicio': datetime.today() + timedelta(days=(1)),
            'fecha_final': datetime.today() + timedelta(days=(1)),
            'presupuesto_cliente': '', 
            'valor_bruto': '',
            'porc_descuento': 0,
            'valor_neto': '',
            'orden_provicional': False
            }

        self.object = None
        form = RadicaEncForm(initial=ctx)

        return self.render_to_response( 
            self.get_context_data(
                form=form,
                sede=self.request.user.profile.sede
            )
        )


    def post(self, request, *args, **kwargs):
        form =RadicaEncForm(request.POST)
        #print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        #print(form.errors)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario = self.request.user
        self.object.sede = self.request.user.profile.sede
        self.object = form.save()
    
        return HttpResponseRedirect(reverse_lazy("radio:radicaciones"))

    def form_invalid(self, form):
        self.object=form
        return self.render_to_response(
            self.get_context_data(
                form=form,
                sede=self.request.user.profile.sede
            )
        )

class RadicarEdit(LoginRequiredMixin, generic.UpdateView):
    permission_required='ordenacion.change_contrato'
    model=Contrato
    template_name="radio/radio_radica_form.html"
    context_object_name='orden'
    form_class=RadicaEncForm
    success_url=reverse_lazy("radio:lista_radicaciones")
    success_message='Radicacion modificada satisfactoriamente'

    def post(self, request, *args, **kwargs):
        contrato = Contrato.objects.get(id=kwargs["pk"])
        form = RadicaEncForm(request.POST, instance=contrato)

        if form.is_valid():
            post = form.save(commit=False)
            post.usuario = self.request.user
            post.sede = self.request.user.profile.sede
            post.save()
            return HttpResponseRedirect(self.success_url)

def get_ajaxVendedor(request, *args, **kwargs):
    query = request.GET.get('q', None)
    if query: 
        vendedor = Vendedores.objects.filter(nombre_vendedor__icontains=query).values("id","nombre_vendedor") 
        vendedor = list(vendedor)
        return JsonResponse(vendedor, safe=False) 
    else: 
        return JsonResponse(data={'success': False, 'errors': 'No encuentro resultados.'})

def get_ajaxGenero(request, *args, **kwargs):
    query = request.GET.get('q', None)
    if query: 
        generor = Generos.objects.filter(nombre__icontains=query).values("id","nombre") 
        generor = list(generor)
        return JsonResponse(generor, safe=False) 
    else: 
        return JsonResponse(data={'success': False, 'errors': 'No encuentro resultados.'}) 

def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
  
    return hours, mins, seconds  # returns the duration
  
def open_audio(arc_audio):
    # Create a WAVE object
    # Specify the directory address of your wavpack file
    # "alarm.wav" is the name of the audiofile
    audio = MP3(arc_audio)
    
    # contains all the metadata about the wavpack file
    audio_info = audio.info
    length = int(audio_info.length)
    hours, mins, seconds = audio_duration(length)
    #print('Total Duration: {}:{}:{}'.format(hours, mins, seconds))
    return hours, mins, seconds, length