import tensorflow as tf
import numpy as np
import io
import joblib
import pandas as pd
from app.services.qcap import postprocess_qcap
from app.schemas.response import QRepReportResponse, QRepReportItem, QCapResponse
from app.core.config import QREP_PATH_TO_MODEL, LE_PATH_TO_PKL
import tensorflow as tf
import joblib
import pandas as pd

qrep_model = tf.keras.models.load_model(QREP_PATH_TO_MODEL)
le = joblib.load(LE_PATH_TO_PKL)


def predict_category(text):
    logits = qrep_model.predict(tf.constant([text]), verbose=0)
    idx = tf.argmax(logits[0]).numpy()
    label = le.inverse_transform([idx])[0]
    return label


def classify_items(df: pd.DataFrame, model, le):
    """
    Menambahkan kolom kategori hasil klasifikasi ke DataFrame item.

    Args:
        df (pd.DataFrame): Data menu hasil postprocess_qcap.
        model: Model klasifikasi.
        le: LabelEncoder yang cocok dengan model.

    Returns:
        pd.DataFrame: DataFrame dengan kolom 'kategory' ditambahkan.
    """
    if 'nama' in df.columns:
        try:
            df['kategori'] = df['nama'].apply(
                lambda x: le.inverse_transform(
                    [model.predict(tf.constant([x]), verbose=0).argmax()])[0]
            )
        except Exception as e:
            print(f"Kategori error: {e}")
            df['kategori'] = ""
    else:
        df['kategori'] = ""

    return df



def classify_qrep(qcap_data: QCapResponse) -> QRepReportResponse: 
    """
    Menerima data struk yang sudah diekstrak dan dirapikan oleh QCap,
    lalu melakukan klasifikasi kategori item.
    """
    
    df_items = pd.DataFrame([item.model_dump() for item in qcap_data.item])

   
    if 'nama' not in df_items.columns:
        
        print("Warning: 'nama' column not found in DataFrame from QCapResponse items.")
        df_items['nama'] = '' 


    classified_df = classify_items(df_items, qrep_model, le)

  
    report_item_list = []
    for index, row in classified_df.iterrows():
        report_item_list.append(
            QRepReportItem(
                nama=row.get('nama', ''),
                kuantitas=row.get('kuantitas', 0),
                harga=row.get('harga', 0),
                kategori=row.get('kategori', '') 
            ).model_dump()
        )

    
    return QRepReportResponse(
        toko=qcap_data.toko,
        tanggal=qcap_data.tanggal,
        total_harga=qcap_data.total_harga,
        metode_pembayaran=qcap_data.metode_pembayaran, 
        item=report_item_list,
    )