from authlib.common.security import generate_token
import urllib.parse
import json
import uuid
import os
import secrets
import hashlib
import base64
import requests
from authlib.oauth2.rfc7636 import create_s256_code_challenge
import authlib.jose as jose
from datetime import datetime, timedelta


class IDPartner:
    SUPPORTED_AUTH_METHODS = [
        "client_secret_basic",
        "tls_client_auth",
        "private_key_jwt",  # For backward compatibility
    ]
    SIGNING_ALG = "PS256"
    ENCRYPTION_ALG = "RSA-OAEP"
    ENCRYPTION_ENC = "A256CBC-HS512"

    def __init__(self, oauth, config):
        if not oauth:
            raise ValueError("OAuth missing.")
        if not config:
            raise ValueError("Config missing.")

        default_config = {
            "account_selector_service_url": "https://auth-api.idpartner.com/oidc-proxy",
            "token_endpoint_auth_method": "client_secret_basic",
            "jwks": None,
            "client_secret": None,
        }

        self.config = {**default_config, **config}

        if (
            self.config.get("token_endpoint_auth_method")
            not in self.SUPPORTED_AUTH_METHODS
        ):
            raise ValueError(
                f"Unsupported token_endpoint_auth_method '{self.config.get('token_endpoint_auth_method')}'. "
                f"It must be one of ({', '.join(self.SUPPORTED_AUTH_METHODS)})"
            )

        client_secret_config = (
            {"client_secret": self.config["client_secret"]}
            if self.config.get("token_endpoint_auth_method") == "client_secret_basic"
            else {}
        )

        jwks_config = (
            {
                "authorization_encrypted_response_alg": self.ENCRYPTION_ALG,
                "authorization_encrypted_response_enc": self.ENCRYPTION_ENC,
                "id_token_encrypted_response_alg": self.ENCRYPTION_ALG,
                "id_token_encrypted_response_enc": self.ENCRYPTION_ENC,
                "request_object_signing_alg": self.SIGNING_ALG,
            }
            if self.config.get("jwks")
            else {}
        )

        self.config = {
            **self.config,
            **{
                "authorization_signed_response_alg": self.SIGNING_ALG,
                "id_token_signed_response_alg": self.SIGNING_ALG,
            },
            **client_secret_config,
            **jwks_config,
        }
        if self.config.get("jwks"):
            self.config["jwks"] = jose.JsonWebKey.import_key_set(self.config["jwks"])
        self.oauth = oauth

    def generate_proofs(self):
        return {
            "state": generate_token(43),
            "nonce": generate_token(43),
            "code_verifier": generate_token(43),
        }

    def jwks(self):
        if not self.config.get("jwks"):
            return {}
        public_jwks = []
        for jwk in self.config.get("jwks").keys:
            public_jwk = jwk.as_dict()
            public_jwk.update({
                "alg": jwk["alg"],
                "use": jwk["use"]
            })
            public_jwks.append(public_jwk)

        return {"keys": public_jwks}

    def get_authorization_url(
        self, query, proofs, scope, extra_authorization_params={}
    ):
        if "iss" not in query:
            return f"{self.config.get('account_selector_service_url')}/auth/select-accounts?client_id={self.config.get('client_id')}&visitor_id={query.get('visitor_id')}&scope={scope}&claims={'+'.join(self._extract_claims(extra_authorization_params.get('claims', [])))}"

        self.config["iss"] = query.get("iss")
        self._init_client(query.get("iss"))

        extra_authorization_params["claims"] = json.dumps(
            extra_authorization_params.get("claims")
        )
        extended_authorization_params = {
            "redirect_uri": self.config.get("redirect_uri"),
            "code_challenge_method": "S256",
            "code_challenge": create_s256_code_challenge(proofs.get("code_verifier")),
            "state": proofs.get("state"),
            "nonce": proofs.get("nonce"),
            "scope": scope,
            "response_type": "code",
            "client_id": self.config.get("client_id"),
            "x-fapi-interaction-id": str(uuid.uuid4()),
            "identity_provider_id": query.get("idp_id"),
            "idpartner_token": query.get("idpartner_token"),
            "response_mode": "jwt",
        }

        pushed_authorization_request_params = extended_authorization_params
        if self.config.get("jwks"):
            pushed_authorization_request_params = {
                "request": self._create_request_object(extended_authorization_params)
            }

        request_uri = self._push_authorization_request(
            pushed_authorization_request_params
        ).get("request_uri")
        return (
            self.oauth_client.server_metadata.get("authorization_endpoint")
            + f"?request_uri={request_uri}"
        )

    def token(self, query, proofs):
        jwt = query.get("response")

        code = self._decode_jwt(jwt).get("code")
        return self.oauth_client.fetch_access_token(
            code=code,
            code_verifier=proofs.get("code_verifier"),
        )

    def userinfo(self, token):
        return self.oauth_client.userinfo(token=token)

    def _decode_jwt(self, jwt):
        if len(jwt.split("."))==5:
            jwe = jose.JsonWebEncryption()
            enc_key = self._get_key_by_use("enc")
            result = jwe.deserialize_compact(jwt, enc_key)
            jwt = result.get("payload").decode("utf-8")
        jwks = self.oauth_client.fetch_jwk_set()
        return jose.jwt.decode(jwt, jwks)

    def _create_request_object(self, params):
        extended_params = {
            **params,
            **{
                "iss": self.config["client_id"],
                "aud": self.config["iss"],
                "exp": int((datetime.now() + timedelta(minutes=1)).timestamp()),
                "iat": int(datetime.now().timestamp()),
                "nbf": int(datetime.now().timestamp()),
            },
        }

        extended_params = {
            **params,
            **{
                "iss": self.config["client_id"],
                "aud": self.config["iss"],
                "exp": int((datetime.now() + timedelta(minutes=1)).timestamp()),
                "iat": int(datetime.now().timestamp()),
                "nbf": int(datetime.now().timestamp()),
            },
        }

        sig_key = self._get_key_by_use("sig")
        return jose.jwt.encode({"alg": sig_key["alg"]}, extended_params, sig_key).decode("utf-8")

    def _get_key_by_use(self, use):
        for key in self.config.get("jwks").keys:
            if key["use"] == use:
                return key

    def _push_authorization_request(self, request_params):
        par_endpoint = self.oauth_client.server_metadata.get(
            "pushed_authorization_request_endpoint"
        )
        credentials = base64.b64encode(
            f"{self.oauth_client.client_id}:{self.oauth_client.client_secret}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        response = requests.post(par_endpoint, data=request_params, headers=headers)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to push authorization request: {response.text}")

    def _extract_claims(self, claims_object):
        if not isinstance(claims_object, dict):
            return []

        userinfo_keys = list(claims_object.get("userinfo", {}).keys())
        id_token_keys = list(claims_object.get("id_token", {}).keys())

        return list(set(userinfo_keys + id_token_keys))

    def _init_client(self, iss):
        self.oauth_client = self.oauth.register(
            name="oauth_client",
            client_id=self.config.get("client_id"),
            client_secret=self.config.get("client_secret"),
            redirect_uri="http://localhost:3001/button/oauth/callback",
            server_metadata_url=f"{iss}/.well-known/openid-configuration",
            client_kwargs={
                "code_challenge_method": "S256",
                "response_mode": "jwt",
                "redirect_uri": self.config.get("redirect_uri"),
            },
        )
        self.oauth_client.load_server_metadata()
