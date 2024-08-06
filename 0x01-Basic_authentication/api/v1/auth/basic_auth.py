#!/usr/bin/env python3
""" Basic Authentication module """

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication class inheriting from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract Base64 part from Authorization header."""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Strip off the "Basic " prefix (6 chars) and return remaining part
        return authorization_header[6:]
