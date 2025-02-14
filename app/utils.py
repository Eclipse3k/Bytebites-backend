# utils.py
from datetime import datetime, timedelta
from .models import FoodLog, db

def cleanup_old_logs():
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    
    # Deleting records in batches of 100
    while True:
        rows_deleted = db.session.query(FoodLog).filter(FoodLog.log_date < one_month_ago).limit(100).delete(synchronize_session='fetch')
        if not rows_deleted:
            break
        db.session.commit()