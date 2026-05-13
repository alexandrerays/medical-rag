from app.safety import get_safety_response, is_medical_advice_request


class TestMedicalAdviceDetection:
    def test_treatment_recommendation_detected(self):
        assert is_medical_advice_request("Should this patient receive treatment A or treatment B?")

    def test_medication_question_detected(self):
        assert is_medical_advice_request("What medication should I take for my headache?")

    def test_diagnosis_request_detected(self):
        assert is_medical_advice_request("Can you diagnose me with these symptoms?")

    def test_prescription_detected(self):
        assert is_medical_advice_request("Can you prescribe something for my pain?")

    def test_drug_question_detected(self):
        assert is_medical_advice_request("What drug should I use for insomnia?")

    def test_regulatory_question_not_triggered(self):
        assert not is_medical_advice_request("What does FDA say about AI/ML-enabled medical devices?")

    def test_governance_question_not_triggered(self):
        assert not is_medical_advice_request("What are common governance practices for AI in healthcare?")

    def test_risk_question_not_triggered(self):
        assert not is_medical_advice_request("What are the main risks when deploying AI in healthcare?")

    def test_patient_in_regulatory_context_not_triggered(self):
        assert not is_medical_advice_request(
            "How should patient data be handled in AI medical device development?"
        )

    def test_validation_question_not_triggered(self):
        assert not is_medical_advice_request(
            "What documentation should a team prepare before validating an AI healthcare product?"
        )


class TestSafetyResponse:
    def test_response_mentions_cannot_provide(self):
        response = get_safety_response()
        assert "cannot provide medical advice" in response.lower()

    def test_response_mentions_alternatives(self):
        response = get_safety_response()
        assert "FDA" in response or "WHO" in response
