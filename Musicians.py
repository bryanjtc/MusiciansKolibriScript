#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from socket import gaierror
from urllib3.exceptions import NewConnectionError
from requests.exceptions import ConnectionError

from ricecooker.chefs import SushiChef
from ricecooker.classes.nodes import TopicNode, DocumentNode
from ricecooker.classes.files import DocumentFile
from ricecooker.classes.licenses import get_license


class Musicians(SushiChef):
    channel_info = {
        "CHANNEL_TITLE": "Free Science",
        "CHANNEL_SOURCE_DOMAIN": "https://github.com/EbookFoundation/free-science-books", 
        "CHANNEL_SOURCE_ID": "5435t46456464564554641212",  
        "CHANNEL_LANGUAGE": "en", 
        "CHANNEL_THUMBNAIL": "https://media.visualstories.com/uploads/images/1/5/5235056-1280_624033418-flask-in-scientist-hand-with-laboratory-background_l.jpg",  # (optional)
        "CHANNEL_DESCRIPTION": "Free Science Books",  
    }

    def construct_channel(self, **kwargs):
        channel = self.get_channel(**kwargs)
        science_topic = TopicNode(title="Science!", source_id="<sciences_id>")
        channel.add_child(science_topic)

        url = "https://github.com/EbookFoundation/free-science-books/blob/master/free-science-books.md"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a")

        linkNumber = 0

        for link in links:
            if ".pdf" in link.get("href", []):
                linkNumber += 1
                print("Selecting file: ", linkNumber)

                try:
                    response = requests.get(link.get("href"))
                    print(link.get("href"))
                    document_node = DocumentNode(
                        title="Libro " + str(linkNumber),
                        description="Libro " + str(linkNumber),
                        source_id="libro" + str(linkNumber),
                        license=get_license(
                            "CC BY", copyright_holder="-"
                        ),
                        language="en",
                        files=[
                            DocumentFile(
                                path=link.get("href"),
                                language="en",
                            )
                        ],
                    )
                    science_topic.add_child(document_node)
                except gaierror:
                    print("Connection failed")
                except NewConnectionError:
                    print("Connection failed")
                except ConnectionError:
                    print("Connection failed")

                continue

        return channel


if __name__ == "__main__":
    musicians = Musicians()
    musicians.main()
