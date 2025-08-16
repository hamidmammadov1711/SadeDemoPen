from backend.core.security import mask_sensitive

def test_mask_sensitive_fields():
    data = {"username": "admin", "password": "123456", "token": "abc123"}
    masked = mask_sensitive(data)
    assert masked["password"] == "***"
    assert masked["token"] == "***"
    assert masked["username"] == "admin"
