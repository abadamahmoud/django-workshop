from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Task

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):      
        role = validated_data.pop('role', None)
        if not role:
            raise serializers.ValidationError("role field is required.")
        
        validated_data['username'] = validated_data['email']

        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError("password field is required.")
        
        if role == 'ADMIN':
            user = User.objects.create_superuser(password=password, role=role, **validated_data)
        else:
            user = User.objects.create_user(password=password, role=role, **validated_data)
        user.is_active = True
        user.save()
        return user
        

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'owner']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'owner': {'read_only': True}
            }

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    project_id = serializers.IntegerField(write_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'created_by', 'assigned_to', 'project', 'project_id', 'assigned_to_id']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
            'assigned_to': {'read_only': True},
            'project': {'read_only': True}
        }
    
    def create(self, validated_data):
        project_id = validated_data.pop('project_id', None)
        assigned_to_id = validated_data.pop('assigned_to_id', None)

        if not project_id:
            raise serializers.ValidationError("project_id field is required.")
        
        if not assigned_to_id:
            raise serializers.ValidationError("assigned_to_id field is required.")
        
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project does not exist.")
        
        try:
            assigned_to = User.objects.get(pk=assigned_to_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        
        validated_data['project'] = project
        validated_data['assigned_to'] = assigned_to
        return super().create(validated_data)