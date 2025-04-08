import httpx
import random
import string

from errors import EmailServiceError


class EmailClient:
    """Client for interacting with the mail.tm API to create temporary email accounts."""

    API = "https://api.mail.tm"
    GET_DOMAINS = "/domains"
    POST_CREATE_ACCOUNT = "/accounts"
    POST_CREATE_TOKEN = "/token"
    GET_MESSAGES = "/messages"

    def __init__(
        self,
        email_address: str | None = None,
        password: str = "password",
        token: str | None = None,
    ):
        """Initialize the EmailClient with optional email address, password, and token."""
        self.client = httpx.AsyncClient(
            base_url=self.API,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        self.email_address = email_address
        self.password = password
        self.token = token

    async def generate_email_address(self) -> str:
        """Generates a random temporary email address."""
        username = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        response = await self.client.get(self.GET_DOMAINS)

        if response.status_code != 200:
            raise EmailServiceError(
                message="Failed to fetch domains",
                debug=f"expected_status_code=200, current_status_code={response.status_code}",
            )

        domains = response.json().get("hydra:member", [])
        if not domains:
            raise EmailServiceError(message="No available domains found.")

        allow_domain = domains[0]["domain"]
        self.email_address = f"{username}@{allow_domain}"
        return self.email_address

    async def create_email(self) -> dict:
        """Creates a temporary email account and returns the response JSON."""
        if not self.email_address:
            self.email_address = await self.generate_email_address()

        response = await self.client.post(
            self.POST_CREATE_ACCOUNT,
            json={"address": self.email_address, "password": self.password},
        )
        if response.status_code != 201:
            raise EmailServiceError(
                message="Failed to create account",
                debug=f"expected_status_code=201, current_status_code={response.status_code}",
            )

        return response.json()

    async def get_token(self) -> str:
        """Authenticates the email account and retrieves an access token."""
        if not self.email_address:
            raise EmailServiceError(message="Email address is required to get a token.")

        response = await self.client.post(
            self.POST_CREATE_TOKEN,
            json={"address": self.email_address, "password": self.password},
        )

        if response.status_code != 200:
            raise EmailServiceError(
                message="Failed to get token",
                debug=f"expected_status_code=200, current_status_code={response.status_code}",
            )

        self.token = response.json().get("token")
        if not self.token:
            raise EmailServiceError(message="Token not found in response.")

        return self.token

    async def get_emails(self) -> list[str]:
        """Retrieves the list of email messages for the account."""
        if not self.token:
            raise EmailServiceError(
                message="Authentication token is required to fetch emails."
            )

        response = await self.client.get(
            self.GET_MESSAGES, headers={"Authorization": f"Bearer {self.token}"}
        )

        if response.status_code != 200:
            raise EmailServiceError(
                message="Failed to get messages",
                debug=f"expected_status_code=200, current_status_code={response.status_code}",
            )
        messages = [
            message["intro"] for message in response.json().get("hydra:member", [])
        ]
        return messages

    async def close(self) -> None:
        """Closes the HTTPX client session."""
        await self.client.aclose()

    async def __aenter__(self):
        """Allows using 'async with EmailClient()' to automatically manage resources."""
        if not self.email_address:
            await self.generate_email_address()
            await self.create_email()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the HTTP client session when exiting the context."""
        await self.close()
