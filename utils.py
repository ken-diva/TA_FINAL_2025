from datetime import timedelta, datetime


def format_time(value):
    """
    Mengubah timedelta, datetime.time, atau string waktu ('09:00:00')
    menjadi format 'HH.MM'
    """
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}.{minutes:02d}"
    elif hasattr(value, "strftime"):  # datetime.time atau datetime.datetime
        return value.strftime("%H.%M")
    elif isinstance(value, str):
        return value[:5].replace(":", ".")
    return value  # fallback jika tidak cocok
