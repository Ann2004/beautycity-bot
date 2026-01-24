from asgiref.sync import sync_to_async
from salon.models import Client, Staff, Feedback, Salon, Service, Appointment, Promo
from datetime import date, timedelta


@sync_to_async
def get_or_create_client(
    name: str,
    phone: str,
    telegram_id: int | None = None
) -> Client:
    client, created = Client.objects.get_or_create(
        phone=phone,
        defaults={
            'name': name,
            'telegram_id': str(telegram_id) if telegram_id else None
        }
    )

    # если клиент уже был, но telegram_id ещё не сохранён
    if not created and telegram_id and not client.telegram_id:
        client.telegram_id = str(telegram_id)
        client.save(update_fields=['telegram_id'])

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
def get_staff_by_id(staff_id: int):
    return Staff.objects.select_related('salon').get(id=staff_id)


@sync_to_async
def get_salon_by_id(salon_id: int) -> Salon:
    return Salon.objects.filter(id=salon_id).first()


@sync_to_async
def get_all_salons():
    return list(Salon.objects.all())


@sync_to_async
def get_all_services():
    return list(Service.objects.all())


@sync_to_async
def get_services_by_staff(staff_id):
    staff = Staff.objects.prefetch_related('services').get(id=staff_id)
    return list(staff.services.all())


@sync_to_async
def get_staff_available_slots(staff_id: int, target_date):
    all_slots = [f"{hour:02d}:00" for hour in range(10, 20)]

    # Занятые слоты на дату
    busy_appointments = Appointment.objects.filter(
        staff_id=staff_id,
        appointment_date=target_date
    )

    busy_times = [appointment.time.strftime('%H:%M') for appointment in busy_appointments]
    # Свободные слоты
    available_slots = [slot for slot in all_slots if slot not in busy_times]

    return available_slots


@sync_to_async
def get_staff_busy_days(staff_id: int, days_ahead: int = 7):
    start_date = date.today()
    end_date = start_date + timedelta(days=days_ahead)

    # записи мастера на перио
    appointments = Appointment.objects.filter(
        staff_id=staff_id,
        appointment_date__gte=start_date,
        appointment_date__lte=end_date
    ).order_by('appointment_date', 'time')

    # группировка по датам
    busy_days = {}
    for appointment in appointments:
        date_str = appointment.appointment_date.isoformat()
        if date_str not in busy_days:
            busy_days[date_str] = []
        busy_days[date_str].append(appointment.time.strftime('%H:%M'))

    return busy_days


@sync_to_async
def is_staff_available(staff_id: int, target_date, target_time):
    exists = Appointment.objects.filter(
        staff_id=staff_id,
        appointment_date=target_date,
        time=target_time
    ).exists()

    return not exists


@sync_to_async
def find_available_master_for_slot(salon_id: int, service_id: int, target_date: str, target_time: str): 
    target_date_obj = date.fromisoformat(target_date)

    # все мастера с выбранной услугой
    masters = Staff.objects.filter(
        salon_id=salon_id,
        services__id=service_id
    ).distinct()

    # поиск свободного мастера
    for master in masters:
        is_busy = Appointment.objects.filter(
            staff_id=master.id,
            appointment_date=target_date_obj,
            time=target_time
        ).exists()

        if not is_busy:
            return master

    return None


@sync_to_async
def get_available_slots_for_salon_service(salon_id: int, service_id: int, target_date):
    all_possible_slots = [f"{hour:02d}:00" for hour in range(10, 20)]

    # все мастера с услугой
    available_masters = Staff.objects.filter(
        salon_id=salon_id,
        services__id=service_id
    ).distinct()

    if not available_masters:
        return []

    free_time_slots = []
    for time_slot in all_possible_slots:
        # мастера, у которого свободен этот временной слот
        slot_is_available = False
        for master in available_masters:
            is_master_busy = Appointment.objects.filter(
                staff_id=master.id,
                appointment_date=target_date,
                time=time_slot
            ).exists()

            if not is_master_busy:
                slot_is_available = True
                break   # + свободный мастер

        if slot_is_available:
            free_time_slots.append(time_slot)
    return free_time_slots


@sync_to_async
def get_busy_days_for_salon_service(salon_id: int, service_id: int, days_ahead: int = 7):
    start_date = date.today()
    end_date = start_date + timedelta(days=days_ahead)

    # мастера в салоне с услугой
    available_masters = Staff.objects.filter(
        salon_id=salon_id,
        services__id=service_id
    ).distinct()

    if not available_masters:
        return {}

    master_ids = [master.id for master in available_masters]

    # все записи для этих мастеров на период
    appointments = Appointment.objects.filter(
        staff_id__in=master_ids,
        appointment_date__gte=start_date,
        appointment_date__lte=end_date
    ).order_by('appointment_date', 'time')

    # группа по датам
    busy_days_info = {}
    for appointment in appointments:
        date_str = appointment.appointment_date.isoformat()
        if date_str not in busy_days_info:
            busy_days_info[date_str] = []
        busy_days_info[date_str].append(appointment.time.strftime('%H:%M'))

    return busy_days_info


@sync_to_async
def get_promo_by_code(code: str) -> Promo | None:
    return Promo.objects.filter(code__iexact=code).first()


@sync_to_async
def get_service_by_id(service_id: int) -> Service:
    return Service.objects.get(id=service_id)


@sync_to_async
def create_appointment(
    *,
    client: Client,
    service: Service,
    staff: Staff,
    appointment_date,
    time,
    promo: Promo | None = None
) -> Appointment:
    return Appointment.objects.create(
        client=client,
        service=service,
        staff=staff,
        appointment_date=appointment_date,
        time=time,
        promo=promo
    )