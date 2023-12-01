from bs4 import BeautifulSoup
from uk_bin_collection.uk_bin_collection.common import *
from uk_bin_collection.uk_bin_collection.get_bin_data import \
    AbstractGetBinDataClass


# import the wonderful Beautiful Soup and the URL grabber
class CouncilClass(AbstractGetBinDataClass):
    """
    Concrete classes have to implement all abstract operations of the
    base class. They can also override some operations with a default
    implementation.
    """

    def parse_data(self, page: str, **kwargs) -> dict:
        # Make a BS4 object
        soup = BeautifulSoup(page.text, features="html.parser")
        soup.prettify()

        data = {"bins": []}

        for bins in soup.find_all("ul", {"class": "refuse"}):
            binCollection = bins.find_all("li")

            if binCollection:
                for bin in binCollection:
                    collection_date = bin.find("strong", {"class": "date"}).contents[0].strip()
                    if collection_date.lower() == "today":
                        collection_date = datetime.now()
                    else:
                        collection_date = datetime.strptime(
                            remove_ordinal_indicator_from_date_string(collection_date).strip(),
                            "%a %d %b"
                        )
                    dict_data = {
                        "type": bin.find("a").contents[0],
                        "collectionDate": collection_date.strftime(date_format)
                    }

                    data["bins"].append(dict_data)

        return data
