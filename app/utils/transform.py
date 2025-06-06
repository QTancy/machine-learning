import re


def str_to_int(s, locale="US"):
    """
    Mengubah string angka format US/ID menjadi integer.

    Args:
        s (str): String angka, contoh "1,591,600.00" atau "1.591.600,00"
        locale (str): "US" atau "ID", default "US"

    Returns:
        int: Nilai bilangan bulat, desimal akan dibuang
    """
    s = s.strip()

    if locale.upper() == "US":
        # Hapus koma (,) lalu pisahkan dari desimal jika ada
        s_clean = re.sub(r",", "", s).split(".")[0]
    elif locale.upper() == "ID":
        # Hapus titik (.) lalu pisahkan dari desimal jika ada
        s_clean = re.sub(r"\.", "", s).split(",")[0]
    else:
        raise ValueError("locale must be either 'US' or 'ID'")

    return int(s_clean)


def extract_int(s):
    """
    Ekstrak digit pertama dari string dan ubah ke int.

    Args:
        s (str): String input, contoh "1 x", "  3pcs", "4x500ml"

    Returns:
        int: Nilai bilangan bulat pertama yang ditemukan. Jika tidak ada, return 0.
    """
    match = re.search(r"\d+", s)
    return int(match.group()) if match else 0
