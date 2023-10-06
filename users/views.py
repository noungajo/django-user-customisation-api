from rest_framework import  permissions,views
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from knox.views import LoginView as KnoxLoginView,LogoutAllView as KnoxLogoutAllView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from random import randint
import hashlib as hs
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework import generics
from .sms import sendsms
from .texte import *
from django.conf import settings
from django.core.mail import send_mail
from .email import *
from django.contrib.auth import get_user_model
# reset pwd
from rest_framework.parsers import MultiPartParser
from .unique_code import generate_unique_code
User = get_user_model()
class RegistrationView(APIView):
    #parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        request_body=SaveUserSerializer(),
        responses={
            status.HTTP_201_CREATED: CreatedUserSerializer(),
             422: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Unprocessable Entity",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
              400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Bad request",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    
    def post(self, request, *args, **kwargs):
        #sauvegarde des donnees user
        serializer = SaveUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        """
        trouver un moyen de generer un code unique et eliminer la date
        """
        code = generate_unique_code()
        # verification du numero de telphone
        phone_verification = UserVerification(
            user = User.objects.get(pk=serializer.data['id']),
            phone_number = serializer.data['telephone'],
            code = code,
            expires_at = timezone.now()+timezone.timedelta(minutes=20)
        )

        try:
            # ================= sms ======================
            message_code = f'{messageResetPassword} {code}'
            sendsms(user.telephone,message_code)
            #================= mail ==========================
            subject = subjectResetPassword
            body = f"{salut} {user.full_name},\n {messageResetPassword} {code}\n{signature}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject, body, email_from, recipient_list)
        except Exception as e:
            pass
        # une fois le sms envoye cela est sauvegarder en bd
        phone_verification.save()
        
        data = serializer.data 
        data['phone_verification'] = phone_verification
        #creation de l'utilisateur:on affecte l'id d l'utilisateur cree avec le code genere
        serializer = CreatedUserSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):
        if 'password' in serializer.validated_data.keys():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()

class ListUsers(APIView):
    """
    view to list all users in the system
    * requires token authentication.
    * only admin users are able to access this view.
    """

    permission_classes = [permissions.IsAdminUser]
    @swagger_auto_schema(
        
        responses={
            200: DisplayUserSerializer(),
             401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Unauthorized",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    def get(self,request):
        users = User.objects.all()
        data = []
        for user in users:
            serializer = DisplayUserSerializer(user).data
            data.append(serializer)
        return Response(data,status=status.HTTP_200_OK)
class CurrentUser(APIView):
    """
    view to list all users in the system
    * requires token authentication.
    """

    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        
        responses={
            200: DisplayUserSerializer(),
             401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Unauthorized",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )

    def get(self,request):
        user = request.user
        if user.is_anonymous:
            return Response({'msg':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
        data = DisplayUserSerializer(user).data
        return Response(data,status=status.HTTP_200_OK)
# Authorisation : Token xxxxxxxx
class UpdateUserViews(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = DisplayUserSerializer 
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        
        responses={
            status.HTTP_200_OK: DisplayUserSerializer(),
             403: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Forbiden",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    
    #def get_permissions(self):
        #permission_classes = [permissions.IsAuthenticated] 
        #return [permission() for permission in permission_classes]
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user,data=request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

class DeleteUser(generics.DestroyAPIView):
    queryset = User.objects.all()
    @swagger_auto_schema(
        
        responses={
            204: {},
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="UNAUTHORIZED",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        curr_user = request.user
        if user != curr_user and not curr_user.is_staff:
            return Response({"message": "Not allowed"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_hash = hs.md5(str(user).encode()).hexdigest()
        user.is_active = False
        user.telephone = user_hash
        user.email = "".join([user_hash,"@dotche.del"])
        user.username = user_hash
        user.fullname = user_hash
        user.password = user_hash
        user.address = user_hash
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhoneNumberVerifyView(views.APIView):
    
    @swagger_auto_schema(
        operation_description="Verify code entered by user for phone number verification",
        request_body=PhoneCodeSerializer(),
        responses={
            200: UserVerificationSerializer(),
            403: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Code expired",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Account verification not found",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            422: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Unprocessable Entity",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request):
        serializer = PhoneCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification = None
        try:
            verification = UserVerification.objects.get(user=serializer.data['user_id'])
        except ObjectDoesNotExist:
            return Response({'message': 'User Phone verification not found'}, status=status.HTTP_404_NOT_FOUND)
        if verification.code != serializer.data['code']:
            return Response({'message': "CODE INCORRECT"}, status=422)
            
        if verification.expires_at < timezone.now():
            return Response({'message': "Code has Expired"}, status=status.HTTP_403_FORBIDDEN)
        
        verification.verified_at = timezone.now()
        verification.save()
        user = User.objects.get(id=serializer.data['user_id'])
        user.is_active = True
        serializer = UserVerificationSerializer(verification)
        return Response(serializer.data)

class PhoneCodeRenew(views.APIView):
    
    @swagger_auto_schema(
        operation_description="Regenerate new phone number verification code for user and send it to them",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required= ['user_id'],
            properties={
                'user_id' : openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={
            200: UserVerificationSerializer(),
            status.HTTP_400_BAD_REQUEST:openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Bad request",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def post(self, request):
        try:
            phone_verification = UserVerification.objects.get(
                user=User.objects.get(pk=request.data['user_id'])
            )
            #utiliser le datetime pour l unicite
            phone_verification.code = generate_unique_code()
          
            try:
                # ================= sms ======================
                message_code = f'{message} {phone_verification.code}'
                sendsms(phone_verification.user.telephone,message_code)
                #================= mail ==========================
                subject = subject
                body = f"{salut} {phone_verification.user.full_name},\n {message} {phone_verification.code}\n{signature}"
                send_email(subject,body,serializer.data['email'])
            except Exception as e:
                pass
           
            phone_verification.save()
            serializer = UserVerificationSerializer(phone_verification)
            return Response(serializer.data,status = status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LoginView(KnoxLoginView):
    serializer_class = UserLoginSerializer
    permission_classes = []
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[ 'password' ],
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING),
                'password':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: {},
            422:openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Unproceed request",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(telephone=serializer.data['email'], password=serializer.data['password'])
        
        if user is None:
            data = {
                "message": "Invalid credentials"
            }
            return Response(data,status=422)
        
        request.user = user
        return super().post(request, format)

class EmailCheckView(views.APIView):
    
    @swagger_auto_schema(
        operation_description="Check if a particular email has already been taken",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[ 'email'],
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
                responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="True if e-mail is taken, False otherwise",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            ),
            422: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Unprocessable Entity",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def post(self, request):
        if "email" not in request.data.keys():
            return Response({"status": "UNKNOWN"}, status=422)
        
        email = request.data['email']
        users = User.objects.filter(email=email)
        if len(users) > 0 :
            return Response({"status": True},status=200)
        
        return Response({"status": False},status=200)

class TelephoneCheckView(views.APIView):
    
    @swagger_auto_schema(
        operation_description="Check if a particular telephone number has already been taken",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[ 'telephone'],
            properties={
                'telephone':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="True if phone number is taken, False otherwise",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            ),
            406: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Incorrect Data supplied",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    @action(detail=True, methods=['post'])
    def post(self, request):
        if "telephone" not in request.data.keys():
            return Response({"status": "UNKNOWN"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        telephone = request.data['telephone']
        
        users = User.objects.filter(telephone=telephone)
        if len(users) > 0 :
            return Response({"status": True},status=200)
        
        return Response({"status": False},status=200)
class ForgotPasswordView(views.APIView):
    @swagger_auto_schema(
        operation_description="Get a code for reset password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[ 'email'],
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="The Code was successfully send",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Incorrect Data supplied",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Not Found",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
    def post(self, request):
        email = request.data.get('email', None)
        if email is None:
            return Response({'error': 'Email field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        code = 0
        try:
            checkResetPwd = ResetPasswordModel.objects.get(email=email)
            code = checkResetPwd.code
        except ResetPasswordModel.DoesNotExist:
            code = generate_unique_code()
            resetPasswordObject = ResetPasswordModel(
                email = user.email,
                code = code
            )
            resetPasswordObject.save()
        try:
            # ================= sms ======================
            message_code = f'{messageResetPassword} {code}'
            sendsms(user.telephone,message_code)
            #================= mail ==========================
            subject = subjectResetPassword
            body = f"{salut} {user.full_name},\n {messageResetPassword} {code}\n{signature}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject, body, email_from, recipient_list)
        except Exception as e:
            pass
       

       
        return Response({'message': responseResetPassword}, status=status.HTTP_200_OK)

class ResetPasswordView(views.APIView):
    @swagger_auto_schema(
        operation_description="Set the new password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[ 'code','new_password'],
            properties={
                'code':openapi.Schema(type=openapi.TYPE_INTEGER),
                'new_password':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="True if the password has been successfully reset.",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Incorrect Data supplied",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Not Found",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        }
    )
   
    def post(self, request):
        code = request.data.get('code', None)
        new_password = request.data.get('new_password', None)
        if code is None or new_password is None:
            return Response({'error': 'Code and new_password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_pwd = ResetPasswordModel.objects.get(code=code)
        except ResetPasswordModel.DoesNotExist:
            return Response({'error': 'Invalid code.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(email=reset_pwd.email)
        user.password = make_password(new_password)
        user.save()
        reset_pwd.delete()

        return Response({'message': 'Password has been successfully reset.'}, status=status.HTTP_200_OK)


class ChangePasswordView(views.APIView):

    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Change the current password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[ 'current_password','new_password'],
            properties={
                'current_password':openapi.Schema(type=openapi.TYPE_STRING),
                'new_password':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="True if the password has been successfully modify.",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Incorrect Data supplied",
                properties={
                    "status" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
              401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="UNAUTHORIZED",
                properties={
                    "message" : openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    
    def post(self, request):
        curr_user = self.request.user
        
        if curr_user.is_anonymous:
            return Response({'msg':'User Not found'},status=status.HTTP_401_UNAUTHORIZED)
        current_password = request.data.get('current_password', None)
        new_password = request.data.get('new_password', None)
        if current_password is None or new_password is None:
            return Response({'error': required_field}, status=status.HTTP_400_BAD_REQUEST)
        if current_password == new_password:
            return Response({'error': same_pwd}, status=status.HTTP_400_BAD_REQUEST)
        if not curr_user.check_password(current_password):
            return Response({'current_password': wrong_pwd}, status=status.HTTP_400_BAD_REQUEST)
        
        
        curr_user.password = make_password(new_password)
        curr_user.save()
        #requete de deconnection

        return Response({'message': pwd_change_success}, status=status.HTTP_200_OK)

