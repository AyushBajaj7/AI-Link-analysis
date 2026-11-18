"""URL validation and SSRF (Server-Side Request Forgery) protection utilities."""

import ipaddress
import socket
from urllib.parse import urlparse


class SSRFProtectionError(ValueError):
    """Raised when a URL targets a restricted, private, or internal IP address."""
    pass


class InvalidURLError(ValueError):
    """Raised when a URL format is invalid or unsupported."""
    pass


BLOCKED_HOSTNAMES = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
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


def validate_and_sanitize_url(url: str) -> str:
    """Validate a user-supplied URL and enforce strict SSRF protection.
    
    Checks:
    1. Valid scheme (must be http or https).
    2. Hostname presence and basic format.
    3. Blocked hostnames and internal domain extensions.
    4. DNS resolution to check for loopback, private, link-local, multicast,
       reserved, or cloud metadata IP addresses.
    
    Returns:
        Cleaned, validated URL string.
        
    Raises:
        InvalidURLError: If the URL syntax or scheme is invalid.
        SSRFProtectionError: If the URL targets internal or restricted IP ranges.
    """
    if not url or not isinstance(url, str):
        raise InvalidURLError("A non-empty URL string is required.")

    cleaned_url = url.strip()

    try:
        parsed = urlparse(cleaned_url)
    except Exception as e:
        raise InvalidURLError(f"Malformed URL structure: {str(e)}")

    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise InvalidURLError(
            f"Unsupported URL scheme '{scheme}'. Only 'http' and 'https' are allowed."
        )

    hostname = parsed.hostname
    if not hostname:
        raise InvalidURLError("The URL must include a valid host name.")

    hostname_lower = hostname.lower()

    # Check blocked hostnames and suffixes
    if hostname_lower in BLOCKED_HOSTNAMES:
        raise SSRFProtectionError(
            f"Access to host '{hostname}' is blocked for security reasons."
        )

    for suffix in BLOCKED_SUFFIXES:
        if hostname_lower.endswith(suffix):
            raise SSRFProtectionError(
                f"Access to internal domain ending with '{suffix}' is not permitted."
            )

    # Check if the hostname is a direct IP address
    try:
        direct_ip = ipaddress.ip_address(hostname_lower)
        _verify_ip_is_public(direct_ip)
        return cleaned_url
    except ValueError:
        # Not a raw IP literal; proceed to DNS resolution
        pass

    # Resolve domain to IP addresses via DNS
    try:
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror as e:
        raise InvalidURLError(f"Could not resolve host '{hostname}': {str(e)}")

    if not addr_info:
        raise InvalidURLError(f"No IP addresses found for host '{hostname}'.")

    # Verify every resolved address is safe and publicly routable
    for item in addr_info:
        sockaddr = item[4]
        ip_str = sockaddr[0]
        try:
            resolved_ip = ipaddress.ip_address(ip_str)
            _verify_ip_is_public(resolved_ip)
        except SSRFProtectionError:
            raise
        except Exception as e:
            raise SSRFProtectionError(
                f"Failed to verify security of resolved IP '{ip_str}': {str(e)}"
            )

    return cleaned_url


def _verify_ip_is_public(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> None:
    """Verify that an IP address is a safe, publicly routable address."""
    if ip.is_loopback:
        raise SSRFProtectionError(
            f"Access to loopback address ({ip}) is blocked."
        )
    if ip.is_private:
        raise SSRFProtectionError(
            f"Access to private network address ({ip}) is blocked."
        )
    if ip.is_link_local:
        raise SSRFProtectionError(
            f"Access to link-local address ({ip}) is blocked."
        )
    if ip.is_multicast:
        raise SSRFProtectionError(
            f"Access to multicast address ({ip}) is blocked."
        )
    if ip.is_reserved:
        raise SSRFProtectionError(
            f"Access to reserved address ({ip}) is blocked."
        )
    if ip.is_unspecified:
        raise SSRFProtectionError(
            f"Access to unspecified address ({ip}) is blocked."
        )

    # AWS/GCP/Azure link-local metadata protection (169.254.169.254)
    if str(ip) in ("169.254.169.254", "100.100.100.200"):
        raise SSRFProtectionError(
            f"Access to cloud metadata address ({ip}) is strictly forbidden."
        )
