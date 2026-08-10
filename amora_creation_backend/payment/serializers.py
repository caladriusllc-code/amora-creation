from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Transaction
        fields = [
            'id',
            'order',
            'amount',
            'status',
            'status_label',
            'payment_method',
            'provider_reference',
            'error_message',
            'created_at',
        ]
        read_only_fields = fields


class PaymentInitiateSerializer(serializers.Serializer):
    order_id       = serializers.UUIDField()
    payment_method = serializers.ChoiceField(
        choices=Transaction.PaymentMethod.choices,
        default=Transaction.PaymentMethod.SIMULATION
    )


class PaymentSimulateSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()
    outcome        = serializers.ChoiceField(choices=['SUCCESS', 'FAILED'])