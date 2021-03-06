import os
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from faunadb.errors import BadRequest


class FaunaWrapper:
    def __init__(self):
        secret = os.getenv("FAUNA_KEY")
        self.client = FaunaClient(secret=secret)
        # initialize faunadb client
        pass

    def get_documents_in_index(self, index="tweets", size=100000):
        """Assume index name exists
        Validation not needed personal script
        unique_halts, unique_news, unique_short_news
        """
        documents = self.client.query(q.paginate(q.match(q.index(index)), size=size))
        return documents

    # Have a faunadb class with a refer to the client
    def create_document_in_collection(self, collection_data, collection="tweets"):
        """Assumes that collection name exists
        collections are halts and news and short_news
        Validation not needed, personal project <3
        """
        try:
            result = self.client.query(
                q.create(q.collection(collection), {"data": collection_data})
            )
            print(result)
            return True
        except BadRequest as error:
            # get properties of bad request
            # print(dir(bad))
            if hasattr(error, "_get_description"):
                if error._get_description() == "document is not unique.":
                    ticker = collection_data.get("ticker")
                    print(f"skipping {ticker} since doc is not unique")
                    return False
            # unknown error, stop everything
        except Exception as error:
            print(collection_data)
            raise Exception(error)