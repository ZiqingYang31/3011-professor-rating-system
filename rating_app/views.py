from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import ModuleInstance, Professor, Rating
from .serializers import ModuleInstanceSerializer, ProfessorSerializer, RatingSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from .models import Rating, Professor, Module
from rest_framework.authentication import TokenAuthentication


class ModuleInstanceListView(generics.ListAPIView):

    queryset = ModuleInstance.objects.all()
    serializer_class = ModuleInstanceSerializer


class ProfessorAverageRatingView(APIView):
    def get(self, request, professor_id, module_code):
        try:
            professor = Professor.objects.filter(id=professor_id).first()
            if not professor:
                return Response({"error": "Professor not found"}, status=404)
            
            module = Module.objects.filter(code=module_code).first()
            if not module:
                return Response({"error": "Module not found"}, status=404)

            average_rating = Rating.objects.filter(
                professor=professor,
                module_instance__module=module
            ).aggregate(Avg('rating'))
            
            avg_rating = average_rating['rating__avg'] if average_rating['rating__avg'] is not None else 0

            print(f"Professor: {professor.name}, Module: {module.name}, Average Rating: {avg_rating}")

            return Response({
                "professor_name": professor.name,
                "module_name": module.name,
                "average_rating": avg_rating
            })

        except Exception as e:
            print(f"Error in ProfessorAverageRatingView: {str(e)}")
            return Response({"error": str(e)}, status=500)
    

class ProfessorRatingListView(generics.ListAPIView):

    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        professors = Professor.objects.all()
        results = []

        for professor in professors:
            avg_rating = Rating.objects.filter(professor=professor).aggregate(Avg('rating'))['rating__avg']
            avg_rating_display = round(avg_rating) if avg_rating is not None else "No Ratings"

            results.append({
                "id": professor.id,
                "name": professor.name,
                "average_rating": avg_rating_display
            })

        return Response(results)


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):

        professor = serializer.validated_data['professor']
        module_instance = serializer.validated_data['module_instance']
        user = self.request.user

        if not ModuleInstance.objects.filter(id=module_instance.id).exists():
            raise ValidationError({"detail": "Module instance not found."})
        
        if Rating.objects.filter(user=user, professor=professor, module_instance=module_instance).exists():
            raise ValidationError({"detail": "You have already rated this professor for this module instance."})

        serializer.save(user=user)


User = get_user_model()

class RegisterView(APIView):
    def get(self, request):
        return Response({
            "message": "To register, send a POST request with the following fields:",
            "required_fields": ["username", "email", "password"]
        })

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            token = Token.objects.create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

