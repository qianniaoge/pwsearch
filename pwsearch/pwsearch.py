#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: PWSearch
Author: JustYoomoon
Date Created: May 27, 2021
Last Modified: June 7, 2021

Dev: K4YT3X
Last Modified: Jun 20, 2021
"""

# fmt: off
# monkey patch gevent before ssl is imported
from gevent import monkey
monkey.patch_all()
# fmt: on

# built-in imports
from typing import Union
import argparse
import json
import urllib.parse
import webbrowser

# third-party imports
from loguru import logger
from mediawiki import MediaWiki
from rich.console import Console
from rich.table import Table
import grequests
import requests


# URL to use for looking up page details
PWNWIKI_PAGE_BYTITLE = "https://www.pwnwiki.org/index.php?title={}"
PWNWIKI_API_TITLE = "https://www.pwnwiki.org/api.php?action=parse&page={}&contentmodel=wikitext&format=json"
PWNWIKI_API_PAGEID = "https://www.pwnwiki.org/api.php?action=parse&pageid={}&contentmodel=wikitext&format=json"


class Pwsearch:
    """PwnWiki searcher"""

    def __init__(self, url="https://www.pwnwiki.org/api.php"):
        """class initialization function

        Args:
            url (str, optional): PwnWiki API URL. Defaults to "https://www.pwnwiki.org/api.php".
        """
        self.pwnwiki = MediaWiki(url=url)

    def search(self, keywords: list, max_results: int = 20) -> list:
        """search for a series of keywords

        Args:
            keywords (list): keywords to search for
            max_results (int, optional): maximum returning results. Defaults to 20.

        Returns:
            list: a list of results
        """
        if max_results <= 0:
            raise ValueError("max_results must > 0")

        return list(self.pwnwiki.search(" ".join(keywords), results=max_results))

    def page(self, pageid: int = None, title: str = None) -> Union[dict, None]:
        """retrieve detailed information about a single page

        Args:
            pageid (int, optional): MediaWiki pageid. Defaults to None.
            title (str, optional): MediaWiki page title. Defaults to None.

        Raises:
            AttributeError: raised if neither pageid nor title are specified

        Returns:
            Union[dict, None]: None if information retrieval has failed, else dict
        """

        if pageid:
            page = requests.get(PWNWIKI_API_PAGEID.format(pageid))
        elif title:
            page = requests.get(PWNWIKI_API_TITLE.format(urllib.parse.quote(title)))
        else:
            raise AttributeError("either pageid or title has to be specified")

        # if server did not return 2xx
        #   detail retrieval has failed
        if not page.ok:
            return None

        try:
            page_dict = page.json().get("parse")
            if page_dict is None:
                return None

            page_dict["url"] = PWNWIKI_PAGE_BYTITLE.format(
                urllib.parse.quote(page_dict["title"])
            )
            return page_dict
        except json.decoder.JSONDecodeError:
            return None

    def pages(
        self, pageids: list = None, titles: list = None, max_concurrency: int = 10
    ) -> list:
        """asynchronously retrieve detailed information about multiple pages

        Args:
            pageids (list, optional): MediaWiki pageids. Defaults to None.
            titles (list, optional): MediaWiki page titles. Defaults to None.
            max_concurrency (int, optional): maximum number of concurrent requests. Defaults to 10.

        Raises:
            AttributeError: raised when neither pageids nor titles are specified

        Returns:
            list: list of results
        """

        responses = []

        # for both pageids and titles:
        # divide the requests into evenly sized chunks
        # map one chunk at a time
        if pageids:
            for chunk in chunks(pageids, max_concurrency):
                request_set = (
                    grequests.get(PWNWIKI_API_PAGEID.format(p)) for p in chunk
                )
                responses += grequests.map(request_set)
        elif titles:
            for chunk in chunks(titles, max_concurrency):
                request_set = (
                    grequests.get(PWNWIKI_API_TITLE.format(urllib.parse.quote(t)))
                    for t in chunk
                )
                responses += grequests.map(request_set)
        else:
            raise AttributeError("either pageid or title has to be specified")

        # analyze responses and add results into list
        results = []
        for response in responses:
            if response is None or not response.ok:
                results.append(None)
            else:
                try:
                    response_dict = response.json().get("parse")
                    if response_dict is None:
                        results.append(None)
                    else:
                        response_dict["url"] = PWNWIKI_PAGE_BYTITLE.format(
                            urllib.parse.quote(response_dict["title"])
                        )
                        results.append(response_dict)
                except json.decoder.JSONDecodeError:
                    results.append(None)

        return results


def chunks(lst: list, n: int) -> list:
    """yield successive n-sized chunks from lst

    Args:
        lst (list): input list
        n (int): chunk size

    Yields:
        list: evenly split chunks
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def parse_arguments() -> argparse.Namespace:
    """parse command line arguments

    Returns:
        argparse.Namespace: parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        prog="pwsearch", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v",
        "--version",
        help="show program version information and exit",
        action="store_true",
    )
    subparsers = parser.add_subparsers(dest="command")

    # search command
    # searches keywords in the PwnWiki database
    search = subparsers.add_parser("search")
    search.add_argument(
        "keywords",
        help="keywords to search for",
        nargs="*",
    )
    search.add_argument(
        "-m",
        "--max",
        type=int,
        help="maximum number of results to show",
        default=20,
    )
    search.add_argument(
        "-t", "--table", help="display search results in a table", action="store_true"
    )

    # open command
    # opens a given page in browser
    opens = subparsers.add_parser("open")
    opens.add_argument("-p", "--pageid", type=int, help="open page by pageid")
    opens.add_argument("-t", "--title", help="open page by title")

    return parser.parse_args()


def main():

    # parse command line arguments
    args = parse_arguments()

    # rich console for printing output
    console = Console()

    # create new Pwsearch instance
    pwsearch = Pwsearch()

    try:

        if args.command == "search":
            results = pwsearch.search(args.keywords, max_results=args.max)

            if results is None:
                console.print("no search results found", style="bold red")
                return

            if args.table:
                # create table and columns
                table = Table()
                table.add_column("Page ID", style="bold red")
                table.add_column("Title", style="bold cyan")
                table.add_column("URL", style="bold white")

                # add all search results as rows
                pages = pwsearch.pages(titles=results)
                for index in range(len(pages)):
                    page = pages[index]
                    if page is None:
                        table.add_row(
                            "None",
                            results[index],
                            "None",
                        )
                    else:
                        table.add_row(
                            str(page["pageid"]),
                            page["displaytitle"],
                            page["url"],
                        )

                # print table
                console.print(table)

            else:
                pages = pwsearch.pages(titles=results)
                for index in range(len(pages)):
                    page = pages[index]
                    if page is None:
                        console.print(f"Title: {results[index]}", style="bold cyan")
                        console.print("URL: None")
                    else:
                        console.print(
                            f"Title: {page['displaytitle']}", style="bold cyan"
                        )
                        console.print(f"URL: {page['url']}")
                    console.print()

        # open a given page (by pageid/title) in web browser
        elif args.command == "open":
            if args.pageid or args.title:
                webbrowser.open(
                    PWNWIKI_PAGE_BYTITLE.format(
                        urllib.parse.quote(
                            pwsearch.page(pageid=args.pageid, title=args.title)["title"]
                        )
                    ),
                    new=2,
                )
            else:
                logger.critical("neither pageid nor title is provided")

    except Exception:
        console.print_exception()


if __name__ == "__main__":
    main()
