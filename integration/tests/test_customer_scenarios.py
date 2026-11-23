
import re

import pytest

from integration.service import handle_message
import integration.service as service


def scenario_extractor(message):
    """Deterministic extraction for customer conversation tests."""
    lowered = message.casefold()

    name = None
    if "ram sharma" in lowered:
        name = "Ram Sharma"
    elif "sita karki" in lowered:
        name = "Sita Karki"

    email_match = re.search(
        r"[\w.+-]+@[\w.-]+\.[a-z]{2,}",
        message,
        re.IGNORECASE,
    )
    email = email_match.group(0) if email_match else None

    phone_match = re.search(
        r"\+977[\s-]?\d{10}",
        message,
    )
    phone = phone_match.group(0) if phone_match else None

    need = None
    if "mother" in lowered or "mom" in lowered:
        if "daytime care" in lowered:
            need = "Daytime care for elderly mother"
        elif "personal care" in lowered:
            need = "Personal care for elderly mother"
        elif "daily activities" in lowered:
            need = "Help with daily activities for elderly mother"
            
        elif "care for" in lowered or "care" in lowered:
            need = "Care for elderly mother"    

    elif "father" in lowered or "dad" in lowered:
        if "daytime care" in lowered:
            need = "Daytime care for elderly father"
        elif "daily activities" in lowered:
            need = "Help with daily activities for elderly father"
        elif "care for" in lowered or "care" in lowered:
            need = "Care for elderly father"

    need_is_vague = (
        "some help for my mom" in lowered
        or "some help for my mother" in lowered
        or "book a service" in lowered
    )

    when_needed = (
        "next week"
        if "next week" in lowered
        else None
    )

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "need": need,
        "when_needed": when_needed,
        "urgency": None,
        "source": None,
        "need_is_vague": need_is_vague,
        "need_is_correction": (
            "correction:" in lowered
            or "instead of" in lowered
        )
    }


@pytest.fixture(autouse=True)
def use_scenario_extractor(monkeypatch):
    """Prevent external AI calls during scenario tests."""
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        scenario_extractor,
    )


def test_scenario_01_payment_from_abroad(tmp_path):
    result = handle_message(
        "Can I pay from abroad?",
        "scenario-01",
        db_path=tmp_path / "scenario01.db",
    )

    assert result["route"] == "faq"
    assert result["faq"]["faq_id"] == "FAQ1"
    assert "international credit or debit cards" in (
        result["faq"]["answer"]
    )


def test_scenario_02_local_payment(tmp_path):
    result = handle_message(
        "Can my parents pay locally using Khalti?",
        "scenario-02",
        db_path=tmp_path / "scenario02.db",
    )

    assert result["route"] == "faq"
    assert result["faq"]["faq_id"] == "FAQ2"
    assert "Khalti" in result["faq"]["answer"]


def test_scenario_03_joining_fee(tmp_path):
    result = handle_message(
        "Is there a joining fee?",
        "scenario-03",
        db_path=tmp_path / "scenario03.db",
    )

    assert result["route"] == "faq"
    assert result["faq"]["faq_id"] == "FAQ3"
    assert "no hidden setup or joining fees" in (
        result["faq"]["answer"]
    )


def test_scenario_04_extra_visits(tmp_path):
    result = handle_message(
        "What if my parents need more visits?",
        "scenario-04",
        db_path=tmp_path / "scenario04.db",
    )

    assert result["route"] == "faq"
    assert result["faq"]["faq_id"] == "FAQ5"
    assert "booked individually" in result["faq"]["answer"]


def test_scenario_05_unsupported_exact_price(tmp_path):
    result = handle_message(
        "How much does care cost exactly?",
        "scenario-05",
        db_path=tmp_path / "scenario05.db",
    )

    assert result["route"] == "faq"
    assert result["faq"]["faq_id"] is None
    assert "couldn't find an exact answer" in (
        result["faq"]["answer"]
    )


def test_scenario_06_vague_care_request(tmp_path):
    result = handle_message(
        "I need some help for my mom.",
        "scenario-06",
        db_path=tmp_path / "scenario06.db",
    )

    assert result["route"] == "lead"
    assert result["lead"]["need"] is None
    assert "What kind of care or help do you need?" in (
        result["lead"]["response"]
    )


def test_scenario_07_name_only(tmp_path):
    result = handle_message(
        "My name is Ram Sharma.",
        "scenario-07",
        db_path=tmp_path / "scenario07.db",
    )

    assert result["route"] == "lead"
    assert result["lead"]["name"] == "Ram Sharma"
    assert result["lead"]["lead_complete"] is False
    assert result["lead"]["next_field"] == "email_or_phone"


def test_scenario_08_phone_only(tmp_path):
    database_path = tmp_path / "scenario08.db"
    thread_id = "scenario-08"

    result = handle_message(
        "My phone number is +9779812345678.",
        thread_id,
        db_path=database_path,
    )

    saved = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert result["route"] == "lead"
    assert saved["phone"] == "+9779812345678"
    assert saved["email"] is None
    assert saved["contact_consent"] is None


def test_scenario_09_email_and_care_need(tmp_path):
    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        "scenario-09",
        db_path=tmp_path / "scenario09.db",
    )

    assert result["route"] == "lead"
    assert result["lead"]["name"] == "Ram Sharma"
    assert result["lead"]["email"] == "ram@example.com"
    assert result["lead"]["need"] == "Care for elderly mother"
    assert result["lead"]["when_needed"] == "next week"
    assert result["lead"]["lead_complete"] is True


def test_scenario_10_mother_care_request(tmp_path):
    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need personal care for my elderly mother next week.",
        "scenario-10",
        db_path=tmp_path / "scenario10.db",
    )

    assert result["route"] == "lead"
    assert result["lead"]["need"] == (
        "Personal care for elderly mother"
    )
    assert result["lead"]["contact_consent_asked"] is True


def test_scenario_11_father_care_request(tmp_path):
    result = handle_message(
        "My name is Sita Karki. My email is sita@example.com. "
        "I need care for my elderly father next week.",
        "scenario-11",
        db_path=tmp_path / "scenario11.db",
    )

    assert result["route"] == "lead"
    assert result["lead"]["name"] == "Sita Karki"
    assert result["lead"]["need"] == "Care for elderly father"
    assert result["lead"]["lead_complete"] is True


def test_scenario_12_faq_and_lead_together(tmp_path):
    result = handle_message(
        "Can I pay from abroad? My name is Ram Sharma. "
        "My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        "scenario-12",
        db_path=tmp_path / "scenario12.db",
    )

    assert result["route"] == "both"
    assert result["faq"]["faq_id"] == "FAQ1"
    assert result["lead"]["name"] == "Ram Sharma"
    assert result["lead"]["lead_complete"] is True


def test_scenario_13_information_across_messages(tmp_path):
    database_path = tmp_path / "scenario13.db"
    thread_id = "scenario-13"

    first = handle_message(
        "My name is Ram Sharma.",
        thread_id,
        db_path=database_path,
    )

    second = handle_message(
        "My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        thread_id,
        db_path=database_path,
    )

    saved = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert first["lead"]["name"] == "Ram Sharma"
    assert second["lead"]["name"] == "Ram Sharma"
    assert saved["email"] == "ram@example.com"
    assert saved["need"] == "Care for elderly mother"
    assert saved["when_needed"] == "next week"


def test_scenario_14_customer_declines_follow_up(tmp_path):
    database_path = tmp_path / "scenario14.db"
    thread_id = "scenario-14"

    first = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        thread_id,
        db_path=database_path,
    )

    assert first["lead"]["contact_consent_asked"] is True

    second = handle_message(
        "No, thank you.",
        thread_id,
        db_path=database_path,
    )

    saved = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert second["route"] == "lead"
    assert second["lead"]["contact_consent"] is False
    assert saved["contact_consent"] is False
    assert "will not arrange" in second["lead"]["response"]


def test_scenario_15_scheduling_handoff_not_booking(tmp_path):
    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        "scenario-15",
        db_path=tmp_path / "scenario15.db",
        requested_date="2026-11-10",
        requested_time="10:00 AM",
        customer_ready=True,
    )

    preparation = result["scheduling_preparation"]

    assert preparation["status"] == "ready_for_handoff"
    assert preparation["request"]["requested_date"] == "2026-11-10"
    assert preparation["request"]["requested_time"] == "10:00 AM"
    assert "booking_confirmed" not in preparation
    assert result["lead"]["status"] != "Booked"
    
    
def test_scenario_16_customer_corrects_care_requirement(tmp_path):
    database_path = tmp_path / "scenario16.db"
    thread_id = "scenario-16"

    first = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need overnight care for my elderly mother next week.",
        thread_id,
        db_path=database_path,
    )

    second = handle_message(
        "Correction: my elderly mother needs daytime care"
        " instead of overnight care.",
        thread_id,
        db_path=database_path,
    )

    saved = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert first["lead"]["need"] == "Care for elderly mother"
    assert second["route"] == "lead"
    assert saved["need"] == "Daytime care for elderly mother"
    assert "Overnight care" not in saved["need"]


def test_scenario_17_customer_adds_care_requirement(tmp_path):
    database_path = tmp_path / "scenario17.db"
    thread_id = "scenario-17"

    first = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need personal care for my elderly mother next week.",
        thread_id,
        db_path=database_path,
    )

    second = handle_message(
        "My elderly mother also needs help with daily activities.",
        thread_id,
        db_path=database_path,
    )

    saved = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert first["lead"]["need"] == "Personal care for elderly mother"
    assert second["route"] == "lead"
    assert "Personal care for elderly mother" in saved["need"]
    assert "Help with daily activities for elderly mother" in (
        saved["need"]
    )    

def test_scenario_18_customer_refuses_phone_but_provides_email(
    tmp_path,
):
    database_path = tmp_path / "scenario18.db"
    thread_id = "scenario-18"

    result = handle_message(
        "My name is Ram Sharma. I don't want to share my "
        "phone number. My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        thread_id,
        db_path=database_path,
    )

    saved = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert result["route"] == "lead"
    assert saved["email"] == "ram@example.com"
    assert saved["phone"] is None
    assert result["lead"]["lead_complete"] is True
    assert saved["contact_consent_asked"] is True
    assert saved["contact_consent"] is None
    
    
def test_scenario_19_customer_is_not_ready_for_scheduling(tmp_path):
    database_path = tmp_path / "scenario19.db"

    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        "scenario-19",
        db_path=database_path,
        requested_date="2026-11-10",
        requested_time="10:00 AM",
        customer_ready=False,
    )

    preparation = result["scheduling_preparation"]

    assert preparation["status"] == "not_ready"
    assert preparation["missing_fields"] == []
    assert preparation["request"] is None
    assert result["lead"]["status"] != "Booked"    
    
def test_scenario_20_customer_asks_about_service_in_pokhara():
    result = handle_message(
        "Do you provide care services in Pokhara?",
        "scenario-20",
    )

    assert result["route"] == "faq"
    assert result["faq"] is not None
    assert result["faq"]["faq_id"] is not None
    assert "contact" in result["faq"]["answer"].lower()
    assert result["lead"] is None    