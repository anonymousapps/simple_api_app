from .models import Task, Status
from rest_framework import serializers

class StatusSerializerWeb(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class TaskSerializerWeb(serializers.HyperlinkedModelSerializer):
    status_name = serializers.ReadOnlyField(source='status.name')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['due_date'] = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
        return super(TaskSerializerWeb, self).to_representation(instance)

class TaskSerializerAPI(serializers.ModelSerializer):
    status_name = serializers.ReadOnlyField(source='status.name')

    class Meta:
        model = Task
        fields = '__all__'
    
    def to_representation(self, instance):
        self.fields['due_date'] = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
        return super(TaskSerializerAPI, self).to_representation(instance)

class TaskSerializerAPIEditStatus(serializers.ModelSerializer):
    # seperate to only allow edit of status from API call
    class Meta:
        model = Task
        fields = ['status']

class StatusSerializerAPI(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'