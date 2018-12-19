"""HN story printing helpers."""
import datetime
import jinja2
import hnlogger

from hnerror import ShnaError


class HnDisplay:  # pylint: disable=too-few-public-methods
    """HN display helper class."""

    def __init__(self):
        """Initialization work."""
        self._log = hnlogger.get_logger(__name__)
        self._jinja2_env = None
        self._story_template = None

    def _setup(self):
        """Setup Jinja2 template environment."""
        # If setup already done, just return.
        if self._jinja2_env and self._story_template:
            return

        try:
            # Setup Jinja2 environment
            self._jinja2_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader("./templates/", encoding="utf-8"),
                autoescape=jinja2.select_autoescape(["template"])
            )
            # Load the story text template
            self._story_template = self._jinja2_env.get_template("story.template")
        except jinja2.TemplateError as _err:
            raise ShnaError(_err)

    def _print_story(self, story: dict):
        """Print a single story to console."""
        # Convert published time from UTC seconds to human readable.
        pub_time = datetime.datetime.fromtimestamp(story["time"])
        story["time"] = pub_time.strftime("%Y-%m-%d, %H:%M:%S")
        # Use the Jinja2 text template and create story to be printed.
        story_text = self._story_template.render(story=story)
        # Print the story.
        self._log.info(story_text)

    def print_stories(self, stories: list, per_page: int):
        """Print all stories in the list.

        Limit the output to per_page and wait for user input to show more.
        """
        # Perform setup if not done already
        self._setup()

        # Print stories page by page
        for index, story in enumerate(stories):
            if index % per_page == 0 and index:
                continue_key = input("Hit any key to continue or press q to quit\n: ")
                if continue_key.lower() == "q":
                    break
            else:
                self._print_story(story)
