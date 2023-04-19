import os
from time import sleep

from people_analytics_itsm_sdk.sdk.servicenow.attachments.exceptions import (
    DeleteAttachment,
    DownloadAttachment,
    RecordFilterException,
)
from people_analytics_itsm_sdk.sdk.servicenow.helpers.client import Client
from people_analytics_itsm_sdk.sdk.servicenow.helpers.query_builder import QueryBuilder


class BaseAttachmentsAPI:
    default_path = "api/now/attachment"
    http_client = Client()

    def __init__(self) -> None:
        super().__init__()


class Attachment(BaseAttachmentsAPI):
    """Allows you to download attachments files
    Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html
    """

    sysparm_limit = None
    sysparm_offset = None
    query = None
    __file = []

    def __init__(self):
        super().__init__()
        self.query = QueryBuilder()

    def __request_helper(self, data=[], next_link="", retries=5):
        try:
            result = None
            params = self._get_params()
            current_data = []

            if next_link:
                result = self.http_client.get(next_link, params=params)
            else:
                result = self.http_client.get(f"{self.default_path}", params=params)

            if result.status_code != 200:
                text = result.text
                raise RecordFilterException(text)

            if result.headers.get("content-type")[:16] == "application/json":
                current_data = result.json()
                data = data + current_data.get("result")

                if result.links.get("next"):
                    next_link = (
                        result.links.get("next", {})
                        .get("url", "")
                        .replace(f"{os.environ['ITSM_SERVICENOW_URL']}/", "")
                    )
                    data = self.__request_helper(data, next_link=next_link)

            return data
        except Exception as e:
            if retries > 0:
                self.__request_helper(data, next_link=next_link, retries=retries - 1)
                print("Error: " + str(e))
                print("Retry in 30s")
                sleep(30)
            return

    def _get_params(self) -> dict:
        params = {}

        query = None
        if self.query._query:
            query = str(self.query)

        if query:
            params["sysparm_query"] = query

        if self.sysparm_limit != 500:
            params["sysparm_limit"] = self.sysparm_limit

        if self.sysparm_offset:
            params["sysparm_limit"] = self.sysparm_limit

        return params

    def limit(self, limit: int):
        """The maximum number of results returned per page (default: 10000)

        Args:
            limit (int): The maximum number of results returned per page

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_limit = limit
        return self

    def get_files_metadata(self):
        """Returns the metadata for multiple attachments.
        Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html#attachment-GET

        Returns:
            dict: metadata registers result. Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html#d1826795e895
        """
        return self.__request_helper()

    def retrieve_file_metadata(self, sys_id: str):
        """Retrieve a file metadata information
        Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html#attachment-GET-file

        Args:
            sys_id (str, mandatory): Sys_id of the attachment record for which to retrieve the metadata.

        Returns:
            dict: metadata registers result. Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html#attachment-GET-sys_id
        """
        result = self.http_client.get(path=f"{self.default_path}/{sys_id}")

        data = result.json()
        if result.status_code != 200:
            raise DownloadAttachment(data)

        return data.get("result")

    def download_file(self, sys_id: str, folder_path: str = "", file_name: str = None):
        """Download a servicenow file to locally storage.
        Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html#attachment-GET-file

        Args:
            sys_id (str, mandatory): Sys_id of the attachment record from which to return binary data.
            folder_path (str, optional): Folder to store file.
            file_name (str, optional): File name to create locally file. If not defined, the raw name it will be used.

        Returns:
            file_path (str): path of file.
        """
        metadata = self.retrieve_file_metadata(sys_id=sys_id)

        if not file_name:
            file_name = metadata.get("file_name")

        result = self.http_client.get(path=f"{self.default_path}/{sys_id}/file")

        binary = result.content
        if result.status_code != 200:
            raise DownloadAttachment(result.json())

        file_path = f"{folder_path}/{file_name}"

        with open(file=file_path, mode="wb") as f:
            f.write(binary)

        return file_path

    def download_file_buffer(self, sys_id: str):
        """Returns the bytes array of file attachment with a specific sys_id value.
        Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html#attachment-GET-file

        Args:
            sys_id (str, mandatory): Sys_id of the attachment record from which to return binary data.

        Returns:
            bytearray: the file buffer content.
        """
        result = self.http_client.get(path=f"{self.default_path}/{sys_id}/file")

        if result.status_code != 200:
            raise DownloadAttachment(result.json())

        binary = result.content

        return binary

    def delete_file(self, sys_id: str):
        """This method deletes the attachment with a specific sys_id value.
        Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_AttachmentAPI.html#attachment-DELETE

        Args:
            sys_id (str, mandatory): Sys_id value of the attachment to delete.

        Returns:
            dict: metadata of file that has been deleted.
        """
        metadata = self.retrieve_file_metadata(sys_id=sys_id)

        result = self.http_client.delete(path=f"{self.default_path}/{sys_id}")

        if result.status_code != 204:
            raise DeleteAttachment(result.json)

        return metadata
