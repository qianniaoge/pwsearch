#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: PWSearch
Author: JustYoomoon
Date Created: May 27, 2021
Last Modified: June 7, 2021

Dev: K4YT3X
Last Modified: Jun 19, 2021
"""

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
from tqdm import tqdm
import requests


# URL to use for looking up page details
PWNWIKI_PAGE_BYTITLE = "https://www.pwnwiki.org/index.php?title={}"
PWNWIKI_API_TITLE = "https://www.pwnwiki.org/api.php?action=parse&page={}&contentmodel=wikitext&format=json"
PWNWIKI_API_PAGEID = "https://www.pwnwiki.org/api.php?action=parse&pageid={}&contentmodel=wikitext&format=json"


class Pwsearch:
    def __init__(self):
        self.pwnwiki = MediaWiki(url="https://www.pwnwiki.org/api.php")

    def search(self, keywords: list, max_results: int = 20) -> Union[list, None]:
        raw_results = self.pwnwiki.opensearch(" ".join(keywords), results=max_results)

        # return None if no results are found
        if len(raw_results) <= 0:
            return None

        results = []
        for result in raw_results:
            results.append({"title": result[0], "url": result[2]})

        return results

    def page(self, pageid: int = None, title: str = None) -> Union[dict, None]:

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
            parsed = page.json()

            if "parse" not in parsed:
                return None

            return parsed["parse"]

        except json.decoder.JSONDecodeError:
            return None


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
                for result in tqdm(results, desc="Searching Database"):
                    page = pwsearch.page(title=result["title"])
                    table.add_row(
                        str(page["pageid"]),
                        page["displaytitle"],
                        result["url"],
                    )

                # print table
                console.print(table)

            else:
                for result in results:
                    console.print(f"Title: {result['title']}", style="bold cyan")
                    console.print(f"URL: {result['url']}")
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
