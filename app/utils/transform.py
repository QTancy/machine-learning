import re
from datetime import datetime, date
from dateutil.parser import parse as dateutil_parse 



def str_to_int(s, locale="US"):
    """
    Mengubah string angka format US/ID menjadi integer.

    Args:
        s (str): String angka, contoh "1,591,600.00" atau "1.591.600,00"
        locale (str): "US" atau "ID", default "US"

    Returns:
        int: Nilai bilangan bulat, desimal akan dibuang
    """
    s = str(s).strip()
    
    # Kalau string kosong, kasi nilai default 0
    if not s: 
        return 0 

    if locale.upper() == "US":
        # Hapus koma (,) lalu pisahkan dari desimal jika ada
        # Contoh: "1,591,600.00" -> "1591600.00" -> "1591600"
        s_clean = re.sub(r",", "", s).split(".")[0]
    elif locale.upper() == "ID":
        # Hapus titik (.) lalu pisahkan dari desimal jika ada
        # Contoh: "1.591.600,00" -> "1591600,00" -> "1591600"
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


def parse_item_string_fallback(item_string: str, locale="ID"):
    """
    Mencoba mengurai string item tunggal
    menjadi nama, kuantitas, dan harga, ketika Donut gagal memberikan dictionary terstruktur.
    """
    nama = item_string.strip()
    # Nilai Default 
    kuantitas = 1  
    harga = 0      

    
    numeric_parts = re.findall(r'(\d[\d.,]*\d|\d+)', item_string)
    
    if numeric_parts:
        try:
            harga_str = numeric_parts[-1]
            harga = str_to_int(harga_str, locale=locale)
            temp_string = item_string.rsplit(harga_str, 1)[0].strip()
            
           
            qty_match = re.search(r'^(\d+)\s*([xX@]?\s*[\d.,]*[\d]?\s*)?', temp_string)
            if qty_match:
                kuantitas = int(qty_match.group(1))
                
                nama = re.sub(r'^(\d+)\s*([xX@]?\s*[\d.,]*[\d]?\s*)?', '', temp_string, 1).strip()
            else:
                nama = temp_string 
            
            nama = re.sub(r'@[0-9.,]+', '', nama).strip() 

        except Exception as e:
            print(f"Error parsing item string fallback for '{item_string}': {e}. Returning defaults.")
            nama = item_string.strip()
            kuantitas = 0
            harga = 0
    
    return {"nama": nama, "kuantitas": kuantitas, "harga": harga}


def convert_date_string_to_datetime(date_str: str) -> datetime:
    """Konversi string tanggal menjadi objek datetime. Sesuaikan format."""
    if not isinstance(date_str, str) or not date_str.strip():
        print(f"Error: tanggal bukan string: {date_str}, type: {type(date_str)}. Menggunakan datetime.now().")
        return datetime.now() # Fallback jika bukan string
    

    try:
        # Coba format umum seperti YYYY-MM-DD atau DD-MM-YYYY
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            return datetime.strptime(date_str, '%Y-%m-%d')
        elif re.match(r'\d{2}-\d{2}-\d{4}', date_str):
            return datetime.strptime(date_str, '%d-%m-%Y')
        return dateutil_parse(date_str)
    except (ValueError, TypeError):
        print(f"Warning: Could not parse date string '{date_str}'. Using current datetime.")
        return datetime.now()