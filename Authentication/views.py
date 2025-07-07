from django.core.mail import EmailMessage
from .serializers import EmailSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
# from rest_framework_simplejwt.tokens import RefreshToken
# from Roles_Rights.models import Rights_Designation_Wise
from django.contrib.auth.hashers import make_password
from Employee_Management.models import *
import random,hashlib,requests,uuid, datetime, time
from requests.exceptions import RequestException
from django.conf import settings

HOSTED_URL = "https://clientinfobackend.vichaarlab.in/crmlite/registered-data/"

User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                employee = Company_profile.objects.get(email=username)
                department_id = employee.department if employee else None
                designation_id = employee.designation if employee.designation else None
                employee_id = employee.empid 
            except Company_profile.DoesNotExist:
                return Response({'error': 'Employee record not found'}, status=status.HTTP_404_NOT_FOUND)

            # refresh = RefreshToken.for_user(user)

            if employee.status == False:
                return Response({
                    # 'refresh': str(refresh),
                    # 'access': str(refresh.access_token),
                    'user_type': "Super Admin" if user.is_superuser else "generaluser",
                    'employee_id': employee_id,
                    'employee_name': employee.name,
                    'employee_mobno': employee.mobileno,
                    'email': employee.email,
                    'department_id': department_id if department_id else None,
                    'designation_id': designation_id if designation_id else None
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        # print(username)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User record not found'}, status=status.HTTP_404_NOT_FOUND)
        if user is not None:
            try:
                employee = Company_profile.objects.get(email=username)
                department_id = employee.department if employee else None
                designation_id = employee.designation if employee.designation else None
                employee_id = employee.empid if employee.empid else None
            except Company_profile.DoesNotExist:
                return Response({'error': 'Employee record not found'}, status=status.HTTP_404_NOT_FOUND)

            # refresh = RefreshToken.for_user(user)

            if employee.status == False:
                return Response({
                    # 'refresh': str(refresh),
                    # 'access': str(refresh.access_token),
                    'user_type': "Super Admin" if user.is_superuser else "generaluser",
                    'employee_id': employee_id,
                    'employee_name': employee.name,
                    'employee_mobno': employee.mobileno,
                    'email': employee.email,
                    'department_id': department_id if department_id else None,
                    'designation_id': designation_id if designation_id else None
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# class CreateUserView(APIView):
#     def post(self, request):
#         # Get the username and password from the request data
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Validate that the username and password are provided
#         if not username or not password:
#             return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if the username already exists
#         if User.objects.filter(username=username).exists():
#             return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

#         # Create a new user with the provided username and hashed password
#         user = User.objects.create(
#             username=username,
#             password=make_password(password),  # Hash the password before saving
#         )

#         # Optionally, you can add extra user details like first_name, last_name, email, etc.

#         return Response({"message": "User created successfully", "username": user.username}, status=status.HTTP_201_CREATED)
    
from django.db import transaction, IntegrityError

class CreateUserView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        name = data.get("name")
        print(username, name)

        if not username:
            return Response({"error": "Username is required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        if Company_profile.objects.filter(email=username).exists():
            return Response({"error": "Company profile with this email already exists."}, status=400)

        # 🌐 Post to hosted URL before proceeding
        try:
            payload = {"username": username}
            print(HOSTED_URL)
            remote_response = requests.post(HOSTED_URL, json=payload, timeout=5)
            remote_response.raise_for_status()
        except RequestException as e:
            return Response({"error": "Cannot connect to license server. Please check your internet connection."}, status=503)

        try:
            with transaction.atomic():
                admin_user = User.objects.create(
                    username=username,
                    is_superuser=True,
                    is_staff=True,
                    is_license_valid=True,
                )

                Company_profile.objects.create(email=username, name=name)

                license_key = hashlib.sha256(f"{admin_user.id}_{time.time()}".encode()).hexdigest()
                license_expiry = datetime.datetime.today().date() + datetime.timedelta(days=15)
                admin_user.license_key = license_key
                admin_user.license_expiry = license_expiry
                admin_user.save()

                access_token = hashlib.sha256(f"{admin_user.id}_{time.time()}".encode()).hexdigest()
                refresh_token = str(uuid.uuid4())

                return Response({
                    "message": "Admin registered successfully!",
                    "refresh": refresh_token,
                    "access": access_token,
                    'license_expiry': license_expiry,
                }, status=201)

        except IntegrityError as e:
            return Response({"error": "User or Company profile creation failed due to unique constraint."}, status=400)


@api_view(['POST'])
def send_email(request):
    serializer = EmailSerializer(data=request.data)
    
    if serializer.is_valid():
        to = serializer.validated_data.get("to")
        cc = serializer.validated_data.get("cc", [])
        subject = serializer.validated_data.get("subject")
        message = serializer.validated_data.get("message")
        file = serializer.validated_data.get("file", None)

        try:
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, to, cc)
            # Attach file if provided
            if file:
                email.attach(file.name, file.read(), file.content_type)

            email.send()
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@api_view(['POST'])
def send_verification_email(request):
    email = request.data.get('email')

    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Retrieve the user
    try:
        user = Company_profile.objects.get(email=email)
    except Company_profile.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Generate OTP
        otp = random.randint(100000, 999999)
        cache.set(f"email_otp_{email}", otp, timeout=300)  # 5 minutes

        # Subject & sender
        subject = "PROPVICHAAR - Your Email Verification Code"
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render HTML template
        html_content = render_to_string('email/otp_template.html', {
            'otp': otp,
            'email': email,
            'site_name': 'PROPVICHAAR'
        })
        text_content = f"Your OTP for email verification is {otp}. It is valid for 5 minutes."

        # Email sending
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response({'message': 'OTP sent to your email successfully!'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.core.cache import cache
# Verify OTP
@api_view(['POST'])
def verify_email_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
        return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve OTP from cache
    cached_otp = cache.get(f"email_otp_{email}")

    if not cached_otp:
        return Response({'error': 'OTP expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)

    if str(otp) != str(cached_otp):
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    # Clear the OTP from cache after successful verification
    cache.delete(f"email_otp_{email}")

    return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def reset_admin_password(request):
    """Allow the admin to reset the password."""
    email = request.data.get('email')
    new_password = request.data.get('password')

    if not email or not new_password:
        return Response({'error': 'Email and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
    # Retrieve the user
    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the password (hash the new password before saving)
    user.password = make_password(new_password)
    user.save()

    # Clear OTP from cache
    cache.delete(f"email_otp_{email}")

    return Response({'message': 'Password has been successfully updated.'}, status=status.HTTP_200_OK)