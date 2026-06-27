from .serializer import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .serializer import *
from .models import *

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message":"User registered successfully"},
            status=status.HTTP_201_CREATED
            )
    return Response(
        serializer.errors,
        status = status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def login(request):
    username_or_email = request.data.get('username')
    password = request.data.get('password')
    
    username = username_or_email
    if username_or_email and '@' in username_or_email:
        from django.contrib.auth.models import User
        try:
            user_obj = User.objects.get(email__iexact=username_or_email)
            username = user_obj.username
        except User.DoesNotExist:
            pass

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_staff or user.is_superuser
            }
        )
    return Response(
        {'error':'Invalid Credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )

from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):

    user = request.user

    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

    return Response(data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from services.calcom import get_bookings, get_bookings_for_email


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser

@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_meetings(request):
    try:
        raw = get_bookings()
        bookings = raw.get("data", [])
        formatted = []
        for b in bookings:
            attendee = b.get("attendees", [{}])[0]
            formatted.append({
                "id": b.get("id"),
                "title": b.get("title", ""),
                "name": attendee.get("name", "Unknown"),
                "email": attendee.get("email", ""),
                "start": b.get("start", ""),
                "end": b.get("end", ""),
                "status": b.get("status", "pending").capitalize(),
                "meetingUrl": b.get("meetingUrl", ""),
            })
        return Response({"bookings": formatted})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_meetings(request):
    try:
        user_email = request.user.email
        if not user_email:
            return Response({"error": "Your account has no email set."}, status=400)
        bookings = get_bookings_for_email(user_email)
        formatted = []
        for b in bookings:
            formatted.append({
                "id": b.get("id"),
                "title": b.get("title", ""),
                "start": b.get("start", ""),
                "end": b.get("end", ""),
                "status": b.get("status", "pending").capitalize(),
                "meetingUrl": b.get("meetingUrl", ""),
            })
        return Response({"bookings": formatted})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_meeting(request):

    serializer = MeetingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

from rest_framework.permissions import IsAdminUser

# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def all_meetings(request):

#     meetings = Meeting.objects.select_related('user')

#     data = []

#     for meeting in meetings:
#         data.append({
#             "id": meeting.id,
#             "username": meeting.user.username,
#             "email": meeting.user.email,
#             "meeting_date": meeting.meeting_date,
#             "meeting_time": meeting.meeting_time,
#             "status": meeting.status
#         })
#     return Response(data)




# ///////////////////////////////////////////////////////////////////////////////////////////////////////
@api_view(['GET'])
def products(request):

    products = Product.objects.all()
    serializer = ProductSerializer(
        products,
        many=True
    )

    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, id):

    product = Product.objects.get(id=id)

    serializer = ProductSerializer(product)

    return Response(serializer.data)

from .models import CartItem, Product
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):

    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    product = Product.objects.get(id=product_id)

    cart_item = CartItem.objects.create(
        user=request.user,
        product=product,
        quantity=quantity
    )

    return Response(
        {
            "message": "Product added to cart"
        },
        status=status.HTTP_201_CREATED
    )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    )

    serializer = CartItemSerializer(
        cart_items,
        many=True
    )

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, id):

    cart_item = CartItem.objects.get(
        id=id,
        user=request.user
    )

    cart_item.delete()

    return Response(
        {"message": "Item removed"}
    )
#   /////////////////////////////////////////////////////////////////////////////////////////////
#     ****  Title  ****
@api_view(['GET'])
def get_title(request):                                                                 
    title = Title.objects.first()
    if not title:
        title = Title.objects.create(
            heading="Scale Distribution Infrastructure",
            sub_heading="We build high-fidelity visual channels that convert organic attention into strategic revenue pipelines."
        )
    serializer = TitleSerializer(title)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_title(request):
    title = Title.objects.first()
    if not title:
        title = Title.objects.create(
            heading="Scale Distribution Infrastructure",
            sub_heading="We build high-fidelity visual channels that convert organic attention into strategic revenue pipelines."
        )

    serializer = TitleSerializer(
        title,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)
# //////////////////////////////////////////////////////////////////////////////////////////////////////
#    *** Portfolio ***
@api_view(['GET'])
def get_portfolios(request):

    portfolios = Portfolio.objects.all()

    serializer = PortfolioSerializer(
        portfolios,
        many=True
    )

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_portfolio(request, pk):

    portfolio = Portfolio.objects.get(id=pk)

    serializer = PortfolioSerializer(
        portfolio,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)
# ///////////////////////////////////////////////////////////////////////
@api_view(['GET'])
def SView(request):
    data = Service.objects.all()
    serializer = ServiceSerializer(data,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def TView(request):
    data = Testimonial.objects.all()
    if data.count() == 0:
        defaults = [
            {
                "quote": "I knew I would hire them one day—and once I started video distribution, they were the only choice. Month one: 6M views. They truly understood my style.",
                "name": "Jasmin Alić",
                "position": "LinkedIn Premium Creator",
                "metric": "6.2M Views"
            },
            {
                "quote": "I wouldn't have even started my visual distribution journey if it wasn't for them. Their execution speed speaks for itself. Hands-off excellence.",
                "name": "Lara Acosta",
                "position": "Founder, Literally Academy",
                "metric": "400k+ Follows"
            },
            {
                "quote": "We collaborated for 3 months, outputting 45 high-caliber clips. They manage raw media effectively, respect instructions, and deliver consistently.",
                "name": "Jimmy Conover",
                "position": "Scale Video Agency",
                "metric": "150% CTR"
            }
        ]
        for item in defaults:
            Testimonial.objects.create(**item)
        data = Testimonial.objects.all()

    serializer = TestimonialSerializer(data,many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_testimonials(request):
    if not isinstance(request.data, list):
        return Response({"error": "Expected a list of testimonials"}, status=400)
    
    Testimonial.objects.all().delete()
    for item in request.data:
        Testimonial.objects.create(
            quote=item.get('quote', ''),
            name=item.get('name', ''),
            position=item.get('position', ''),
            metric=item.get('metric', '')
        )
    
    data = Testimonial.objects.all()
    serializer = TestimonialSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_settings(request):
    settings = WebsiteSettings.objects.first()
    if not settings:
        settings = WebsiteSettings.objects.create()
    serializer = WebsiteSettingsSerializer(settings)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_settings(request):
    settings = WebsiteSettings.objects.first()
    if not settings:
        settings = WebsiteSettings.objects.create()
    serializer = WebsiteSettingsSerializer(
        settings,
        data=request.data,
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def VView(request):
    data = Video.objects.all()
    serializer = VideoSerializer(data,many=True)
    return Response(serializer.data)


import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_video(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)
    
    uploaded_file = request.FILES['file']
    # Create the videos directory if not exists
    videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)
        
    fs = FileSystemStorage(location=videos_dir)
    filename = fs.save(uploaded_file.name, uploaded_file)
    file_url = settings.MEDIA_URL + 'videos/' + filename
    
    return Response({"url": file_url})


