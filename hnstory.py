"""HN story helpers."""
import json
import requests
import hnlogger

from hnerror import ShnaError
from hnapi import APIs


class HnStory:  # pylint: disable=too-few-public-methods
    """HN story related helpers."""

    def __init__(self):
        """Init work."""
        self._log = hnlogger.get_logger(__name__)

    @staticmethod
    def _parse_hn_response(response: requests.Response) -> dict:
        """Validate response from HN API and parse response."""
        if not response.ok:
            raise ShnaError("Error fetching HN stories: {}".format(response.reason))
        return json.loads(response.text)

    def get_stories(self, hn_category: str, limit: int) -> list:
        """Get stories from given category while limiting the output."""
        # Sanity check.
        if hn_category is None or limit <= 0:
            raise ShnaError("Invalid arguments for type and limit")

        # Get the API end point based on the story type.
        hn_api = APIs.END_POINT.get(hn_category, None)
        if hn_api is None:
            raise ShnaError("Invalid story type")

        # Get the IDs of stories we are interested in
        hn_resp = requests.get(hn_api)
        hn_item_ids = self._parse_hn_response(hn_resp)

        hn_items = []

        # API to fetch story details.
        hn_api = APIs.END_POINT.get("_item")

        # Fetch complete story using story ID.
        for item_id in hn_item_ids[:limit]:
            hn_resp = requests.get("{}/{}.json".format(hn_api, item_id))
            hn_item = self._parse_hn_response(hn_resp)
            hn_items.append(hn_item)

        return hn_items
