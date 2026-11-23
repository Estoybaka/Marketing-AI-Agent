from pathlib import Path

from integration.service import handle_message
import integration.service as service


def fake_extract_information(message):
    lowered = message.casefold()
    return {
        "name": (
            "Ram Sharma"
            if "ram sharma" in lowered
            else "Sita Karki"
            if "sita karki" in lowered
            else None
        ),
        "email": (
            "ram@example.com"
            if "ram@example.com" in lowered
            else "sita@example.com"
            if "sita@example.com" in lowered
            else None
        ),
        "phone": None,
        "need": (
            "Care for elderly mother"
            if "care for" in lowered and "mother" in lowered
            else "Care for elderly father"
            if "care for" in lowered and "father" in lowered
            else None
        ),
        "when_needed": (
            "next week"
            if "next week" in lowered
            else None
        ),
        "urgency": None,
        "source": None,
    }


def test_faq_message_uses_existing_faq_agent():
    result = handle_message(
        "Can I pay from abroad?",
        thread_id="faq-only-test",
    )

    assert result["route"] == "faq"
    assert result["faq"]["faq_id"] == "FAQ1"
    assert result["faq"]["answer"].strip()
    assert result["lead"] is None
    assert result["scheduling_preparation"] is None


def test_lead_message_uses_graph_and_temporary_database(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    database_path = tmp_path / "integration_leads.db"

    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        thread_id="lead-integration-test",
        db_path=database_path,
    )

    assert result["route"] == "lead"
    assert result["faq"] is None
    assert result["lead"]["name"] == "Ram Sharma"
    assert result["lead"]["email"] == "ram@example.com"
    assert result["lead"]["lead_complete"] is True
    assert result["scheduling_preparation"] is None
    assert database_path.exists()


def test_mixed_message_calls_faq_and_lead_agents(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    result = handle_message(
        "Can I pay from abroad? My name is Ram Sharma. "
        "My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        thread_id="mixed-integration-test",
        db_path=tmp_path / "mixed_leads.db",
    )

    assert result["route"] == "both"
    assert result["faq"]["faq_id"] == "FAQ1"
    assert result["lead"]["name"] == "Ram Sharma"
    assert result["lead"]["lead_complete"] is True


def test_empty_message_is_rejected():
    import pytest

    with pytest.raises(ValueError, match="Message must not be empty"):
        handle_message("", thread_id="empty-test")


def test_missing_thread_id_is_rejected():
    import pytest

    with pytest.raises(ValueError, match="thread_id"):
        handle_message("My name is Ram Sharma.", thread_id=" ")


def test_invalid_week1_lead_stops_before_week3(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr(
        service,
        "run_lead_workflow",
        lambda state: SimpleNamespace(
            errors=["Channel is required."],
            lead=None,
        ),
    )

    def fail_if_graph_runs(*args, **kwargs):
        raise AssertionError(
            "Week 3 must not run when Week 1 validation fails."
        )

    monkeypatch.setattr(
        service.lead_graph.graph,
        "invoke",
        fail_if_graph_runs,
    )

    result = handle_message(
        "My name is Ram Sharma.",
        thread_id="invalid-week1-test",
    )

    assert result["route"] == "lead"
    assert result["validation"]["errors"] == ["Channel is required."]
    assert result["validation"]["lead"] is None
    assert result["lead"] is None
    assert result["scheduling_preparation"] is None


def test_lead_persists_across_messages(tmp_path, monkeypatch):
    """A later message should complete the lead saved by an earlier message."""
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    database_path = tmp_path / "multi_message_leads.db"
    thread_id = "multi-message-integration-test"

    first_result = handle_message(
        "My name is Ram Sharma.",
        thread_id=thread_id,
        db_path=database_path,
    )

    assert first_result["route"] == "lead"
    assert first_result["lead"]["name"] == "Ram Sharma"
    assert first_result["lead"]["lead_complete"] is False

    second_result = handle_message(
        "My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        thread_id=thread_id,
        db_path=database_path,
    )

    assert second_result["route"] == "lead"
    assert second_result["lead"]["name"] == "Ram Sharma"
    assert second_result["lead"]["email"] == "ram@example.com"
    assert second_result["lead"]["need"] == "Care for elderly mother"
    assert second_result["lead"]["lead_complete"] is True
    assert database_path.exists()


def test_temporary_database_does_not_modify_production_database(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    production_database = (
        Path(service.REPOSITORY_ROOT)
        / "Week-3"
        / "Day-4"
        / "leads.db"
    )
    before = (
        production_database.stat().st_size,
        production_database.stat().st_mtime_ns,
    )

    handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother.",
        thread_id="production-isolation-test",
        db_path=tmp_path / "isolated_leads.db",
    )

    after = (
        production_database.stat().st_size,
        production_database.stat().st_mtime_ns,
    )

    assert after == before


def test_two_threads_keep_lead_details_separate(
    tmp_path,
    monkeypatch,
):
    """Two conversation threads must not share customer information."""
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    database_path = tmp_path / "separate_threads.db"

    ram_result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother next week.",
        thread_id="separation-ram",
        db_path=database_path,
    )

    sita_result = handle_message(
        "My name is Sita Karki. My email is sita@example.com. "
        "I need care for my elderly father next week.",
        thread_id="separation-sita",
        db_path=database_path,
    )

    assert ram_result["lead"]["name"] == "Ram Sharma"
    assert ram_result["lead"]["email"] == "ram@example.com"
    assert ram_result["lead"]["need"] == "Care for elderly mother"
    assert ram_result["lead"]["when_needed"] == "next week"

    assert sita_result["lead"]["name"] == "Sita Karki"
    assert sita_result["lead"]["email"] == "sita@example.com"
    assert sita_result["lead"]["need"] == "Care for elderly father"
    assert sita_result["lead"]["when_needed"] == "next week"

    assert ram_result["lead"]["lead_id"] != sita_result["lead"]["lead_id"]


def test_service_prepares_scheduling_handoff_for_ready_customer(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother.",
        thread_id="scheduling-ready-test",
        db_path=tmp_path / "scheduling_ready.db",
        requested_date="2026-10-20",
        requested_time="10:00 AM",
        customer_ready=True,
    )

    preparation = result["scheduling_preparation"]

    assert preparation["status"] == "ready_for_handoff"
    assert preparation["missing_fields"] == []
    assert preparation["request"]["name"] == "Ram Sharma"
    assert preparation["request"]["email"] == "ram@example.com"
    assert preparation["request"]["requested_date"] == "2026-10-20"
    assert preparation["request"]["requested_time"] == "10:00 AM"
    assert "booking_confirmed" not in preparation


def test_service_does_not_prepare_handoff_when_customer_is_not_ready(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother.",
        thread_id="scheduling-not-ready-test",
        db_path=tmp_path / "scheduling_not_ready.db",
        requested_date="2026-10-20",
        requested_time="10:00 AM",
        customer_ready=False,
    )

    preparation = result["scheduling_preparation"]

    assert preparation["status"] == "not_ready"
    assert preparation["request"] is None


def test_service_reports_missing_scheduling_details(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    result = handle_message(
        "My name is Ram Sharma. My email is ram@example.com. "
        "I need care for my elderly mother.",
        thread_id="scheduling-missing-details-test",
        db_path=tmp_path / "scheduling_missing.db",
        customer_ready=True,
    )

    preparation = result["scheduling_preparation"]

    assert preparation["status"] == "not_ready"
    assert "requested_date" in preparation["missing_fields"]
    assert "requested_time" in preparation["missing_fields"]
    assert preparation["request"] is None
    
    
def test_service_routes_consent_agreement_to_lead_agent(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    database_path = tmp_path / "consent_agreement.db"
    thread_id = "consent-agreement-integration-test"

    service.lead_graph.save_lead(
        thread_id,
        {
            "name": "Ram Sharma",
            "email": "ram@example.com",
            "need": "Care for elderly mother",
            "when_needed": "next week",
            "contact_consent_asked": True,
        },
        database_path,
    )

    result = handle_message(
        "Yes, please.",
        thread_id=thread_id,
        db_path=database_path,
    )

    saved_lead = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert result["route"] == "lead"
    assert result["faq"] is None
    assert result["lead"]["contact_consent"] is True
    assert saved_lead["contact_consent"] is True        

def test_service_routes_consent_decline_to_lead_agent(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    database_path = tmp_path / "consent_decline.db"
    thread_id = "consent-decline-integration-test"

    service.lead_graph.save_lead(
        thread_id,
        {
            "name": "Ram Sharma",
            "email": "ram@example.com",
            "need": "Care for elderly mother",
            "when_needed": "next week",
            "contact_consent_asked": True,
        },
        database_path,
    )

    result = handle_message(
        "No, thank you.",
        thread_id=thread_id,
        db_path=database_path,
    )

    saved_lead = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert result["route"] == "lead"
    assert result["lead"]["contact_consent"] is False
    assert saved_lead["contact_consent"] is False
    
def test_service_routes_consent_revocation_to_lead_agent(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    database_path = tmp_path / "consent_revocation.db"
    thread_id = "consent-revocation-integration-test"

    service.lead_graph.save_lead(
        thread_id,
        {
            "name": "Ram Sharma",
            "email": "ram@example.com",
            "need": "Care for elderly mother",
            "when_needed": "next week",
            "contact_consent": True,
            "contact_consent_asked": True,
        },
        database_path,
    )

    result = handle_message(
        "No, please don't contact me.",
        thread_id=thread_id,
        db_path=database_path,
    )

    saved_lead = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert result["route"] == "lead"
    assert result["lead"]["contact_consent"] is False
    assert saved_lead["contact_consent"] is False    
    

def test_service_does_not_grant_consent_for_ambiguous_answer(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "consent_ambiguous.db"
    thread_id = "consent-ambiguous-integration-test"

    service.lead_graph.save_lead(
        thread_id,
        {
            "name": "Ram Sharma",
            "email": "ram@example.com",
            "need": "Care for elderly mother",
            "when_needed": "next week",
            "contact_consent_asked": True,
        },
        database_path,
    )

    monkeypatch.setattr(
        service.lead_graph,
        "extract_information",
        fake_extract_information,
    )

    result = handle_message(
        "Maybe later.",
        thread_id=thread_id,
        db_path=database_path,
    )

    saved_lead = service.lead_graph.get_lead(
        thread_id,
        db_path=database_path,
    )

    assert result["route"] == "both"
    assert result["faq"] is not None
    assert result["lead"] is not None
    assert "Please reply yes or no" in result["lead"]["response"]
    assert saved_lead["contact_consent"] is None
    assert saved_lead["contact_consent_asked"] is True
    