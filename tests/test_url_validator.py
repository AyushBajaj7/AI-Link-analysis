import pytest
from app.utils.url_validator import validate_url


def test_valid_urls():
    assert validate_url("https://example.com") == "https://example.com"
    assert validate_url("https://www.google.com") == "https://www.google.com"


def test_blocked_localhost():
    with pytest.raises(ValueError, match="Access to private, loopback, or non-public addresses is not allowed"):
        validate_url("http://localhost")


def test_blocked_loopback_ip():
    with pytest.raises(ValueError, match="Access to private, loopback, or non-public addresses is not allowed"):
        validate_url("http://127.0.0.1")


def test_blocked_private_ips():
    with pytest.raises(ValueError, match="Access to private, loopback, or non-public addresses is not allowed"):
        validate_url("http://192.168.1.1")
    with pytest.raises(ValueError, match="Access to private, loopback, or non-public addresses is not allowed"):
        validate_url("http://10.0.0.1")


def test_blocked_cloud_metadata():
    with pytest.raises(ValueError, match="Access to private, loopback, or non-public addresses is not allowed"):
        validate_url("http://169.254.169.254")


def test_blocked_credentials():
    with pytest.raises(ValueError, match="URLs containing credentials are not allowed"):
        validate_url("http://user:password@example.com")


def test_unsupported_schemes():
    with pytest.raises(ValueError, match="Only HTTP and HTTPS URLs are allowed"):
        validate_url("ftp://example.com")
    with pytest.raises(ValueError, match="Only HTTP and HTTPS URLs are allowed"):
        validate_url("file:///etc/passwd")


def test_blocked_non_standard_ports():
    with pytest.raises(ValueError, match="Only ports 80 and 443 are allowed"):
        validate_url("http://example.com:8080")
