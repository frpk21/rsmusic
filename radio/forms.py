from django import forms

from django.forms.models import inlineformset_factory

from ordenacion.models import Contrato, Contra1, Agenda, Vendedores

from inspector.models import Terceros
from radio.models import Generos, Rsmusic

from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from ckeditor.widgets import CKEditorWidget

from django.core.exceptions import ValidationError


class RsmusicForm(forms.ModelForm):
    genero = forms.ModelChoiceField(queryset=Generos.objects.filter(activo=True).order_by("nombre"),empty_label="Seleccione un Genero")
    arc_audio = forms.FileField()

    class Meta:
        model=Rsmusic
        fields = [
            'nombre',
            'interprete',
            'autor',
            'ano',
            'likes',
            'genero',
            'arc_audio',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        
        self.fields['arc_audio'].required = False
        #self.fields['arc_audio'].widget.attrs.update({'accept':'.mp3'})

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        if not nombre:
            raise forms.ValidationError("Nombre tema Requerido.")

        return nombre

    def clean_interprete(self):
        interprete = self.cleaned_data["interprete"]
        if not interprete:
            raise forms.ValidationError("Interprete Requerido.")

        return interprete

    def clean_autor(self):
        autor = self.cleaned_data["autor"]
        if not autor:
            raise forms.ValidationError("Autor Requerido.")

        return autor

    def clean_genero(self):
        genero = self.cleaned_data["genero"]
        if not genero:
            raise forms.ValidationError("Genero Requerido.")

        return genero

    def clean_arc_audio(self):
        arc_audio = self.cleaned_data["arc_audio"]
    #    if not arc_audio:
    #        raise forms.ValidationError("Archivo de audio Requerido. ")
        #if (not arc_audio.endswith('.mp3')):
        #    raise forms.ValidationError("Solo archivos de audio")
        return arc_audio

class RadicaEncForm(forms.ModelForm):
    class Meta:
        model=Contrato
        fields = [
            'no_publicidad',
            'nit_cliente',
            'nit_anunciante',
            'idagencia',
            'asesor_comercial',
            'fecha_inicio',
            'fecha_final',
            'producto',
            'presupuesto_cliente', 
            'valor_bruto',
            'porc_descuento',
            'valor_neto',
            'orden_provicional',
        ]
    fecha_inicio = forms.DateField(widget=DatePicker())
    fecha_final = forms.DateField(widget=DatePicker())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['fecha_inicio'].widget.attrs.update({'style':'text-align: center;'})
        self.fields['fecha_final'].widget.attrs.update({'style':'text-align: center;'})
        #self.fields['porc_descuento'].widget.attrs.update({'style':'text-align: center; color:red;'})
        #self.fields['valor_bruto'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['porc_descuento'].widget.attrs['readonly']= True
        #self.fields['valor_neto'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:blue; font-size:14px; width: 200px;'})
        #self.fields['valor_neto'].widget.attrs.update({'onchange': 'valida_descuento(id)'})
        #self.fields['tcredito'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['transferencia'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['bonos'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['credito'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        #self.fields['descuento'].widget.attrs.update({'onkeyup': 'format(this)', 'style':'text-align: right; color:red; font-size:14px; width: 200px;'})
        self.fields['porc_descuento'].required = False
        self.fields['valor_bruto'].required = False
        self.fields['valor_neto'].required = False
        self.fields['idagencia'].required = False
        self.fields['presupuesto_cliente'].required = False


    def clean_no_publicidad(self):
        no_publicidad = self.cleaned_data["no_publicidad"]
        if not no_publicidad:
            raise forms.ValidationError("Numero orden/Contrato Requerido.")

        return no_publicidad

    def clean_producto(self):
        producto = self.cleaned_data["producto"]
        if not producto:
            raise forms.ValidationError("Producto Requerido.")

        return producto

    def clean_nit_cliente(self):
        nit_cliente = self.cleaned_data["nit_cliente"]
        if not nit_cliente:
            raise forms.ValidationError("NIT/CC Cliente Requerido.")

        return nit_cliente

    def clean_nit_anunciante(self):
        nit_anunciante = self.cleaned_data["nit_anunciante"]
        if not nit_anunciante:
            raise forms.ValidationError("NIT/CC Anunciante Requerido.")

        return nit_anunciante

    def clean_asesor_comercial(self):
        asesor_comercial = self.cleaned_data["asesor_comercial"]
        if not asesor_comercial:
            raise forms.ValidationError("NIT/CC Anunciante Requerido.")

        return asesor_comercial

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data["fecha_inicio"]
        if not fecha_inicio:
            raise forms.ValidationError("vigencia contrato requerida")
        return fecha_inicio

    def clean_fecha_final(self):
        fecha_final = self.cleaned_data["fecha_final"]
        if not fecha_final:
            raise forms.ValidationError("vigencia contrato requerida")
        return fecha_final




class RadicaDetalleForm(forms.ModelForm):
    obs_producto = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model= Contra1
        fields = [
            'producto', 'referencia',
            #'tiempo_cuna', 'costo_cuna',  
         #'fr_dia', 'mencion','mes', 'ano', 

        #'total_cunas', 'bonificados', 'total_dias_mes', 
        #'valor_bruto', 'valor_neto', 'porc_iva', 'sel',
        #'porc_canje', 'valor_orden', 'valor_factura', 'obs_producto',
        #'fecha_inicio_pauta', 'fecha_final_pauta', 'tarifa_aplicada',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        archivo_cuna = forms.FileField()
        
    def clean_producto(self):  
        producto = self.cleaned_data["producto"]
        if not producto:
            raise forms.ValidationError("Producto Requerido")

        return producto

    def clean_tiempo_cuna(self):
        tiempo_cuna = self.cleaned_data["tiempo_cuna"]
        if not tiempo_cuna:
            raise forms.ValidationError("Tiempo Requerido")
        if tiempo_cuna <= 0:
            raise forms.ValidationError("Tiempo Incorrecto")
        return tiempo_cuna

    def clean_costo_cuna(self):
        costo_cuna = self.cleaned_data["costo_cuna"]
        if not costo_cuna:
            raise forms.ValidationError("Costo Requerido")
        if costo_cuna <= 0:
            raise forms.ValidationError("Costo Incorrecto")
        return costo_cuna

    def clean_referencia(self):
        referencia = self.cleaned_data["referencia"]
        if not referencia:
            raise forms.ValidationError("Referencia Requerida")
        return referencia

    def clean_fr_dia(self):
        fr_dia = self.cleaned_data["fr_dia"]
        if not fr_dia:
            raise forms.ValidationError("Frecuencia Requerida")
        if fr_dia<= 0:
            raise forms.ValidationError("Frecuencia Incorrecta")
        return fr_dia

    def clean_valor_orden(self):
        valor_orden = self.cleaned_data["valor_orden"]
        if not valor_orden:
            raise forms.ValidationError("Valor Orden Requerido")
        if valor_orden <= 0:
            raise forms.ValidationError("Valor Orden Incorrecto")
        return valor_orden

    def clean_valor_factura(self):
        valor_factura = self.cleaned_data["valor_factura"]
        if not valor_factura:
            raise forms.ValidationError("Valor Factura Requerido")
        if valor_factura <= 0:
            raise forms.ValidationError("Valor Factura Incorrecto")
        return valor_factura


DetalleMovimientosFormSet = inlineformset_factory(Contrato,Contra1,form=RadicaDetalleForm, extra=1,
    min_num=0,
    validate_min=True, can_delete=False)