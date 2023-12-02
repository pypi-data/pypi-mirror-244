from ipaddress import IPv4Address
from typing import Optional, Sequence, Tuple  # for type hinting

from ..._host.server import Server  # for type hinting
from ...constants import UDP_DYNAMIC_PORT_START
from ..nat_resolver import NatResolver
from .port import IPv4Port


class NattedPort(IPv4Port):

    __slots__ = ('_nat_resolver', )

    def __init__(
        self,
        server: Server,
        interface: str = None,
        mac: Optional[str] = None,
        ipv4: Optional[str] = None,
        netmask: Optional[str] = None,
        gateway: Optional[str] = None,
        name: Optional[str] = None,
        tags: Optional[Sequence[str]] = None,
        **kwargs
    ) -> None:
        super().__init__(
            server,
            interface=interface,
            mac=mac,
            ipv4=ipv4,
            netmask=netmask,
            gateway=gateway,
            name=name,
            tags=tags,
            **kwargs
        )
        self._nat_resolver = NatResolver(self)

    @property
    def public_ip(self) -> IPv4Address:
        # TODO - Return ip when public_ip is not (yet) resolved?
        if self._nat_resolver.public_ip:
            return IPv4Address(self._nat_resolver.public_ip)
        # TODO - Resolve NAT when not yet done?
        #      * For example when only performing TCP tests
        #        (NAT is not resolved then via the NatResolver)
        return self.ip

    @property
    def is_natted(self) -> bool:
        return True

    def discover_napt(
        self,
        remote_port: IPv4Port,
        remote_udp_port: int = UDP_DYNAMIC_PORT_START,
        local_udp_port: int = UDP_DYNAMIC_PORT_START
    ) -> Tuple[IPv4Address, int]:
        """
        Resolve the IPv4 address (and/or UDP port) as seen by `remote_port`.

        .. note::
           UDP ports can be left to the default if
           you are only interested in the public IP.
        """
        return self._nat_resolver.resolve(
            remote_port,
            remote_udp_port=remote_udp_port,
            local_udp_port=local_udp_port,
        )
