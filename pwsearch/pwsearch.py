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
import sys

# third-party imports
from mediawiki import MediaWiki
from rich.console import Console


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
    parser.add_argument(
        "-k",
        "--keywords",
        help="keywords to search for",
        action="append",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--results",
        type=int,
        help="maximum number of results to show",
        default=20,
    )
    return parser.parse_args()


def main():

    # parse command line arguments
    args = parse_arguments()

    # create MediaWiki instance for PwnWiki
    pwnwiki = MediaWiki(
        url="https://www.pwnwiki.org/api.php",
        user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64",
    )

    # rich console for printing output
    console = Console()

    if args.version:
        sys.exit(0)

    elif args.keywords:
        keywords = ",".join(args.keywords)
        search_results = pwnwiki.opensearch(keywords, results=args.results)

        for page in range(len(search_results)):
            # display = f"https://www.pwnwiki.org/api.php?action=parse&page={urllib.parse.quote_plus(search_results[page][0])}&contentmodel=wikitext&format=json"
            # response = requests.get(display).json()

            console.print(f"Title: {search_results[page][0]}", style="bold cyan")
            console.print(f"URL: {search_results[page][2]}")
            console.print()
