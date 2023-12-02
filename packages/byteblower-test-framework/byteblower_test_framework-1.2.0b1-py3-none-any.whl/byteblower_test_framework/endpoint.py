"""ByteBlower traffic endpoint interfaces."""
from ._endpoint.endpoint import Endpoint  # for user convenience type hinting
from ._endpoint.ipv4.endpoint import IPv4Endpoint
from ._endpoint.ipv4.nat import NattedPort
from ._endpoint.ipv4.port import IPv4Port
from ._endpoint.ipv6.endpoint import IPv6Endpoint
from ._endpoint.ipv6.port import IPv6Port
from ._endpoint.natted_endpoint import \
    NattedEndpoint  # for user convenience type hinting
from ._endpoint.port import Port  # for user convenience type hinting
from ._endpoint.port import \
    VlanConfig  # pylint: disable=unused-import; for user convenience

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.endpoint import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
# NOTE
#   Port is only useful for type hinting, but we export it so that we
#   are sure that it is included in the Sphinx documentation properly.
#
__all__ = (
    # ByteBlowerPort base interface:
    Port.__name__,  # Include it for Sphinx documentation
    # ByteBlowerPort interfaces:
    IPv4Port.__name__,
    NattedPort.__name__,
    IPv6Port.__name__,
    # ByteBlower Endpoint interfaces:
    Endpoint.__name__,  # Include it for Sphinx documentation
    NattedEndpoint.__name__,  # Include it for Sphinx documentation
    IPv4Endpoint.__name__,
    IPv6Endpoint.__name__,
)
