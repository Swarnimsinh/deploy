import requests
from django.conf import settings

BASE_URL = "https://api.cal.com/v2"


def get_bookings(status="upcoming"):
    headers = {
        "Authorization": f"Bearer {settings.CAL_API_KEY}",
        "cal-api-version": settings.CAL_API_VERSION,
    }

    response = requests.get(
        f"{BASE_URL}/bookings",
        headers=headers,
        params={
            "status": status
        }
    )

    response.raise_for_status()
    return response.json()


def get_bookings_for_email(email, status="upcoming"):
    """Fetch bookings and filter by attendee email for a specific user."""
    data = get_bookings(status=status)
    all_bookings = data.get("data", [])

    user_bookings = []
    for booking in all_bookings:
        attendees = booking.get("attendees", [])
        for attendee in attendees:
            if attendee.get("email", "").lower() == email.lower():
                user_bookings.append(booking)
                break

    return user_bookings