#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: PWSearch
Author: JustYoomoon
Date Created: May 27, 2021
Last Modified: June 7, 2021

Dev: K4YT3X
Last Modified: Jun 14, 2021
"""

# built-in imports
import argparse
import webbrowser

# third-party imports
from loguru import logger
from mediawiki import MediaWiki
from rich.console import Console
from rich.table import Table
from tqdm import tqdm


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
        "-r",
        "--results",
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

    try:
        # create MediaWiki instance for PwnWiki
        pwnwiki = MediaWiki(
            url="https://www.pwnwiki.org/api.php",
            user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64",
        )

        if args.command == "search":
            keywords = " ".join(args.keywords)
            search_results = pwnwiki.opensearch(keywords, results=args.results)

            if len(search_results) == 0:
                console.print("no search results found", style="bold red")
                return

            if args.table:
                # create table and columns
                table = Table()
                table.add_column("Page ID", style="bold red")
                table.add_column("Title", style="bold cyan")
                table.add_column("URL", style="bold white")

                # add all search results as rows
                for result in tqdm(search_results, desc="Searching Database"):
                    page = pwnwiki.page(result[0])
                    table.add_row(
                        page.pageid,
                        page.title,
                        page.url,
                    )

                # print table
                console.print(table)

            else:
                for result in search_results:
                    console.print(f"Title: {result[0]}", style="bold cyan")
                    console.print(f"URL: {result[2]}")
                    console.print()

        # open a given page (by pageid/title) in web browser
        elif args.command == "open":
            if args.pageid:
                webbrowser.open(pwnwiki.page(pageid=args.pageid).url, new=2)
            elif args.title:
                webbrowser.open(pwnwiki.page(title=args.title).url, new=2)
            else:
                logger.critical("neither pageid nor title is provided")

    except Exception:
        console.print_exception()


if __name__ == "__main__":
    main()
