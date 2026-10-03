import boto3

from backend.config.settings import settings


s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION
)


def upload_file_to_s3(
    local_file_path: str,
    s3_key: str
) -> None:

    s3.upload_file(
        local_file_path,
        settings.S3_BUCKET_NAME,
        s3_key
    )

    print(f"Uploaded: {s3_key}")

from pathlib import Path


def upload_retail_data_to_bronze() -> None:

    datasets = [
        "sales",
        "inventory",
        "suppliers"
    ]

    for dataset in datasets:

        local_directory = (
            Path("data")
            / "raw"
            / dataset
        )

        for file_path in sorted(local_directory.glob("*.csv")):

            s3_key = (
                f"bronze/"
                f"{dataset}/"
                f"{file_path.name}"
            )

            upload_file_to_s3(
                local_file_path=str(file_path),
                s3_key=s3_key
            )


if __name__ == "__main__":
    upload_retail_data_to_bronze()