from app.logging_config import scrub_event
from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_vietnamese_phone_formats() -> None:
    phone_numbers = (
        "0901234567",
        "090 123 4567",
        "090.123.4567",
        "090-123-4567",
        "+84 90 123 4567",
    )

    for phone_number in phone_numbers:
        out = scrub_text(f"Contact: {phone_number}")
        assert phone_number not in out
        assert "REDACTED_PHONE_VN" in out


def test_scrub_passport_and_vietnamese_address() -> None:
    out = scrub_text("Passport A12345678, address số 12 đường Nguyễn Huệ, quận 1")

    assert "A12345678" not in out
    assert "Nguyễn Huệ" not in out
    assert "REDACTED_PASSPORT" in out
    assert "REDACTED_ADDRESS_VN" in out


def test_scrub_event_redacts_context_and_nested_payload_strings() -> None:
    event = scrub_event(
        None,
        "info",
        {
            "event": "request_received",
            "session_id": "student@vinuni.edu.vn",
            "payload": {"context": {"phone": "090 123 4567"}},
        },
    )

    assert event["session_id"] == "[REDACTED_EMAIL]"
    assert event["payload"]["context"]["phone"] == "[REDACTED_PHONE_VN]"
