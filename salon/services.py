from asgiref.sync import sync_to_async
from salon.models import Client, Staff, Feedback


@sync_to_async
def get_or_create_client(name: str, phone: str) -> Client:
    client, _ = Client.objects.get_or_create(
        phone=phone,
        defaults={'name': name}
    )
    return client


@sync_to_async
def create_feedback(
    staff_id: int,
    client: Client,
    text: str
) -> Feedback:
    staff = Staff.objects.get(id=staff_id)

    return Feedback.objects.create(
        staff=staff,
        client=client,
        feedback=text
    )


@sync_to_async
def get_all_staff():
    return list(
        Staff.objects.select_related('salon').all()
    )


@sync_to_async
def get_staff_by_id(staff_id: int) -> Staff:
    return Staff.objects.filter(id=staff_id).first()
