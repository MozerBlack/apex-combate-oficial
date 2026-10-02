import unittest

from apex_db import hash_password, normalize_birth_date, normalize_document, verify_password
from server import decode_jwt, issue_jwt


class NormalizationTests(unittest.TestCase):
    def test_document_accepts_formatted_cpf(self):
        self.assertEqual(normalize_document("529.982.247-25"), "52998224725")

    def test_document_accepts_passport(self):
        self.assertEqual(normalize_document("br a-123 456"), "BRA123456")

    def test_birth_date_accepts_supported_formats(self):
        expected = "1998-05-10"
        for value in ("1998-05-10", "10/05/1998", "10-05-1998", "1998/05/10", "10051998"):
            with self.subTest(value=value):
                self.assertEqual(normalize_birth_date(value), expected)


class AuthenticationPrimitiveTests(unittest.TestCase):
    def test_password_hash_is_salted_and_verifiable(self):
        first = hash_password("Senha-Forte-2026")
        second = hash_password("Senha-Forte-2026")
        self.assertNotEqual(first, second)
        self.assertTrue(verify_password("Senha-Forte-2026", first))
        self.assertFalse(verify_password("senha-errada", first))

    def test_jwt_round_trip_preserves_profile_and_permissions(self):
        token = issue_jwt("AC-TEST", "atleta", "ATHLETE", extra={"athlete_id": 99})
        payload = decode_jwt(token)
        self.assertEqual(payload["sub"], "AC-TEST")
        self.assertEqual(payload["perfil"], "atleta")
        self.assertEqual(payload["athlete_id"], 99)
        self.assertIn("ATHLETE_READ", payload["permissions"])


if __name__ == "__main__":
    unittest.main()
