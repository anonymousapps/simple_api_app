from .models import Task, Status
from rest_framework import serializers

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    status_name = serializers.ReadOnlyField(source='status.name')

    class Meta:
        model = Task
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['due_date'] = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
        return super(TaskSerializer, self).to_representation(instance)