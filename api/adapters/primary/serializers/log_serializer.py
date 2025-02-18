from rest_framework import serializers
from api.domain.entities.log_entry import LogEntry

class LogSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    admin_id = serializers.IntegerField()
    target_id = serializers.IntegerField()
    action = serializers.CharField()
    changes = serializers.JSONField()
    created_at = serializers.DateTimeField()
