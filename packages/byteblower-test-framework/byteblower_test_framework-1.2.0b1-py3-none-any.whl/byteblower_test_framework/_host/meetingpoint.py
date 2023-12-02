import logging
from datetime import datetime
from typing import List  # for type hinting

from byteblowerll.byteblower import ByteBlower
from byteblowerll.byteblower import \
    MeetingPoint as LLMeetingPoint  # for type hinting
from byteblowerll.byteblower import \
    WirelessEndpoint as LLEndpoint  # for type hinting


class MeetingPoint(object):
    """ByteBlower MeetingPoint interface."""

    def __init__(self, ip_or_host: str) -> None:
        """Connect to the ByteBlower Meeting Point.

        :param ip_or_host: The connection address. This can be
           the hostname or IPv4/IPv6 address of the ByteBlower server.
        :type ip_or_host: str
        """
        self._host_ip = ip_or_host
        bb: ByteBlower = ByteBlower.InstanceGet()
        self._bb_meeting_point: LLMeetingPoint = (
            bb.MeetingPointAdd(self._host_ip)
        )

        # NOTE: We can't use the LLEndpointList() here
        #       because .erase() does not work.
        #       That is required for `release_endpoint()`
        self._endpoint_devices: List[LLEndpoint] = []

    @property
    def info(self) -> str:
        """Return connection address this Meeting Point."""
        return self._host_ip

    def release(self) -> None:
        """
        Release this host related resources used on the ByteBlower system.

        .. warning::
           Releasing resources related to traffic generation and analysis
           should be done *first* via the :meth:`Scenario.release()`
           and/or :meth:`Flow.release()`.

        .. warning::
           Releasing endpoint resources should be done *first*
           via :meth:`Port.release()`.
        """
        try:
            bb_meeting_point = self._bb_meeting_point
            del self._bb_meeting_point
        except AttributeError:
            logging.warning('MeetingPoint: Already destroyed?', exc_info=True)
        else:
            bb_root: ByteBlower = ByteBlower.InstanceGet()
            bb_root.MeetingPointRemove(bb_meeting_point)

    @property
    def timestamp(self) -> datetime:
        """Return the current time on the Meeting Point."""
        ts = self._bb_meeting_point.TimestampGet()
        return datetime.utcfromtimestamp(ts / 1e9)

    def reserve_endpoint(self, uuid: str) -> LLEndpoint:
        """Add device to the list of endpoints used in the test."""
        bb_endpoint: LLEndpoint = self._bb_meeting_point.DeviceGet(uuid)
        self._endpoint_devices.append(bb_endpoint)
        return bb_endpoint

    def release_endpoint(self, endpoint: LLEndpoint) -> None:
        """Release this endpoint resources used on the ByteBlower system.

        Removes this device from the list of endpoints used in the test
        and destroys it on the Meeting Point.

        :param endpoint: Endpoint to release
        :type endpoint: LLEndpoint
        """
        self._endpoint_devices.remove(endpoint)
        self._bb_meeting_point.DeviceDestroy(endpoint)

    @property
    def bb_meeting_point(self) -> LLMeetingPoint:
        """Object from the ByteBlower API."""
        return self._bb_meeting_point
