"""Main application entry for shna."""
import PyInquirer

from hnstory import HnStory
from hndisplay import HnDisplay
from hnlogger import setup_logger
from hnerror import ShnaError


def main():
    """Entry function for shna application."""
    setup_logger()

    options = [
        {
            "type": "list",
            "name": "hn_category",
            "message": "Select a HN category:",
            "choices": ["new", "top", "best", "ask", "show", "job"],
        },
        {
            "type": "input",
            "name": "limit",
            "message": "Limit number of results to:",
            "default": "10",
            "validate": lambda _limit: True if _limit.isdigit() else False,
        }
    ]

    hn_story = HnStory()
    hn_display = HnDisplay()

    try:
        while True:
            # Get user choice
            selected = PyInquirer.prompt(options)
            # Get HN stories
            stories = hn_story.get_stories(selected["hn_category"], int(selected["limit"]))
            # Print stories on console
            hn_display.print_stories_summary(stories, 5)
    except KeyError as _err:
        # Ignore KeyError from pressing ctrl + c
        raise ShnaError(_err)


if __name__ == "__main__":
    main()
