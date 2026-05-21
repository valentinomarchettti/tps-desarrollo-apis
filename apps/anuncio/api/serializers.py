from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from decimal import Decimal, ROUND_HALF_UP

from ..models import Anuncio, Categoria, OfertaAnuncio


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'activa']


class AnuncioSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)
    precio_inicial_convertido = serializers.SerializerMethodField()
    moneda_convertida = serializers.SerializerMethodField()
    categorias_ids = PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        many=True,
        write_only=True,
        source='categorias',
    )

    class Meta:
        model = Anuncio
        fields = [
            'uuid',
            'titulo',
            'descripcion',
            'precio_inicial',
            'precio_inicial_convertido',
            'moneda_convertida',
            'imagen',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',
            'categorias_ids',
            'publicado_por',
            'oferta_ganadora',
        ]
        read_only_fields = ['uuid', 'publicado_por', 'oferta_ganadora']

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        precio_inicial = data.get('precio_inicial')
        categorias = data.get('categorias')

        if fecha_inicio and fecha_inicio <= timezone.now():
            raise serializers.ValidationError({
                'fecha_inicio': 'La fecha de inicio debe ser posterior a la fecha actual.'
            })

        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise serializers.ValidationError({
                'fecha_fin': 'La fecha de fin debe ser posterior a la fecha de inicio.'
            })

        if precio_inicial is not None and precio_inicial <= 0:
            raise serializers.ValidationError({
                'precio_inicial': 'El precio inicial debe ser mayor a cero.'
            })

        if self.instance is None and not categorias:
            raise serializers.ValidationError({
                'categorias_ids': 'Debe ingresar al menos una categoria.'
            })

        return data

    def create(self, validated_data):
        categorias = validated_data.pop('categorias')
        anuncio = Anuncio.objects.create(**validated_data)
        anuncio.categorias.set(categorias)
        return anuncio

    def update(self, instance, validated_data):
        categorias = validated_data.pop('categorias', None)
        anuncio = super().update(instance, validated_data)
        if categorias is not None:
            anuncio.categorias.set(categorias)
        return anuncio

    def get_precio_inicial_convertido(self, obj):
        exchange_rate = self.context.get('exchange_rate')
        if exchange_rate is None:
            return None

        try:
            rate = Decimal(str(exchange_rate))
            converted = (obj.precio_inicial * rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            return converted
        except Exception:
            return None

    def get_moneda_convertida(self, obj):
        if self.context.get('exchange_rate') is None:
            return None
        return self.context.get('target_currency')


class OfertaAnuncioSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OfertaAnuncio
        fields = ['precio_oferta', 'fecha_oferta', 'usuario']
        read_only_fields = ['fecha_oferta', 'usuario']

    def validate_precio_oferta(self, value):
        anuncio = self.context['anuncio']

        if value <= anuncio.precio_inicial:
            raise serializers.ValidationError(
                'La oferta debe ser mayor al precio inicial del articulo.'
            )

        ultima_oferta = anuncio.ofertas.order_by('-precio_oferta').first()
        if ultima_oferta and value <= ultima_oferta.precio_oferta:
            raise serializers.ValidationError(
                f'La oferta debe ser mayor que la oferta mas alta actual. (${ultima_oferta.precio_oferta})'
            )

        return value
