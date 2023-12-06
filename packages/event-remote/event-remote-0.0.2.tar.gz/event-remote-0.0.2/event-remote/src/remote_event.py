# TODO: This is an example file which you should delete after impenting
import pymysql
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from url_local.component_name_enum import ComponentName
from url_local.entity_name_enum import EntityName
from url_local.action_name_enum import ActionName
from url_local.url_circlez import OurUrl
from sdk.src.utilities import create_http_headers




GROUP_PROFILE_COMPONENT_ID = 248
GROUP_PROFILE_COMPONENT_NAME = "event-remote-restapi-python-package"
COMPONENT_CATEGORY = LoggerComponentEnum.ComponentCategory.Code.value
COMPONENT_TYPE = LoggerComponentEnum.ComponentType.Remote.value
DEVELOPER_EMAIL = "gil.a@circ.zone"

obj = {
    'component_id': GROUP_PROFILE_COMPONENT_ID,
    'component_name': GROUP_PROFILE_COMPONENT_NAME,
    'component_category': COMPONENT_CATEGORY,
    'component_type': COMPONENT_TYPE,
    "developer_email": DEVELOPER_EMAIL
}

BRAND_NAME = os.getenv("BRAND_NAME")
ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME")
EVENT_API_VERSION = 1



class EventRemote:

    def __init__(self):
        self.url_circlez = OurUrl()
        self.logger = Logger.create_logger(object=obj)
        self.brand_name = BRAND_NAME
        self.env_name = ENVIRONMENT_NAME


    def get_url_by_action_name(self, action_name:ActionName, path_parameters:dict=None):
        #optional query_parameters can be added if needed
        return self.url_circlez.endpoint_url(
            brand_name=self.brand_name,
            environment_name=self.env_name,
            component_name=ComponentName.EVENT.value,
            entity_name=EntityName.EVENT.value,
            version=EVENT_API_VERSION,
            action_name=action_name.value,
            path_parameters=path_parameters if path_parameters else None
        )

    def create(self, location_id:int, organizers_profile_id:int, website_url:str,
                facebook_event_url:str='', meetup_event_url:str ='', registration_url:str=''):
        object_start = {
            'location_id':location_id,
            'organizers_profile_id':organizers_profile_id,
            'website_url':website_url,
            'facebook_event_url':facebook_event_url,
            'meetup_event_url':meetup_event_url,
            'registration_url':registration_url
        }
        self.logger.start("Start create event", object=object_start)
        try:
            url =self.get_url_by_action_name(ActionName.CREATE_EVENT)
          
            #placeholder for url - component name is wrong 
            url = "https://x8ql0j9cwf.execute-api.us-east-1.amazonaws.com/dev/play1/api/v1/event/createEvent"

            self.logger.info(
                "Endpoint event  - createEvent action: " + url)

            event_payload_json = {
                "location_id": location_id,
                "organizers_profile_id": organizers_profile_id,
                "website_url": f"{website_url}",
                "facebook_event_url": f"{facebook_event_url}",
                "meetup_event_url": f"{meetup_event_url}",
                "registration_url": f"{registration_url}"
            }

            headers = create_http_headers(
               self.logger.user_context.get_user_JWT())
            response = requests.post(
                url=url, json=event_payload_json, headers=headers) 
            self.logger.end(
                f"End create event-remote, response: {str(response)}")
            return response


        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise


    def get_event_by_event_id(self, event_id: int):
        object_start = {
            'event_id': event_id
        }
        self.logger.start("Start get event-remote", object=object_start)
        try:
            path_parameters = {
                'event_id':event_id
            }
            url = self.get_url_by_action_name(ActionName.GET_EVENT_BY_ID, path_parameters=path_parameters)

            #placeholder for url - component name is wrong 
            url = f"https://x8ql0j9cwf.execute-api.us-east-1.amazonaws.com/dev/play1/api/v1/event/getEventById/{event_id}"

            self.logger.info(
                "Endpoint event - getEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())
            response = requests.get(url=url, headers=headers)
            self.logger.end(
                f"End get event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise


    def delete_event_by_id(self, event_id: int):
        object_start = {
            'event_id': event_id
        }
        self.logger.start("Start delete event-remote", object=object_start)
        try:
            path_parameters = {
                'event_id':event_id
            }
            url = self.get_url_by_action_name(ActionName.DELETE_EVENT_BY_ID, path_parameters=path_parameters)

            #placeholder for url - base url is wrong 
            url = f"https://x8ql0j9cwf.execute-api.us-east-1.amazonaws.com/dev/play1/api/v1/event/deleteEventById/{event_id}"

            self.logger.info(
                "Endpoint event - deleteEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())

            response = requests.delete(url=url, headers=headers)
            self.logger.end(
                f"End delete event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise


    def update_event_by_id(self, event_id: int, location_id: int, organizers_profile_id: int, website_url: str,
                facebook_event_url: str='', meetup_event_url: str='', registration_url: str=''):
        
        object_start = {
            'event_id':event_id,
            'location_id':location_id,
            'organizers_profile_id':organizers_profile_id,
            'website_url':website_url,
            'facebook_event_url':facebook_event_url,
            'meetup_event_url':meetup_event_url,
            'registration_url':registration_url
        }        
        self.logger.start("Start update event-remote", object=object_start)
        try:
            path_parameters = {
                'event_id':event_id
            }
            url = self.get_url_by_action_name(ActionName.UPDATE_EVENT_BY_ID, path_parameters=path_parameters)

            event_payload_json = {
                "location_id": location_id,
                "organizers_profile_id": organizers_profile_id,
                "website_url": f"{website_url}",
                "facebook_event_url": f"{facebook_event_url}",
                "meetup_event_url": f"{meetup_event_url}",
                "registration_url": f"{registration_url}"
            }

            #placeholder for url - base url is wrong 
            url = f"https://x8ql0j9cwf.execute-api.us-east-1.amazonaws.com/dev/play1/api/v1/event/updateEventById/{event_id}"

            self.logger.info(
                "Endpoint event - updateEventById action: " + url)

            headers = create_http_headers(
                self.logger.user_context.get_user_JWT())

            response = requests.put(url=url, json=event_payload_json, headers=headers)
            self.logger.end(
                f"End update event-remote, response: {str(response)}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise

        except requests.Timeout as e:
            self.logger.exception("Request timed out", e)
            raise

        except requests.RequestException as e:
            self.logger.exception(f"General error: {str(e)}", object=e)
            raise

        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {str(e)}", object=e)
            raise
