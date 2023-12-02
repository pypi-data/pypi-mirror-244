from ipaddress import IPv4Address, IPv4Network  # for type hinting
from typing import Optional  # for type hinting

from ..._host.meetingpoint import MeetingPoint  # for type hinting
from ...exceptions import FeatureNotSupported
from ..natted_endpoint import NattedEndpoint


class IPv4Endpoint(NattedEndpoint):
    """ByteBlower Endpoint interface."""

    def __init__(
        self,
        meeting_point: MeetingPoint,
        uuid: str,
        name: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(meeting_point, uuid, name=name, **kwargs)

    @property
    def ip(self) -> IPv4Address:
        """Return the Endpoint host IP address."""
        # Returns a single IPv4 address instead of a list
        ipv4_address: str = self._network_info.IPv4Get()
        return IPv4Address(ipv4_address)

    @property
    def network(self) -> IPv4Network:
        """
        Return the network of the *preferred* IP address.

        .. note::
           Useful for reporting. Furthermore not used
           in traffic generation or analysis.
        """
        raise FeatureNotSupported('Endpoint IPv4 network address')

    @property
    def gateway(self) -> IPv4Address:
        """
        Return the default gateway.

        .. note::
           Useful for reporting. Furthermore not used
           in traffic generation or analysis.
        """
        raise FeatureNotSupported('Endpoint IPv4 network gateway')
