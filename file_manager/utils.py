import mimetypes
from mimetypes import guess_type


def detect_file_type(file_url):
    """Detect file type based on extension or MIME type."""
    extension = file_url.split('.')[-1].lower()
    mime_type, _ = guess_type(file_url)

    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'svg', 'ico','jtif', 'jp2', 'j2k', 'jpf', 'jpx', 'jpt']

    video_extensions = ['mp4', 'avi', 'mov', 'webm', 'mkv']
    pdf_extensions = ['pdf']
    document_extensions = ['docx', 'doc', 'xlsx', 'xls', 'pptx', 'txt']

    # Use MIME type to improve accuracy (optional)
    if mime_type and mime_type.startswith('image'):
        return 'image'
    elif mime_type and mime_type.startswith('video'):
        return 'video'
    elif mime_type == 'application/pdf':
        return 'pdf'

    # Fall back to extension-based detection
    if extension in image_extensions:
        return 'image'
    elif extension in video_extensions:
        return 'video'
    elif extension in pdf_extensions:
        return 'pdf'
    elif extension in document_extensions:
        return 'document'
    return 'unsupported'