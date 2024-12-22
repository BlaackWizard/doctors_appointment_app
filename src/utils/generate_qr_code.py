import qrcode
from io import BytesIO


def generate_receipt(payment, service, patient, requisites):
    data = (
        f"""
            Имя пациента: {patient.full_name}\n
            Услуга: {service.title}\n
            Стоимость: {service.cost}\n
            Номер карты получателя: {requisites}\n 
            Дата: {payment.date}\n
        """
    )

    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make()
    img = qr.make_image()

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
