import argparse

from ThreadCrawler import ThreadCrawler


def main():
    """
    Parses the command line argument, initializes the class object and starts the crawling
    :return: None
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("target")
    parser.add_argument("--number_of_threads")

    args = parser.parse_args()

    base_url = args.target

    job = ThreadCrawler(args.number_of_threads or 5)

    job.crawl(base_url)


if __name__ == '__main__':
    main()
