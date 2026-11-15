from django.core.exceptions import ValidationError

# Cloudinary's free plan rejects images larger than 10 MB (10485760 bytes).
# Stay just under that so the admin shows a clear message instead of a 500 page.
MAX_IMAGE_UPLOAD_BYTES = 10 * 1024 * 1024


def validate_image_size(image):
    """Reject images that Cloudinary would refuse to store."""
    size = getattr(image, "size", None)

    if size is not None and size > MAX_IMAGE_UPLOAD_BYTES:
        size_mb = size / (1024 * 1024)
        limit_mb = MAX_IMAGE_UPLOAD_BYTES // (1024 * 1024)
        raise ValidationError(
            f"This photo is {size_mb:.1f} MB, but the maximum is {limit_mb} MB. "
            "Please resize it (about 2500 px wide is plenty) and upload it again."
        )
