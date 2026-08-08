from rest_framework import serializers
from cart.models import GuestInfo

class GuestInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuestInfo
        fields = [
            'id', 
            'email', 
            'full_name', 
            'phone_number'
        ]
        read_only_fields = ['id']

    def validate_email(self, value):
        return value.lower().strip()

    def validate_full_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Le nom complet est trop court.")
        return value.strip()

    def validate_phone_number(self, value):
        import re
        cleaned = re.sub(r'\s+', '', value.strip())
        if not re.match(r'^\+?\d{8,15}$', cleaned):
            raise serializers.ValidationError(
                "Numéro de téléphone invalide. Formats acceptés : +2250701234567 ou 0701234567."
            )
        return cleaned