from io import BytesIO

import qrcode


def generate_receipt(payment, service, patient, requisites):
    data = f"""
Имя пациента: {patient.full_name}
Услуга: {service.title}
Стоимость: {service.cost}
Номер карты получателя: {requisites}
Дата: {payment.date}
"""
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make()
    img = qr.make_image()

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
