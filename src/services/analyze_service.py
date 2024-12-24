import os
import uuid
from dataclasses import dataclass

from src.exceptions.medical_card.card import (
    NotFoundMedicalCardException, ThisIsNotYourMedicalCardException)
from src.repos.base import BaseRepo
from src.schemas.analyze import SAnalyzeRequest
from src.utils.aws_connect import s3
from src.utils.config_aws import settings


@dataclass
class AnalyzeService:
    analyze_repo: BaseRepo
    user_repo: BaseRepo
    medical_card_repo: BaseRepo

    async def add_analyze(self, doctor_id: int, analyze_data: SAnalyzeRequest):

        medical_card = await self.medical_card_repo.find_one(id=analyze_data.medical_card_id)
        if not medical_card:
            raise NotFoundMedicalCardException().message

        if doctor_id != medical_card.doctor_id:
            raise ThisIsNotYourMedicalCardException().message

        file_extension = os.path.splitext(analyze_data.file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        file_location = f"{temp_dir}/{unique_filename}"
        with open(file_location, "wb") as f:
            f.write(await analyze_data.file.read())

        safe_filename = uuid.uuid4().hex + file_extension

        s3.upload_file(
            Filename=file_location,
            Bucket=settings.BUCKET_NAME,
            Key=f"uploads/{safe_filename}",
        )

        os.remove(file_location)

        file_url = f"https://{settings.ENDPOINT_URL}/{settings.BUCKET_NAME}/uploads/{safe_filename}"

        await self.analyze_repo.add(
            analyze_name=analyze_data.analyze_name,
            result=analyze_data.result,
            file=file_url,
            medical_card_id=analyze_data.medical_card_id,
        )
        return 'Успешно создан анализ'
