import os
from time import sleep

from service_now_api_sdk.sdk.servicenow.helpers.client import Client
from service_now_api_sdk.sdk.servicenow.helpers.query_builder import QueryBuilder
from service_now_api_sdk.sdk.servicenow.table.exceptions import (
    ManagerRetriveException,
    RecordFilterException,
    RecordRetriesException,
)


class BaseTableAPI:
    def __init__(self, table: str) -> None:
        self.default_path = "api/now/table"
        self.http_client = Client()
        self.sysparm_display_value = False
        self.sysparm_exclude_reference_link = False
        self.sysparm_fields = None
        self.sysparm_query_no_domain = False
        self.sysparm_view = ""
        self.table = table

    def view(self, view: str):
        """Render the response according to the specified UI view (overridden by sysparm_fields)

        Args:
            view (srtr): Specify UI view

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_view = view
        return self

    def exclude_reference_link(self, exclude: bool):
        """Exclude Table API links for reference fields (default: false)

        Args:
            exclude (bool): True to exclude Table API links for reference fields (default: false)

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_exclude_reference_link = exclude
        return self

    def display_value(self, display: str):
        """Return field display values (true), actual values (false), or both (all) (default: false).

        Args:
            display (str): Return field display values (default: false).

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_display_value = display
        return self

    def query_no_domain(self, no_domain: bool):
        """True to access data across domains if authorized (default: false)

        Args:
            no_domain (bool): Access data across domains if authorized (default: false)

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_query_no_domain = no_domain
        return self

    def only(self, fields: list):
        """List of fields to return in the response

        Args:
            fields (list): List of fields to return in the response

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_fields = ",".join(fields)
        return self

    def _get_params(self) -> dict:
        params = {}

        if self.sysparm_fields:
            params["sysparm_fields"] = self.sysparm_fields

        if self.sysparm_display_value:
            params["sysparm_display_value"] = self.sysparm_display_value

        if self.sysparm_exclude_reference_link:
            params["sysparm_exclude_reference_link"] = (
                self.sysparm_exclude_reference_link
            )

        if self.sysparm_view:
            params["sysparm_view"] = self.sysparm_view

        if self.sysparm_query_no_domain:
            params["sysparm_query_no_domain"] = self.sysparm_query_no_domain

        return params


class Records(BaseTableAPI):
    """Allows you to perform queries on existing tables
    Ref. link: https://docs.servicenow.com/bundle/quebec-application-development/page/integrate/inbound-rest/concept/c_TableAPI.html
    """

    def __init__(self, table: str):
        super().__init__(table=table)
        self.sysparm_limit: int = 500
        self.sysparm_offset: int = None
        self.sysparm_suppress_pagination_header: bool = False
        self.sysparm_query_category = None
        self.sysparm_no_count: bool = False
        self.sysparm_count: bool = False
        self.response_timeout: int = 300
        self.total_registers_sequence_request: int = 0
        self.next_link_sequence_request: str = None
        self.data = []
        self.query = QueryBuilder()

    def suppress_pagination_header(self, supress: bool):
        """Supress pagination header (default: false)

        Args:
            supress (bool): True to supress pagination header (default: false)

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_suppress_pagination_header = supress
        return self

    def limit(self, limit: int):
        """The maximum number of results returned per page (default: 10000)

        Args:
            limit (int): The maximum number of results returned per page

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_limit = limit
        return self

    def offset(self, offset: int = 500):
        """The index of results returned per page (default: 500)

        Args:
            offset (int): The index of results returned per page

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_offset = offset
        return self

    def query_category(self, category: str):
        """Name of the query category (read replica category) to use for queries

        Args:
            view (srtr): Specify UI view

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_query_category = category
        return self

    def no_count(self, no_count: bool):
        """Do not execute a select count(*) on table (default: false)

        Args:
            no_domain (bool): True to execute a select count(*) on table (default: false)

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_no_count = no_count
        return self

    def count(self, count: bool):
        """Do not execute a select count(*) on table (default: false)

        Args:
            count (bool): True to execute a select count(*) on table (default: false)

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_count = count
        return self

    def timeout(self, timeout: int):
        """Time to get error on try request data (default: 300)

        Args:
            timeout (bool): time to get error on try request data (default: 300)

        Returns:
            TableAPI: Return self class
        """
        self.response_timeout = timeout
        return self

    def _get_params(self) -> dict:
        params = super()._get_params()

        query = None
        if self.query._query:
            query = str(self.query)

        if query:
            params["sysparm_query"] = query

        if self.sysparm_limit != 500:
            params["sysparm_limit"] = self.sysparm_limit

        if self.sysparm_offset:
            params["sysparm_offset"] = self.sysparm_offset

        if self.sysparm_suppress_pagination_header:
            params["sysparm_suppress_pagination_header"] = (
                self.sysparm_suppress_pagination_header
            )

        if self.sysparm_query_category:
            params["sysparm_query_category"] = self.sysparm_query_category

        if self.sysparm_no_count:
            params["sysparm_no_count"] = self.sysparm_no_count

        if self.sysparm_count:
            params["sysparm_count"] = self.sysparm_count

        return params

    def __request_helper(self, next_link="", retries=5) -> str:
        try:
            result = None
            params = self._get_params()
            if next_link:
                result = self.http_client.get(
                    next_link, params=params, timeout=self.response_timeout
                )
            else:
                result = self.http_client.get(
                    f"{self.default_path}/{self.table}",
                    params=params,
                    timeout=self.response_timeout,
                )
            if result.status_code != 200:
                text = result.text
                raise RecordFilterException(text)

            if result.headers.get("content-type")[:16] == "application/json":
                data = result.json()
                self.data.extend(data.get("result"))
                if result.links.get("next"):
                    next_link = (
                        result.links.get("next", {})
                        .get("url", "")
                        .replace(f"{os.environ['SERVICENOW_URL']}/", "")
                    )
                    return next_link
                return None
        except Exception as e:
            if retries > 0:
                print("Error: " + str(e))
                print("Retry in 30s")
                sleep(30)
                return self.__request_helper(next_link=next_link, retries=retries - 1)
            else:
                raise RecordRetriesException(e)

    def __request_helper_without_next_link(self, retries=5) -> int:
        try:
            params = self._get_params()
            if not self.sysparm_offset:
                self.sysparm_offset = 0

            result = self.http_client.get(
                path=f"{self.default_path}/{self.table}",
                params=params,
                timeout=self.response_timeout,
            )

            if result.status_code != 200:
                text = result.text
                raise RecordFilterException(text)

            total_registers = int(result.headers["X-Total-Count"])
            data = result.json()
            self.data.extend(data.get("result"))
            return total_registers

        except Exception as e:
            if retries > 0:
                print("Error: " + str(e))
                print("Retry in 30s")
                sleep(30)
                return self.__request_helper_without_next_link(retries=retries - 1)
            else:
                raise RecordRetriesException(e)

    def get(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        self.data = []
        if self.sysparm_suppress_pagination_header:
            self.total_registers_sequence_request = (
                self.__request_helper_without_next_link()
            )
            if (
                self.sysparm_offset + self.sysparm_limit
                < self.total_registers_sequence_request
            ):
                self.sysparm_offset = self.sysparm_offset + self.sysparm_limit
            else:
                self.sysparm_offset = None
                self.total_registers_sequence_request = 0
            return self
        self.next_link_sequence_request = self.__request_helper(
            self.next_link_sequence_request
        )
        return self

    @property
    def next(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.get()

    def all(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        self.data = []
        if self.sysparm_suppress_pagination_header:
            while True:
                total_registers = self.__request_helper_without_next_link()
                if self.sysparm_offset + self.sysparm_limit < total_registers:
                    self.sysparm_offset = self.sysparm_offset + self.sysparm_limit
                else:
                    self.sysparm_offset = None
                    break
            return self.data

        else:
            next_link = None
            while True:
                next_link = self.__request_helper(next_link=next_link)
                if not next_link:
                    break
            return self.data


class Manager(BaseTableAPI):
    sysparm_input_display_value = None
    sysparm_suppress_auto_sys_field = None

    def input_display_value(self, input_display_value: bool):
        """Set field values using their display value (true) or actual value (false) (default: false)

        Args:
            input_display_value (bool): Set field values using their display value (true) or actual value (false) (default: false)

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_input_display_value = input_display_value
        return self

    def suppress_auto_sys_field(self, suppress_auto_sys_field: bool):
        """Suppress auto generation of system fields (default: false)

        Args:
            input_display_value (bool): True to suppress auto generation of system fields (default: false)

        Returns:
            TableAPI: Return self class
        """
        self.sysparm_suppress_auto_sys_field = suppress_auto_sys_field
        return self

    def _get_params(self) -> dict:
        params = super()._get_params()

        if self.sysparm_suppress_auto_sys_field:
            params["sysparm_suppress_auto_sys_field"] = (
                self.sysparm_suppress_auto_sys_field
            )

        if self.sysparm_input_display_value:
            params["sysparm_input_display_value"] = self.sysparm_input_display_value

    def retrive(self, sys_id: str):
        result = self.http_client.get(
            f"{self.default_path}/{self.table}/{sys_id}", params=self._get_params()
        )

        data = result.json()
        if result.status_code != 200:
            raise ManagerRetriveException(data)
        return data

    def create(self, data: dict):
        result = self.http_client.post(
            f"{self.default_path}/{self.table}", data=data, params=self._get_params()
        )

        data = result.json()
        if result.status_code != 201:
            raise ManagerRetriveException(data)
        return data

    def delete(self, sys_id: str):
        result = self.http_client.delete(f"{self.default_path}/{self.table}/{sys_id}")

        data = result.json()
        if result.http_client.status_code != 200:
            raise ManagerRetriveException(data)
        return data

    def full_update(self, sys_id: str, data: dict):
        result = self.http_client.put(
            f"{self.default_path}/{self.table}/{sys_id}",
            data=data,
            params=self._get_params(),
        )

        data = result.json()
        if result.status_code != 200:
            raise ManagerRetriveException(data)
        return data

    def update(self, sys_id: str, data: dict):
        result = self.http_client.patch(
            f"{self.default_path}/{self.table}/{sys_id}",
            data=data,
            params=self._get_params(),
        )

        data = result.json()
        if result.status_code != 200:
            raise ManagerRetriveException(data)
        return data


class Vars(BaseTableAPI):
    __query = QueryBuilder()

    def __init__(self) -> None:
        super().__init__(table="sc_item_option_mtom")
        self.sysparm_limit = 500

    def _get_params(self) -> dict:
        params = super()._get_params()

        query = None
        if self.__query._query:
            query = str(self.__query)

        if query:
            params["sysparm_query"] = query

        return params

    def get_vars(self, by_field: str, data: str):
        self.__query.field(f"request_item.{by_field}").equals(data)
        self.__query.AND().field("request_item.sys_id").equals("sc_req_item.sys_id")
        self.__query.AND().field("sc_item_option_mtom.sc_item_option").equals(
            "sc_item_option.sys_id"
        )

        result = self.http_client.get(
            f"{self.default_path}/{self.table}", params=self._get_params()
        )

        data = result.json()
        if result.status_code != 200:
            raise RecordFilterException(data)

        return data


class ProducerServiceCatalog(Client):
    default_path = "api/sn_sc/servicecatalog/items"

    def store(self, catalog_id: str, variables: dict):
        path = f"{catalog_id}/submit_producer"
        result = self.post(f"{self.default_path}/{path}", data={"variables": variables})
        data = result.json()
        if result.status_code != 200:
            raise ManagerRetriveException(data)
        return data

    def store_task(self, catalog_id: str, variables: dict, sysparm_quantity: int = 1):
        """Open task ticket in servicenow
        Args:
            catalog_id (str, mandatory): service catalog sys id.
            variables (dict, mandatory): dictionary with variables values to open ticket.
            sysparm_quantity (int, optional): quantity of requisitions.

        Return:
            dict: data of ticket opened
        """
        path = f"{catalog_id}/order_now"
        payload = {"sysparm_quantity": sysparm_quantity, "variables": variables}
        result = self.post(f"{self.default_path}/{path}", data=payload)

        data = result.json()

        if result.status_code != 200:
            raise ManagerRetriveException(data)
        return data

    def update(self, sys_id: str, variables: dict):
        path = f"{sys_id}/submit_guide"
        result = self.put(f"{self.default_path}/{path}", data={"variables": variables})
        data = result.json()
        if result.status_code != 200:
            raise ManagerRetriveException(data)
        return data

    def get_catalog_item(self, sys_id: str) -> dict:
        """Retrieves a catalog item information.

        Args:
            sys_id (str, mandatory): sys id of catalog item

        Return:
            dict: catalog item information
        """
        path = f"{sys_id}"
        result = self.get(f"{self.default_path}/{path}")
        data = result.json()

        if result.status_code != 200:
            raise RecordFilterException(data)

        return data["result"]
