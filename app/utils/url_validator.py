"""URL security validator implementing SSRF protection."""

import ipaddress
import socket
from urllib.parse import urlsplit

BLOCKED_HOSTNAMES = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "metadata.google.internal",
    "instance-data",
}

BLOCKED_SUFFIXES = (
    ".local",
    ".internal",
    ".lan",
    ".home",
    ".corp",
    ".arpa",
    ".localhost",
)


def validate_url(url: str) -> str:
    """Validate that the given URL is a safe public web destination.
    
    Checks:
    - Scheme must be http or https.
    - Hostname must be present.
    - No embedded username or password credentials.
    - Only standard web ports (80, 443) are allowed.
    - Resolved IP addresses must not be private, loopback, link-local,
      multicast, reserved, unspecified, or cloud metadata addresses.
    """
    try:
        parsed = urlsplit(str(url))
        scheme = parsed.scheme.lower()
        if scheme not in ("http", "https"):
            raise ValueError("Only HTTP and HTTPS URLs are allowed")
        if not parsed.hostname:
            raise ValueError("URL must contain a hostname")
        if parsed.username or parsed.password:
            raise ValueError("URLs containing credentials are not allowed")

        port = parsed.port
        if port is not None and port not in (80, 443):
            raise ValueError("Only ports 80 and 443 are allowed")

        host = parsed.hostname.lower()

        # Check explicitly blocked hostnames and suffixes
        if host in BLOCKED_HOSTNAMES:
            raise ValueError("Access to private, loopback, or non-public addresses is not allowed")

        for suffix in BLOCKED_SUFFIXES:
            if host.endswith(suffix):
                raise ValueError("Access to private, loopback, or non-public addresses is not allowed")

        # Resolve IP addresses
        try:
            ip = ipaddress.ip_address(host)
            addresses = [ip]
        except ValueError:
            results = socket.getaddrinfo(
                host,
                port or (443 if scheme == "https" else 80),
                type=socket.SOCK_STREAM,
            )
            addresses = [ipaddress.ip_address(res[4][0]) for res in results]

        for address in addresses:
            if (
                address.is_loopback
                or address.is_private
                or address.is_link_local
                or address.is_multicast
                or address.is_reserved
                or address.is_unspecified
                or str(address) in ("169.254.169.254", "100.100.100.200")
            ):
                raise ValueError(
                    "Access to private, loopback, or non-public addresses is not allowed"
                )

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Could not validate URL destination: {str(e)}")

    return str(url)
