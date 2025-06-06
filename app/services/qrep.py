import tensorflow as tf
import numpy as np
import io
import joblib
import pandas as pd
from app.services.qcap import postprocess_qcap
from app.schemas.request import QRepClassifyRequest
from app.schemas.response import QRepReportResponse
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
    if 'item' in df.columns:
        try:
            df['kategory'] = df['item'].apply(
                lambda x: le.inverse_transform(
                    [model.predict(tf.constant([x]), verbose=0).argmax()])[0]
            )
        except Exception as e:
            print(f"Kategori error: {e}")
            df['kategory'] = ""
    else:
        df['kategory'] = ""

    return df


def classify_qrep(req: QRepClassifyRequest) -> QRepReportResponse:
    # Ubah QRepClassifyRequest ke dict yang menyerupai hasil QCap
    fake_qcap_out = {
        "merchant": req.merchant,
        "date": req.date,
        "pembayaran": req.payment_method,
        "menu": [item.dict() for item in req.items],
        "total": {
            "total_price": sum(item.qty * item.price for item in req.items)
        }
    }

    df, meta = postprocess_qcap(fake_qcap_out)

    # Klasifikasikan
    df = classify_items(df, qrep_model, le)

    return QRepReportResponse(
        merchant_name=meta["merchant_name"],
        date=meta["date"],
        payment_method=meta["payment_method"],
        report_period=req.report_period,
        item_list=df.to_dict(orient='records'),
        total_amount=meta["total_amount"]
    )
