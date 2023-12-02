import argparse
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import logging
import sys

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
VERIFY_SSL = True

def search_engines():
    return {
        "google": google_search,
        "duckduckgo": ddg_search,
    }

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Retrieve domain URLs from Search Engines",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "domain",
        nargs="*",
        help="Specify several domain or files. If None then stdin is used"
    )

    parser.add_argument(
        "--max-results",
        help="Max results to retrieve. If 0, then all will be retrieved.",
        default=100,
        type=int
    )

    parser.add_argument(
        "--workers",
        default=5,
        help="Parallel search engines."
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="Verbosity",
        default=0
    )

    parser.add_argument(
        "-k", "--insecure",
        help="Do not check SSL certificate",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "-e", "--engines",
        help="Search engines to use.",
        choices=list(search_engines().keys()),
        nargs="+",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    init_log(args.verbose)
    global VERIFY_SSL
    VERIFY_SSL = not args.insecure


    all_engines = search_engines()
    if not args.engines:
        engines = list(all_engines.values())
    else:
        engines = []
        for engine in args.engines:
            engines.append(all_engines[engine])

    print_lock = Lock()
    try:
        with ThreadPoolExecutor(args.workers) as pool:
            for domain in read_text_targets(args.domain):
                for engine in engines:
                    pool.submit(
                        worker_main,
                        engine,
                        domain,
                        args.max_results,
                        print_lock
                    )
    except (KeyboardInterrupt, BrokenPipeError):
        pass


def worker_main(search_func, domain, max_results, print_lock):
    try:
        for result in search_func("site:{}".format(domain), max_results):
            with print_lock:
                print(result, flush=True)
    except CaptchaError as e:
        logger.error("Captcha in %s", e)
    except (KeyboardInterrupt, BrokenPipeError):
        pass
    except Exception as e:
        logger.warning("Error: %s", e)
        raise e

def google_search(query, max_results):
    logger.info("Start searching in Google for %s", query)
    data = {
        "q": query,
        "start": 0,
    }

    s = requests_session()

    search_params = data
    total_results_count = 0

    while True:
        resp = s.get("https://www.google.com/search", params=search_params)
        soup = BeautifulSoup(resp.text, "html.parser")

        results = list(google_extract_page_results(soup))
        for result in results:
            yield result

        total_results_count += len(results)
        if len(results) == 0 or (max_results and total_results_count >= max_results):
            break

        search_params["start"] += len(results)


def google_extract_page_results(soup):
    for a_soup in soup.find_all("a"):
        if "jsname" in a_soup.attrs:
            children = list(a_soup.children)
            if len(children) and children[0].name == "br":
                yield a_soup["href"]

def ddg_search(query, max_results):
    logger.info("Start searching in Duckduckgo for %s", query)

    data = {
        "q": query,
    }

    s = requests_session()
    search_params = data
    total_results_count = 0
    while True:
        resp = s.post(
            "https://lite.duckduckgo.com/lite/",
            data=search_params,
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        # print(soup)

        results = list(extract_page_results(soup))
        for result in results:
            yield result

        if len(results) == 0:
            if ddg_is_captcha_page(soup):
                raise CaptchaError("Duckduckgo")
            else:
                break

        total_results_count += len(results)
        if max_results and total_results_count >= max_results:
            break

        search_params = extract_next_page_params(soup)

        if not search_params:
            break

def ddg_is_captcha_page(soup):
    return soup.find("div", class_="anomaly-modal__title") is not None

def extract_page_results(soup):
    for a_soup in soup.find_all("a", class_="result-link"):
        yield a_soup["href"]

def extract_next_page_params(soup):
    form_soup = soup.find("form", class_="next_form")
    if not form_soup:
        return {}

    next_data = {}
    for input_soup in form_soup.find_all("input"):
        try:
            name = input_soup["name"]
        except KeyError:
            continue
        next_data[name] = input_soup["value"]


    return next_data

class CaptchaError(Exception):
    pass

def requests_session():
    s = requests.session()
    s.headers.update({"User-Agent": USER_AGENT})
    if not VERIFY_SSL:
        s.verify = False
    return s

def read_text_targets(targets):
    yield from read_text_lines(read_targets(targets))

def read_targets(targets):
    """Function to process the program ouput that allows to read an array
    of strings or lines of a file in a standard way. In case nothing is
    provided, input will be taken from stdin.
    """
    if not targets:
        yield from sys.stdin

    for target in targets:
        try:
            with open(target) as fi:
                yield from fi
        except FileNotFoundError:
            yield target


def read_text_lines(fd):
    """To read lines from a file and skip empty lines or those commented
    (starting by #)
    """
    for line in fd:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue

        yield line

def init_log(verbosity=0, log_file=None):

    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logging.basicConfig(
        level=level,
        filename=log_file,
        format="%(levelname)s:%(name)s:%(message)s"
    )

if __name__ == '__main__':
    exit(main())
