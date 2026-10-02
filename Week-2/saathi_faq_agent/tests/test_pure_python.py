
import unittest

from pure_python.faq_agent import answer_question


class TestFAQAgent(unittest.TestCase):

    def test_payment_abroad(self):
        result = answer_question("Can I pay from abroad?")
        self.assertEqual(result["faq_id"], "payment_abroad")

    def test_international_card(self):
        result = answer_question("Do you accept international credit card?")
        self.assertEqual(result["faq_id"], "payment_abroad")

    def test_local_payment(self):
        result = answer_question("Can my parents pay locally?")
        self.assertEqual(result["faq_id"], "local_payment")

    def test_khalti(self):
        result = answer_question("Can I pay with Khalti?")
        self.assertEqual(result["faq_id"], "local_payment")

    def test_joining_fee(self):
        result = answer_question("Is there a setup or joining fee?")
        self.assertEqual(result["faq_id"], "joining_fee")

    def test_hidden_fees(self):
        result = answer_question("Are there any hidden fees?")
        self.assertEqual(result["faq_id"], "joining_fee")

    def test_change_cancel(self):
        result = answer_question("Can I change or cancel the plan?")
        self.assertEqual(result["faq_id"], "change_cancel")

    def test_upgrade(self):
        result = answer_question("Can I upgrade my plan?")
        self.assertEqual(result["faq_id"], "change_cancel")

    def test_additional_visits(self):
        result = answer_question("What if my parents need more visits?")
        self.assertEqual(result["faq_id"], "additional_visits")

    def test_extra_visits(self):
        result = answer_question("Can I book extra visits?")
        self.assertEqual(result["faq_id"], "additional_visits")

    def test_service_area(self):
        result = answer_question("Do you serve outside Kathmandu?")
        self.assertEqual(result["faq_id"], "service_area")

    def test_pokhara(self):
        result = answer_question("Is service available in Pokhara?")
        self.assertEqual(result["faq_id"], "service_area")

    def test_unsupported_question(self):
        result = answer_question("Do you provide ambulance services?")
        self.assertIsNone(result["faq_id"])

    def test_empty_question(self):
        result = answer_question("")
        self.assertIsNone(result["faq_id"])

    def test_answer_is_not_empty(self):
        result = answer_question("Can I pay from abroad?")
        self.assertTrue(result["answer"].strip())


if __name__ == "__main__":
    unittest.main()