import logging
from abc import ABC, abstractmethod
from ipaddress import (  # for type hinting
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network,
)
from itertools import count
from typing import (  # for type hinting
    Iterator,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from byteblowerll.byteblower import DeviceInfo, DeviceStatus, NetworkInfo
from byteblowerll.byteblower import WirelessEndpoint as LLEndpoint

from .._helpers.taggable import Taggable
from .._host.meetingpoint import MeetingPoint
from ..constants import UDP_DYNAMIC_PORT_START
from ..exceptions import FeatureNotSupported
from .port import Port, VlanFlatConfig  # for type hinting

_LOGGER = logging.getLogger(__name__)


class Endpoint(Taggable, ABC):
    """ByteBlower Endpoint interface."""

    _number = count(start=1)

    def __init__(
        self,
        meeting_point: MeetingPoint,
        uuid: str,
        name: Optional[str] = None,
        tags: Optional[Sequence[str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(tags=tags)

        self._meeting_point = meeting_point
        self._uuid = uuid

        self._bb_endpoint: LLEndpoint = self._meeting_point.reserve_endpoint(
            self._uuid
        )
        device_info: DeviceInfo = self._bb_endpoint.DeviceInfoGet()
        self._network_info: NetworkInfo = device_info.NetworkInfoGet()

        # NOTE: Always increment, even with given name
        endpoint_number = next(Endpoint._number)
        if name is not None:
            self._name = name
        else:
            self._name = f'Endpoint {endpoint_number}'

        if kwargs:
            logging.error(
                'Unsupported keyword arguments for %r: %r', self._name, [
                    '{}={!r}'.format(key, value)
                    for key, value in kwargs.items()
                ]
            )
            raise ValueError(
                f'Unsupported configuration parameters for {self._name!r}'
                f' (UUID {self._uuid!r}): {[key for key in kwargs]!r}'
            )

    def release(self) -> None:
        """
        Release this endpoint resources used on the ByteBlower system.

        .. warning::
           Releasing resources related to traffic generation and analysis
           should be done *first* via the :meth:`Scenario.release()`
           and/or :meth:`Flow.release()`.

        .. note::
           The ByteBlower Meeting Point is not released. This should be
           done afterwards via :meth:`MeetingPoint.release()`
        """
        try:
            bb_endpoint = self._bb_endpoint
            del self._bb_endpoint
        except AttributeError:
            logging.warning('Endpoint: Already destroyed?', exc_info=True)
        else:
            self._meeting_point.release_endpoint(bb_endpoint)

    @property
    def meeting_point(self) -> MeetingPoint:
        """Meeting Point object from the ByteBlower Test Framework."""
        return self._meeting_point

    @property
    def bb_endpoint(self) -> LLEndpoint:
        """Endpoint object from the ByteBlower API."""
        return self._bb_endpoint

    @property
    def vlan_config(self) -> Iterator[Sequence[VlanFlatConfig]]:
        """VLAN configurations of the ByteBlower Lower Layer API.

        .. note::
           Currently not supported by the ByteBlower Endpoint.

        :return:
           Ordered collection (Outer -> Inner) of VLAN configuration tuples
        :yield: VLAN configuration for current layer 2.5
        :rtype: Iterator[Sequence[VlanFlatConfig]]
        """
        raise FeatureNotSupported('Endpoint VLAN configuration')

    @property
    def failed(self) -> bool:
        """Return whether (IP) address configuration failed."""
        # TODO - Might be used to return failed IP connectivity
        #      ! on traffic interface of the Endpoint
        #      * Now, it is mainly here to keep the interface consistent with
        #      * the `endpoint.Port` interface.
        #      This property is used for example in the Flow constructor
        #      for sanity checks.
        return False

    @property
    @abstractmethod
    def ip(self) -> Union[IPv4Address, IPv6Address]:
        """
        Return the *preferred* IP address.

        .. note::
           Subject to change in dual stack implementations.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def network(self) -> Union[IPv4Network, IPv6Network]:
        """
        Return the network of the *preferred* IP address.

        .. note::
           Useful for reporting. Furthermore not used
           in traffic generation or analysis.

        .. note::
           Subject to change in dual stack implementations.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def gateway(self) -> Union[IPv4Address, IPv6Address]:
        """
        Return the default gateway.

        .. note::
           Useful for reporting. Furthermore not used
           in traffic generation or analysis.

        .. note::
           Subject to change in dual stack implementations.
        """
        raise NotImplementedError()

    @property
    def is_natted(self) -> bool:
        """
        Return whether this endpoint is behind a NAT gateway.

        .. note::
           Hook function for extending Port implementations.
        """
        return False

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> DeviceStatus:
        """Return this endpoint's current status.

        :return: The Endpoint's current status.
        :rtype: DeviceStatus
        """
        endpoint = self.bb_endpoint
        endpoint.Refresh()
        return endpoint.StatusGet()

    @property
    def active(self) -> bool:
        """Return whether this Endpoint is active.

        :return: Whether this endpoint is active or not.
        :rtype: bool
        """
        endpoint_status = self.status
        return endpoint_status in (
            DeviceStatus.Starting,
            DeviceStatus.Running,
        )

    def discover_napt(
        self,
        remote_port: Port,  # pylint: disable=unused-argument
        remote_udp_port: int = UDP_DYNAMIC_PORT_START,  # pylint: disable=unused-argument
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
        return self.ip, local_udp_port
