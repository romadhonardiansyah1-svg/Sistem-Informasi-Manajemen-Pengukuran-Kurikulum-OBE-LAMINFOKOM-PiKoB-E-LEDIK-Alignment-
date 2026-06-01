"""
String formatting dan kode generator.
"""


def generate_kode(prefix, sequence_number, width=2):
    """
    Menghasilkan kode berformat prefix + angka zero-padded.
    Contoh: generate_kode("CPL", 1) -> "CPL01"
    Contoh: generate_kode("MK", 12) -> "MK12"
    """
    return prefix + str(sequence_number).zfill(width)


def sanitize_text(text):
    """Menghilangkan whitespace berlebih dari text."""
    if text is None:
        return ""
    return " ".join(text.split())


def truncate(text, max_length=100, suffix="..."):
    """Memotong text dan menambahkan suffix."""
    if text is None:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def to_snake_case(text):
    """Konversi text ke snake_case."""
    result = []
    for char in text:
        if char.isupper() and result:
            result.append("_")
        result.append(char.lower())
    return "".join(result)
