import unittest
import requests_mock
from flask import Flask
from authlib.integrations.flask_client import OAuth
from idpartner import IDPartner
import json
from unittest.mock import Mock

openid_configuration = {
    "acr_values_supported": ["urn:mace:incommon:iap:silver"],
    "authorization_endpoint": "http://localhost:9001/oidc/auth",
    "claims_parameter_supported": True,
    "claims_supported": [
        "sub",
        "vc.MockBankCredential",
        "payment_details",
        "payment_processing",
        "address",
        "email",
        "birthdate",
        "family_name",
        "given_name",
        "age_over_18",
        "age_over_21",
        "age_over_25",
        "acr",
        "sid",
        "auth_time",
        "iss",
    ],
    "code_challenge_methods_supported": ["S256"],
    "end_session_endpoint": "http://localhost:9001/oidc/session/end",
    "grant_types_supported": ["authorization_code", "refresh_token"],
    "issuer": "http://localhost:9001/oidc",
    "jwks_uri": "http://localhost:9001/oidc/jwks",
    "registration_endpoint": "http://localhost:9001/oidc/reg",
    "authorization_response_iss_parameter_supported": True,
    "response_modes_supported": [
        "form_post",
        "fragment",
        "query",
        "jwt",
        "query.jwt",
        "fragment.jwt",
        "form_post.jwt",
    ],
    "response_types_supported": ["code"],
    "scopes_supported": [
        "openid",
        "offline_access",
        "vc.MockBankCredential",
        "payment_details",
        "payment_processing",
        "address",
        "email",
        "profile",
        "age_over_18",
        "age_over_21",
        "age_over_25",
    ],
    "subject_types_supported": ["public"],
    "token_endpoint_auth_methods_supported": [
        "client_secret_basic",
        "tls_client_auth",
        "private_key_jwt",
    ],
    "token_endpoint_auth_signing_alg_values_supported": ["PS256"],
    "token_endpoint": "http://localhost:9001/oidc/token",
    "id_token_signing_alg_values_supported": ["PS256"],
    "id_token_encryption_alg_values_supported": ["RSA-OAEP"],
    "id_token_encryption_enc_values_supported": ["A256CBC-HS512"],
    "pushed_authorization_request_endpoint": "http://localhost:9001/oidc/request",
    "request_parameter_supported": True,
    "request_uri_parameter_supported": False,
    "request_object_signing_alg_values_supported": ["PS256"],
    "request_object_encryption_alg_values_supported": [
        "A128KW",
        "A256KW",
        "dir",
        "RSA-OAEP",
    ],
    "request_object_encryption_enc_values_supported": [
        "A128CBC-HS256",
        "A128GCM",
        "A256CBC-HS512",
        "A256GCM",
    ],
    "userinfo_endpoint": "http://localhost:9001/oidc/me",
    "payment_details_info_endpoint": "http://localhost:9001/oidc/payment_details",
    "payment_processing_endpoint": "http://localhost:9001/oidc/payment_processing",
    "authorization_signing_alg_values_supported": ["PS256"],
    "authorization_encryption_alg_values_supported": ["RSA-OAEP"],
    "authorization_encryption_enc_values_supported": ["A256CBC-HS512"],
    "introspection_endpoint": "http://localhost:9001/oidc/token/introspection",
    "revocation_endpoint": "http://localhost:9001/oidc/token/revocation",
    "tls_client_certificate_bound_access_tokens": True,
    "claim_types_supported": ["normal"],
    "mtls_endpoint_aliases": {
        "token_endpoint": "undefined/token",
        "introspection_endpoint": "undefined/token/introspection",
        "revocation_endpoint": "undefined/token/revocation",
        "userinfo_endpoint": "undefined/me",
        "pushed_authorization_request_endpoint": "undefined/request",
        "payment_details_info_endpoint": "undefined/payment_details",
        "payment_processing_endpoint": "undefined/payment_processing",
    },
}

oidc_jwks = {
    "keys": [
        {
            "kty": "RSA",
            "use": "sig",
            "kid": "-M_9vqJi0tSYDeXFh3clvZ70ntBosUVT9aqB--2SQiU",
            "alg": "PS256",
            "e": "AQAB",
            "n": "xXGeqFK71mOGUdSSqWr2-DS2oCywcO5TLhLC7QFld-rx6LQ--qmqu7uQgiFO9aFl01MIZF_hs7D1RGX1EmB5odP98vqFVvpBvy3Sse6VZtMccKFtvywNsfWLGRwydzGw9B2s4yWy5ARP2w7fg1X3TnZgtOjtilwvJ1QCXWj3AshXcFj9Mn62z7iPnUcYZCupdyJObaCTcnclLBfUSk4AifkGvyqGplfDpfebLcJWMOUd4mm-Hv2qd9o95WhCfmsEALis8tgxkXTjAUIrS17Fw4-MIEDWFDDEn9bXQkzJ2vYGoKklN5k9_6y3pW95YIX81vvAEiLeRImWI-1q7ka5rw",
        },
        {
            "kty": "RSA",
            "use": "enc",
            "kid": "sG0SskqyiA6IWm0Hb3VhmL8TUqSIx_Mqncb3CJNm63c",
            "alg": "RSA-OAEP",
            "e": "AQAB",
            "n": "4LdgDCzIqIV0q2O42B8rXM7WulYJ3gQWJGpElWI4taXb71jPLhbuVphIggmqFmTejVkKGsOVieZoN8CHBkXQq7JmFXbDLHHzqY9uhIsJbNP6i-xRb-rnNPzNy7Vs5I0tpNByi30zQluyO8z0Q3LYK1gOvxAED3jAWfmpcIO1kjlGRxjWeql3Tt6uc3jbt3mqeTsqb7Y5jnO0ee7oHcncWiQvufcGTaOa7NusfTCAcTpWsxoTD3CbmRaVXW0VERpNkzXPpqls3Jned01oDI9F4LkCn03mD2srNUnMElf0AWT_fJ0ZlelBTmZQhV8Luxyoio9DjJDLKxf67CyrJ6VU3Q",
        },
    ]
}


class TestIDPartner(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.oauth = OAuth(self.app)
        self.config = {
            "client_id": "test-client-id",
            "client_secret": "test-client-secret",
            "redirect_uri": "https://example.com/callback",
            "account_selector_service_url": "https://auth-api.idpartner.com/oidc-proxy",
        }
        self.client = IDPartner(self.oauth, self.config)

    def create_client_with_jwks(self):
        config_with_jwks = self.config.copy()
        config_with_jwks[
            "jwks"
        ] = '{"keys":[{"kty":"RSA","kid":"3eL_LSEgEHCNa45mwU7zZ83SEHvX2MesdKWcP14jQ8s","use":"sig","alg":"PS256","e":"AQAB","n":"0bml-h4oJEkmonIBzKZWKoaEt_jn5exY06RwOY-EB6Xp5RPbnQj8AdEW6tl8XBnpdJzhYMb7dnySzRj--jMxG_K8ZhTjLG68og4sm66H08QhWUey1lCN3vTvni8tCZtc7iPKgXJXTzyIkOse-UVkZwhQngPCh7MWjFcG4UfF97APl8XKcjpyshKakfYSpfbKoFqvRbqlJAKCyiwnVf3Ea-RXjh9spLsd77qTNMJEQt14PJxruYXTHPPubKvTJRqwR_ObxYrFxE5h8UZLFk8QYd6k_qKXdV0h2KNuu-PzmyIq7RmQMTr7M4xWexLzrQ7msnsPFJHncXfUD1-jQMtK5Q","d":"gDpoFuM1W-o16wCVxRC2gk24-9r9voChVtWloCv1Z8-zkFJx5jPGET5MKs9Kz-0v5hK9YjSHL0y_XRM5YrTGA_aH5kpDE7mpL9RGxfESLxIt6a6C07Jw668KiscBXGxXh2rut_K3G0VBool_aJ1a4_wbfmGCIQIIeUoEdN0zV1p84ZfCTpwDbbxfnK83ia6ke_RQmoKBjrUyiciUF6jiZEfb-1Vm7aE2NWU8yhmiZ14VAq0YR3xq0OlE8FxjWpr9Lr1i-5Gy-LDOnMRM4zfvYqC_FsiOQ-wGxAxMme_-tm3B05OIsk_O82YpyxpBZYgHn7AK7xahAQMMLiL2y2viyQ","p":"7UUoo8AKof_cIhRBSwmFhTt7_e8BZ7w0uPCAcSv4DNepCoUoTSNDHuuUmgPEULmQplHwhH-wW7ACVvylSZT4JYq-qwSVr9wJoFAYQDYiJizP73eVnFkfqiv2-xwPQaFONwGGxixuz0r8j16Tpe4iMK8Hy-LYpjucvTp6RrNHgls","q":"4kfZ2710YTnCXUsgga-lZxxDIloJ55iLtRSRizRGyxVCNkH1IMoo6pf59AiPkyk1iWYTx4IS_SkelSPWNtJLnFKmgocYikILsiVVSOoI1vkq9la3FTmJkRNzPfTtFWVf0_e0Ff7dkQxr3XBEZUVS0o9-y_V3k7sMsnfuajjva78","dp":"WFk_J7Izg1z1SA9IvLsf55tdsRFU8Z6H9zE-cmWP6KBJBmzMs-Rkctf_rlWmvPRL41Jxf7TYI1vnkyJiHYMF31zJYH7FigUh5HrOfOJrVtGq350krWIWQ1Q5lAk_uQ1qRVshJxuWa0OdxXjO-6MvQfd6rLWcPFHILEHhFABfqS8","dq":"GMe3kvnfadpSb7cPe0RJ_823iGaF2Sf6fL0g5za1Xf4Y_yof9xRMgMxd4hyh5ILJyx8zoVCcVb8QC1MeXWiQQTFH7NlwlYuADmVKPq7qguhMjSeX6yoe55VStIFDCWnNob_pp9L-XqkWkux9gP2jgU2XnCxoiPQeAtlhcZ6Eka8","qi":"Rh3yHepiLVy2gxHepFp2Yi9qSCULNCySjpDy9eeegEHQMIlH5cdO6Q5UmAtQZwoexWgXhmL8hPcgKumcGq0ZG_EpStIy176-McxtkmpbycY8Bfw6rk1FH2Sfn44oIB2JxUm8yHouh6UMz3e_WeisrmotbeAmH0NtG8DyPkTSgmA"},{"kty":"RSA","kid":"u64VsIB-cxX3NHf1nYn1OtBXmWWQfZZp2BVN1rZL6XU","use":"enc","alg":"RSA-OAEP","e":"AQAB","n":"0CIIQ8dAvOfVE38owR4I03lu1oHmCJz0vSKCRWVyNXSfXwl00eH6JmyDC8sFo2h66iU8vNBauYELoxNf4yT9hXsEcDgJcf9NPW186LSttqqgZ8wSycS7Pn3YTfbzH45R5mH_1zvsKnI8Xwi2DibpOht0bVWStG-EXkAkj6YQdSR1cMQXvtBIetWP6cPx7kG-qzjze3mvtIucnKRnphbW31Bker2Ykur3_ySqXJpCxUx3TchL5-pckTfS9Na6VALIBTLR8dHPq1GJXVgQOCh6GrY7ljIY7ZbkJW2_n1SgyNT49SuxBrPWKiIJW2uIdgMtq3Fp-BFMqJJGaqQ_W2jtAw","d":"x7A_ObhMNnI_jusrkM1eLneNjiUnLRBaB7S6RBam0v7HgYkzGcO0G3V07bWl_Tfa5hdABO_qe5yCK74E-4ub6ZszkO9SsJr_4nXPp_zhxiZCrBOx2v_znmtjQroyXQ5RKbbQnhKR7c-YeJ2E_mL61ZNNyzCVBqUP3NWxvljX5WqQiwsap-RN2ZiCXKrGiC_pG59uS5NSTNqf2cgXy0eSlQqt-7T6ZAZtsCz0I6pUYfHbXa3lIHCCRtTDWoVIoaKUa01FqyBeE04V6DvU9AOZWcK670cXbzhG1kkEk5HHYrQabPrBFXtRaOrApaasGDbZDv4fRW31WnNYLuhllPcQMQ","p":"55y41df36jmE0eQmLtI1jLAq7Adw-AhweUUL-Sklf4GkzCEnJ2wVguiCni8NrFMRiCrM95ntFwT6o1neuG4St3rK5wvE_SOYbLvw2MMnjqLVr4zbbDuLJ-w8-SeqDuFRxHkR6xp8J-YwXeD5N4blceEqU36XHpChcZkzoSWCO68","q":"5gxo1-MeuxMk_-RbS85hWMyQzVOBXGpuUlDpFELB2FxjAaaEN9bDRplWfVwTL-txN24NhFZepd8Bf7NL9nAGmGtTiEWhK5jQZz_WeXA6zRLwcm1v9Hbl516baMQy1cOa5VUyrGTsjVO3Q35j8fpRFa_RK-h3U6_bdDpO3UMyFO0","dp":"TEaZvJseYz3EFxeK15qU1htiV07wDk9BMz7g_ZJmbgJ1EmDMszfuMal-8rdOSnUk7fIihFxl71HNdSRwq85cTZ6b2dFPc4pYdV7Dp69FhLztoJ3D2XYWkvRC9E7yu2nK8uhoVUPopX8yaIhhqr67K3Da7ppfDErXUEEC9swSgrM","dq":"J_XP4HBbTjOtIaYRFcHrtvkRzhjLR7pVH4dedV6DPYoOyKKcJPbxRLouA-iSjKhhKje7sVkvZ7CtGfmTIGOlQaSjBfDSZjhNOyIjp0SPcj_v9HB-GgDtPpt4c2JhUjCAH4YFH10ImiQImXjC861_mDzKIM5oq-jIPhBC0rxxXqE","qi":"exJQqZEtA7p9XxItMAip-OTQ7W6n40xexi8PrJdfEvbrk0aAqO4-ixFyqlQnkwKGQt-IIBgwxjRPwEMMMufd_iLbc0EL1QZN370hSCyqIReGa5qH0W2vvoRf4QfmIiEWumfVWTOb9isCW1nlrPnCkBgGrLxTyZKS_BWwez7eDXQ","enc":"A256CBC-HS512"}]}'
        return IDPartner(self.oauth, config_with_jwks)


class WithRequestMocks(TestIDPartner):
    def mock_oidc_configuration(self, mocker):
        mocker.get(
            "http://localhost:9001/oidc/.well-known/openid-configuration",
            json=openid_configuration,
        )

    def mock_push_authorization_request(
        self,
        mocker,
        request_uri="urn:ietf:params:oauth:request_uri:BfdJw4QAuMr5Ir6a-Uypx",
    ):
        mocker.post(
            "http://localhost:9001/oidc/request",
            json={"expires_in": 60, "request_uri": request_uri},
            status_code=201,
        )

    def mock_oidc_jwks(self, mocker):
        mocker.get(
            "http://localhost:9001/oidc/jwks",
            json=oidc_jwks,
        )

    def mock_token(self, mocker):
        mocker.post(
            "http://localhost:9001/oidc/token",
            json={
                "access_token": "NHtB5NG6woOQSeGn5BQr5qAu6ai8B_edu8S9VpfrAXY",
                "expires_in": 60,
                "id_token": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1NXzl2cUppMHRTWURlWEZoM2Nsdlo3MG50Qm9zVVZUOWFxQi0tMlNRaVUifQ.eyJzdWIiOiIzMmYwOTk4ZmM3MTBjNjhjNzY2MWY3M2QxMmJmMDdlOTg3YTRjYjY4OGIzZGZhNDhhNmVlMjdmOTUyNjJlZTIyIiwiZW1haWwiOiJQaGlsaXBITG92ZXR0QG1pa29tb3Rlc3QuY29tIiwiZmFtaWx5X25hbWUiOiJMb3ZldHQiLCJnaXZlbl9uYW1lIjoiUGhpbGlwIiwibm9uY2UiOiJMYk1SNTBJRXVCQmtOWmpPZFhtcURkV2FXWmVXUUg0emtxblBpV1FjNGR1U2FBV2JlZnB3VE9hLXh4eDYxVEljTXJZcWdzNWhrUVJDN0d5MFB0LVN4USIsImF0X2hhc2giOiJibkFTcEN2M2xNLTZ2dzBHZWd0YW1nIiwiYXVkIjoiRjhXOFpLVWl5UlhfMG5vT0xhOTQzIiwiZXhwIjoxNjk4ODc0MDU5LCJpYXQiOjE2OTg4NzM5OTksImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6OTAwMS9vaWRjIn0.QLySATBZIUYbJ7fNKCsTNypuF34H4TBjNywy-FB2O-QF0NXrSNIhIwGfJ7K_VHQfYXodkqNxUc-rOmNxU053IaEtlV-tTFhrxEshiD5P5UpMtecBhESac_yG621OS-zH-_NrZLhXELdBLEojAISYODdNh3DXv1ivaoWRHQFBALmWotc7MnIFPUdior1-IocKyn-k6b80KEOx5qTfvXIrmELrlWqsFzJA8DNpKqGPcyBzDjLs26zCbS-jRgvg1jk2I6YT9ywYWitqm5XuzQze-e3A1h9_r1U3eTG2BL4jA9l0X6qNOu602MOCP0aTTLALV74mAkcrQB3_lCWpHnOntQ",
                "scope": "openid offline_access email profile birthdate address",
                "token_type": "Bearer",
            },
        )

    def mock_user_info(self, mocker):
        mocker.get(
            "http://localhost:9001/oidc/me",
            json={
                "sub": "32f0998fc710c68c7661f73d12bf07e987a4cb688b3dfa48a6ee27f95262ee22",
                "email": "PhilipHLovett@mikomotest.com",
                "family_name": "Lovett",
                "given_name": "Philip",
            },
        )


class TestInitialization(TestIDPartner):
    def test_initializes_with_config(self):
        self.assertIsInstance(self.client, IDPartner)

    def test_raises_error_if_oauth_missing(self):
        with self.assertRaises(ValueError):
            IDPartner(None, self.config)

    def test_raises_error_if_config_missing(self):
        with self.assertRaises(ValueError):
            IDPartner(Mock(), None)

    def test_raises_error_for_unsupported_auth_method(self):
        config = self.config.copy()
        config["token_endpoint_auth_method"] = "unsupported_method"
        with self.assertRaises(ValueError):
            IDPartner(Mock(), config)

    def test_default_token_endpoint_auth_method(self):
        client = IDPartner(Mock(), self.config)
        self.assertEqual(
            client.config.get("token_endpoint_auth_method"), "client_secret_basic"
        )


class TestGenerateProofs(TestIDPartner):
    def test_generate_proofs(self):
        proofs = self.client.generate_proofs()
        self.assertIn("state", proofs)
        self.assertIn("nonce", proofs)
        self.assertIn("code_verifier", proofs)


class TestGetAuthorizationUrl(WithRequestMocks):
    def test_returns_authorization_url_pointing_to_account_selector(self):
        proofs = self.client.generate_proofs()
        scope = "openid offline_access email profile birthdate address"
        url = self.client.get_authorization_url({}, proofs, scope, {})
        self.assertEqual(
            url,
            "https://auth-api.idpartner.com/oidc-proxy/auth/select-accounts?client_id=test-client-id&visitor_id=None&scope=openid offline_access email profile birthdate address&claims=",
        )

    def test_returns_authorization_url_pointing_to_iss(self):
        with requests_mock.Mocker() as m:
            self.mock_oidc_configuration(m)
            self.mock_push_authorization_request(m)

            proofs = self.client.generate_proofs()
            scope = "openid offline_access email profile birthdate address"
            url = self.client.get_authorization_url(
                {"iss": "http://localhost:9001/oidc"}, proofs, scope, {}
            )
            self.assertEqual(
                url,
                "http://localhost:9001/oidc/auth?request_uri=urn:ietf:params:oauth:request_uri:BfdJw4QAuMr5Ir6a-Uypx",
            )

    def test_returns_authorization_url_pointing_to_iss_using_jwks(self):
        with requests_mock.Mocker() as m:
            self.mock_oidc_configuration(m)
            self.mock_push_authorization_request(m)

            client_with_jwks = self.create_client_with_jwks()
            proofs = client_with_jwks.generate_proofs()
            scope = "openid offline_access email profile birthdate address"
            url = client_with_jwks.get_authorization_url(
                {"iss": "http://localhost:9001/oidc"}, proofs, scope, {}
            )
            self.assertEqual(
                url,
                "http://localhost:9001/oidc/auth?request_uri=urn:ietf:params:oauth:request_uri:BfdJw4QAuMr5Ir6a-Uypx",
            )

            post_request = next(
                (req for req in m.request_history if req.method == "POST"), None
            )
            body = post_request.text.split("=")
            param_name = body[0]
            param_value = body[1]
            self.assertEqual(param_name, "request")
            self.assertEqual(len(param_value.split(".")), 3)


class TestToken(WithRequestMocks):
    def test_exchange_code_from_jws_for_token(self):
        with requests_mock.Mocker() as m:
            self.mock_oidc_configuration(m)
            self.mock_push_authorization_request(m)
            self.mock_oidc_jwks(m)
            self.mock_token(m)

            proofs = self.client.generate_proofs()
            scope = "openid offline_access email profile birthdate address"
            url = self.client.get_authorization_url(
                {"iss": "http://localhost:9001/oidc"}, proofs, scope, {}
            )
            jws_token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1NXzl2cUppMHRTWURlWEZoM2Nsdlo3MG50Qm9zVVZUOWFxQi0tMlNRaVUifQ.eyJjb2RlIjoiVEJvYTlLR1lsU2RPMGZGdnhJMklYV2NnV3diT1VVYlpQNjB6VWh5TkQyVyIsInN0YXRlIjoib3FKYm13eDZuQ1ZDRF9LanQ2cE9kbjZpZTF4R3REY2VlTHRiN0x4azRBYzBIeWxEMzBxd241cGdyYm9rRjBmQW53aVBOT1JPQWk4ZWtGYlhXbHJIU3ciLCJhdWQiOiJGOFc4WktVaXlSWF8wbm9PTGE5NDMiLCJleHAiOjE2OTg4Njc3NDYsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6OTAwMS9vaWRjIn0.XACQeu39-bNTLSW0AKh5IvNnjzQhCsTejvPpYEt-Obcyu6D-Z6hm7r-9q_TM5eRL9S2M2D9TqzOMro_ncZ7GUR4ERUn1sCmHxBE_amSUeecXIifTYonUPnRf3AfzJ3hDyewXQ2nyJt2wVmFe2WXPkJsbFZadZnjJt9hu5TG7QH2wPraZj7JcfERF6kbmu30NzPC-qW8DmzH3B5KpJ74S3WkUSgq0C3S_BHDbzYKjuAnKtrxt92jFlvthYApaLrimNKxjvZCe38Yd8G0kq8EWVi3X4pX2GF9cGc7mheZB88gN_AEWiSgPuUMKOWpEDMu_TDAetZix8sBtUnDFnz7vcg"
            proofs = {"code_verifier": "test_code_verifier"}
            token_response = self.client.token({"response": jws_token}, proofs)
            self.assertIn("access_token", token_response)

    def test_exchange_code_from_jwe_for_token(self):
        with requests_mock.Mocker() as m:
            self.mock_oidc_configuration(m)
            self.mock_push_authorization_request(m)
            self.mock_oidc_jwks(m)
            self.mock_token(m)

            proofs = self.client.generate_proofs()
            scope = "openid offline_access email profile birthdate address"
            url = self.client.get_authorization_url(
                {"iss": "http://localhost:9001/oidc"}, proofs, scope, {}
            )
            jws_token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1NXzl2cUppMHRTWURlWEZoM2Nsdlo3MG50Qm9zVVZUOWFxQi0tMlNRaVUifQ.eyJjb2RlIjoiVEJvYTlLR1lsU2RPMGZGdnhJMklYV2NnV3diT1VVYlpQNjB6VWh5TkQyVyIsInN0YXRlIjoib3FKYm13eDZuQ1ZDRF9LanQ2cE9kbjZpZTF4R3REY2VlTHRiN0x4azRBYzBIeWxEMzBxd241cGdyYm9rRjBmQW53aVBOT1JPQWk4ZWtGYlhXbHJIU3ciLCJhdWQiOiJGOFc4WktVaXlSWF8wbm9PTGE5NDMiLCJleHAiOjE2OTg4Njc3NDYsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6OTAwMS9vaWRjIn0.XACQeu39-bNTLSW0AKh5IvNnjzQhCsTejvPpYEt-Obcyu6D-Z6hm7r-9q_TM5eRL9S2M2D9TqzOMro_ncZ7GUR4ERUn1sCmHxBE_amSUeecXIifTYonUPnRf3AfzJ3hDyewXQ2nyJt2wVmFe2WXPkJsbFZadZnjJt9hu5TG7QH2wPraZj7JcfERF6kbmu30NzPC-qW8DmzH3B5KpJ74S3WkUSgq0C3S_BHDbzYKjuAnKtrxt92jFlvthYApaLrimNKxjvZCe38Yd8G0kq8EWVi3X4pX2GF9cGc7mheZB88gN_AEWiSgPuUMKOWpEDMu_TDAetZix8sBtUnDFnz7vcg"
            proofs = {"code_verifier": "test_code_verifier"}
            token_response = self.client.token({"response": jws_token}, proofs)
            self.assertIn("access_token", token_response)


class TestGetUserInfo(WithRequestMocks):
    def test_retrieve_user_info(self):
        with requests_mock.Mocker() as m:
            self.mock_oidc_configuration(m)
            self.mock_push_authorization_request(m)
            self.mock_oidc_jwks(m)
            self.mock_token(m)
            self.mock_user_info(m)

            proofs = self.client.generate_proofs()
            scope = "openid offline_access email profile birthdate address"
            url = self.client.get_authorization_url(
                {"iss": "http://localhost:9001/oidc"}, proofs, scope, {}
            )
            jws_token = "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1NXzl2cUppMHRTWURlWEZoM2Nsdlo3MG50Qm9zVVZUOWFxQi0tMlNRaVUifQ.eyJjb2RlIjoiVEJvYTlLR1lsU2RPMGZGdnhJMklYV2NnV3diT1VVYlpQNjB6VWh5TkQyVyIsInN0YXRlIjoib3FKYm13eDZuQ1ZDRF9LanQ2cE9kbjZpZTF4R3REY2VlTHRiN0x4azRBYzBIeWxEMzBxd241cGdyYm9rRjBmQW53aVBOT1JPQWk4ZWtGYlhXbHJIU3ciLCJhdWQiOiJGOFc4WktVaXlSWF8wbm9PTGE5NDMiLCJleHAiOjE2OTg4Njc3NDYsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6OTAwMS9vaWRjIn0.XACQeu39-bNTLSW0AKh5IvNnjzQhCsTejvPpYEt-Obcyu6D-Z6hm7r-9q_TM5eRL9S2M2D9TqzOMro_ncZ7GUR4ERUn1sCmHxBE_amSUeecXIifTYonUPnRf3AfzJ3hDyewXQ2nyJt2wVmFe2WXPkJsbFZadZnjJt9hu5TG7QH2wPraZj7JcfERF6kbmu30NzPC-qW8DmzH3B5KpJ74S3WkUSgq0C3S_BHDbzYKjuAnKtrxt92jFlvthYApaLrimNKxjvZCe38Yd8G0kq8EWVi3X4pX2GF9cGc7mheZB88gN_AEWiSgPuUMKOWpEDMu_TDAetZix8sBtUnDFnz7vcg"
            proofs = {"code_verifier": "test_code_verifier"}
            token_response = self.client.token({"response": jws_token}, proofs)
            user_info = self.client.userinfo(token_response)
            self.assertEqual(user_info.get('sub'), "32f0998fc710c68c7661f73d12bf07e987a4cb688b3dfa48a6ee27f95262ee22")
            self.assertEqual(user_info.get('email'), "PhilipHLovett@mikomotest.com")
            self.assertEqual(user_info.get('family_name'), "Lovett")
            self.assertEqual(user_info.get('given_name'), "Philip")

class TestGetPublicJwks(TestIDPartner):
    def test_returns_public_jwks(self):
        client_with_jwks = self.create_client_with_jwks()
        public_jwks = client_with_jwks.jwks()
        self.assertIsInstance(public_jwks, dict)
        for key in public_jwks.get("keys", []):
            self.assertNotIn("d", key)


if __name__ == "__main__":
    unittest.main()
