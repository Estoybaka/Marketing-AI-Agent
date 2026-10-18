import unittest

from integration.router import classify_message


class TestMessageRouting(unittest.TestCase):
    def test_known_faq_routes_to_faq(self):
        self.assertEqual(classify_message("Can I pay from abroad?"), "faq")

    def test_clear_lead_intent_routes_to_lead(self):
        self.assertEqual(
            classify_message(
                "My name is Ram Sharma. I need care for my elderly mother."
            ),
            "lead",
        )

    def test_faq_and_lead_intent_routes_to_both(self):
        self.assertEqual(
            classify_message(
                "Can I pay from abroad? My name is Ram Sharma. "
                "I need care for my mother."
            ),
            "both",
        )

    def test_unsupported_question_still_routes_to_faq_fallback(self):
        self.assertEqual(
            classify_message("Do you provide ambulance services?"),
            "faq",
        )

    def test_faq_about_extra_visits_is_not_lead_intent(self):
        self.assertEqual(
            classify_message("What if my parents need more visits?"),
            "faq",
        )

    def test_empty_message_defaults_to_faq(self):
        self.assertEqual(classify_message(""), "faq")
        self.assertEqual(classify_message("   "), "faq")

    def test_generic_greeting_does_not_start_lead_capture(self):
        self.assertEqual(classify_message("Hello, how are you?"), "faq")

    def test_natural_care_request_routes_to_lead(self):
        self.assertEqual(
            classify_message("Could you arrange support for my father?"),
            "lead",
        )

    def test_natural_care_request_with_faq_routes_to_both(self):
        self.assertEqual(
            classify_message(
                "What are your fees? Could you arrange support for my father?"
            ),
            "both",
        )

    def test_home_care_request_routes_to_lead(self):
        self.assertEqual(
            classify_message("I'm looking for home care for my father."),
            "lead",
        )

    def test_daily_activities_request_routes_to_lead(self):
        self.assertEqual(
            classify_message(
                "Can someone help my mother with daily activities?"
            ),
            "lead",
        )

    def test_elderly_parent_care_request_routes_to_lead(self):
        self.assertEqual(
            classify_message(
                "I'd like to arrange care for my elderly parent."
            ),
            "lead",
        )

    def test_general_service_question_stays_faq(self):
        self.assertEqual(
            classify_message("What care services do you offer?"),
            "faq",
        )

    def test_direct_help_request_for_mother_routes_to_lead(self):
        self.assertEqual(
            classify_message("I need help for my mother."),
            "lead",
        )

    def test_direct_help_request_for_elderly_father_routes_to_lead(self):
        self.assertEqual(
            classify_message("Can you help my elderly father?"),
            "lead",
        )

    def test_service_question_about_parent_stays_faq(self):
        self.assertEqual(
            classify_message("What services do you offer for my mother?"),
            "faq",
        )
        
    
    def test_mother_needs_home_help_routes_to_lead(self):
        self.assertEqual(
            classify_message(
                "My mother needs someone to help her at home."
            ),
            "lead",
        )

    def test_father_needs_daily_support_routes_to_lead(self):
        self.assertEqual(
            classify_message("My father needs daily support."),
            "lead",
        )

    def test_mom_needs_help_at_home_routes_to_lead(self):
        self.assertEqual(
            classify_message("Mom needs help at home."),
            "lead",
        )

    def test_mother_needs_daily_activities_help_routes_to_lead(self):
        self.assertEqual(
            classify_message(
                "My mother needs help with daily activities."
            ),
            "lead",
        )

    def test_fees_question_with_home_care_request_routes_to_both(self):
        self.assertEqual(
            classify_message(
                "What are your fees? My mother needs someone "
                "to help her at home."
            ),
            "both",
        )



if __name__ == "__main__":
    unittest.main()
