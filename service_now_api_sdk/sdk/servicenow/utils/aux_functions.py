# Reference: https://docs.servicenow.com/bundle/utah-platform-user-interface/page/use/navigation/task/navigate-using-url.html

from service_now_api_sdk.settings import SERVICENOW_URL
from service_now_api_sdk.sdk.servicenow.utils.constants import URLPatterns

from service_now_api_sdk.sdk.servicenow.helpers.query_builder import (
    QueryBuilder
)


def make_platform_url_list_view(
    table_name: str,
    ticket_number: str = None,
    query: QueryBuilder = None
) -> str:
    """
    Constructs the URL for a list of tickets user interface.

    Args:
        table_name (str, required): An str indicating the table that store the ticket.
        ticket_number (str, optional/required): An str indicating the ticket number.
            Defaults to None but required if the query parameter wasnt given.
        query (QueryBuilder, optional): An instance of the QueryBuilder class containing query parameters.
            Defaults to None. If not given, the return will be the default view of a ticket.

    Returns:
        str: The URL for the list of tickets user interface.

    Examples:
        query = QueryBuilder().field('number').starts_with("RIT")
        
        url = make_platform_url_list_view(table_name="sc_req_item", query=query, interface="list_view")
        
        print(url)

        Output:
            https://stone.service-now.com/sc_req_item_list.do?sysparm_query=numberSTARTSWITHRIT
    
    Notes:
        If the query parameter is not defined, you should set ticket_number parameter
        so that the function returns its interface view for that ticket.
    """
    if not query and not ticket_number:
        raise TypeError("Neither query or ticket_number parameters were given.")
    else:
        interface_url = "list"
        base_url = (
            f"{SERVICENOW_URL}/{table_name}_{interface_url}"
            f".{URLPatterns.ACTION}"
            f"?{URLPatterns.SYSPARM_QUERY}"
        ) 
        if query:
            return_url = (
                f"{base_url}"
                f"={query.__str__()}"
            )
        if not query:
            return_url = (
                f"{base_url}"
                f"={URLPatterns.NUMBER_FIELD}"
                f"={ticket_number}"
            )      
        return return_url


def make_platform_url_standard_view(
    table_name: str,
    ticket_number: str = None,
    query: QueryBuilder = None
) -> str:
    """
    Constructs the URL for a ticket user interface.

    Args:
        table_name (str, required): An str indicating the table that store the ticket.
        ticket_number (str, optional/required): An str indicating the ticket number.
            Defaults to None but required if the query parameter wasnt given.
        query (QueryBuilder, optional): An instance of the QueryBuilder class containing query parameters.
            Defaults to None. If not given, the return will be the default view of a ticket.

    Returns:
        str: The URL for the ticket user interface.

    Examples:
        ticket_number = "RITM123456"
        
        url = make_platform_url_standard_view(table_name="sc_req_item", ticket_number=ticket_number)
        
        print(url)

        Output:
            https://stonedev.service-now.com/nav_to.do?uri=sc_req_item.do?sysparm_query=number=RITM123456
    
    Notes:
        If the query parameter is not defined, you should set ticket_number parameter
        so that the function returns its interface view for that ticket.
    """
    if not query and not ticket_number:
        raise TypeError("Neither query or ticket_number parameters were given.")
    else:
        interface_url = "nav_to"
        base_url = (
            f"{SERVICENOW_URL}/{interface_url}"
            f".{URLPatterns.ACTION}"
            f"?{URLPatterns.URI}"
            f"={table_name}"
            f".{URLPatterns.ACTION}"
            f"?{URLPatterns.SYSPARM_QUERY}"
        )
        if query:
            return_url = (
                f"{base_url}"
                f"={query.__str__()}"
            )
        if not query:
            return_url = (
                f"{base_url}"
                f"={URLPatterns.NUMBER_FIELD}"
                f"={ticket_number}"
            )      
        return return_url
