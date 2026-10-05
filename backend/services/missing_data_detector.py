from datetime import datetime

import boto3

from backend.config.settings import settings
from backend.services.incident_service import create_incident


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def check_expected_file(
    dataset: str,
    file_name: str
) -> bool:

    s3_key = f"bronze/{dataset}/{file_name}"

    try:
        s3.head_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=s3_key
        )

        print(
            f"✅ File received: {s3_key}"
        )

        return True

    except s3.exceptions.ClientError as error:

        error_code = error.response.get(
            "Error",
            {}
        ).get(
            "Code"
        )

        if error_code in ["404", "NoSuchKey"]:

            print(
                f"❌ Missing file: {s3_key}"
            )

            create_incident(
                dataset=dataset,
                file_name=file_name,
                incident_type="MISSING_DATA",
                severity="HIGH",
                description=(
                    f"Expected daily file was not "
                    f"received in the Bronze layer: "
                    f"{s3_key}"
                )
            )

            return False

        raise


if __name__ == "__main__":

    check_expected_file(
        dataset="sales",
        file_name="sales_2026-04-01.csv"
    )