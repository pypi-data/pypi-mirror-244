from ipaddress import (  # for type hinting
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from typing import Iterable, Optional, Sequence  # for type hinting

from byteblowerll.byteblower import NetworkInterface

from ..._host.meetingpoint import MeetingPoint  # for type hinting
from ...exceptions import AddressSelectionFailed, FeatureNotSupported
from ..natted_endpoint import NattedEndpoint


class IPv6Endpoint(NattedEndpoint):
    """ByteBlower Endpoint interface for IPv6."""

    def __init__(
        self,
        meeting_point: MeetingPoint,
        uuid: str,
        name: Optional[str] = None,
        network_interface: Optional[str] = None,
        **kwargs
    ) -> None:
        """Initialize ByteBlower Endpoint.

        :param network_interface: Network interface used by the endpoint
        :type network_interface: Optional[str]
        """
        super().__init__(meeting_point, uuid, name=name, **kwargs)
        self._network_interface = network_interface

    @property
    def ip(self) -> IPv6Address:
        """Return the Endpoint host IP address."""
        self._network_info.Refresh()
        for address in self._global_addresses:
            return address.ip
        for address in self._link_local_addresses:
            return address.ip
        raise AddressSelectionFailed(
            f'No valid IPv6 address found for {self._network_interface}'
        )

    @property
    def network(self) -> IPv6Network:
        """
        Return the network of the *preferred* IP address.

        .. note::
           Useful for reporting. Furthermore not used
           in traffic generation or analysis.
        """
        raise FeatureNotSupported('Endpoint IPv6 network address')

    @property
    def gateway(self) -> IPv6Address:
        """
        Return the default gateway.

        .. note::
           Useful for reporting. Furthermore not used
           in traffic generation or analysis.
        """
        raise FeatureNotSupported('Endpoint IPv6 network gateway')

    @property
    def _global_addresses(self) -> Iterable[IPv6Interface]:
        """
        Return all available global IPv6 addresses.

        Searches for the traffic interface on the endpoint.

        :return: list if IPv6 global addresses
        :rtype: Iterable[IPv6Interface]
        """
        network_interface_list: Sequence[NetworkInterface] = (
            self._network_info.InterfaceGet()
        )
        for network_interface in network_interface_list:
            if (self._network_interface is None
                    or network_interface.NameGet() == self._network_interface):
                yield from (
                    IPv6Interface(address)
                    for address in network_interface.IPv6GlobalGet()
                )

    @property
    def _link_local_addresses(self) -> Iterable[IPv6Interface]:
        """
        Return all available link-local IPv6 addresses.

        Searches for the traffic interface on the endpoint.

        :return: list if IPv6 link-local addresses
        :rtype: Iterable[IPv6Interface]
        """
        network_interface_list: Sequence[NetworkInterface] = (
            self._network_info.InterfaceGet()
        )
        for network_interface in network_interface_list:
            if (self._network_interface is None
                    or network_interface.NameGet() == self._network_interface):
                yield from (
                    IPv6Interface(address)
                    for address in network_interface.IPv6LinkLocalGet()
                )
