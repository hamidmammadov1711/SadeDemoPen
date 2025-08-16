# Frontend developer üçün təqdimat

## 1. API sənədləri
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: backend/openapi.json

## 2. Backend işə salmaq
- Python 3.13 və virtual environment istifadə edin
- `pip install -r requirements.txt`
- `uvicorn backend.main:app --reload`

## 3. Demo istifadəçi və test dataları
- Demo user, lab, challenge və s. üçün endpointlər mövcuddur

## 4. Database
- Hazırda SQLite (test.db) istifadə olunur
- SQLAlchemy ORM modelləri və Alembic migration dəstəyi var
- Alembic migration üçün: `alembic upgrade head`

## 5. Əsas endpointlər
- /login, /register, /run-test, /report, /lab, /ctf, /notifications və s.
- Multi-language dəstəyi: lang parametri ilə (az, en, ru, tr)

## 6. Docker dəstəyi
- Dockerfile mövcuddur (istəyə görə)

## 7. Əlavə məlumat
- Əlavə sual və ya inteqrasiya üçün backend developer ilə əlaqə saxlayın
