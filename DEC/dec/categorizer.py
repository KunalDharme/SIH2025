def categorize_file(file_info):
    """
    Categorize file based on MIME type or extension.
    """
    mime = file_info["mime"] or ""
    path = file_info["path"].lower()

    if "pdf" in mime or path.endswith(".pdf"):
        return "document"
    elif "word" in mime or path.endswith((".doc", ".docx")):
        return "document"
    elif "excel" in mime or path.endswith((".xls", ".xlsx", ".csv")):
        return "spreadsheet"
    elif "image" in mime or path.endswith((".jpg", ".jpeg", ".png", ".gif")):
        return "image"
    elif "video" in mime or path.endswith((".mp4", ".avi", ".mov", ".mkv")):
        return "video"
    elif "zip" in mime or path.endswith((".zip", ".rar", ".7z")):
        return "archive"
    else:
        return "other"
