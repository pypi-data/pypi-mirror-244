from ipaddress import IPv4Address, IPv6Address, ip_address  # for type hinting
from typing import Optional, Tuple, Union  # for type hinting

from byteblower_test_framework._host.meetingpoint import MeetingPoint

from .._endpoint.endpoint import Endpoint
from .._endpoint.port import Port
from ..constants import UDP_DYNAMIC_PORT_START
from .nat_resolver import NatResolver


class NattedEndpoint(Endpoint):

    def __init__(
        self,
        meeting_point: MeetingPoint,
        uuid: str,
        name: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(meeting_point, uuid, name=name, **kwargs)
        self._nat_resolver = NatResolver(self)

    @property
    def is_natted(self) -> bool:
        """Return whether this endpoint is behind a NAT gateway."""
        return True

    @property
    def public_ip(self) -> Union[IPv4Address, IPv6Address]:
        # TODO - Return ip when public_ip is not (yet) resolved?
        if self._nat_resolver.public_ip:
            return ip_address(self._nat_resolver.public_ip)
        # TODO - Resolve NAT when not yet done?
        #      * For example when only performing TCP tests
        #        (NAT is not resolved then via the NatResolver)
        return self.ip

    def discover_napt(
        self,
        remote_port: Port,
        remote_udp_port: int = UDP_DYNAMIC_PORT_START,
        local_udp_port: int = UDP_DYNAMIC_PORT_START
    ) -> Tuple[Union[IPv4Address, IPv6Address], int]:
        """
        Resolve the IP address (and/or UDP port) as seen by `remote_port`.

        This will resolve either the IP address of the endpoint
        or the public IP address of the (IPv4 NAT) gateway when
        the endpoint is using IPv4 and is located behind a NAT
        gateway.

        .. note::
           UDP ports can be left to the default if
           you are only interested in the public IP.
        """
        return self._nat_resolver.resolve(
            remote_port,
            remote_udp_port=remote_udp_port,
            local_udp_port=local_udp_port
        )
