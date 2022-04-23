import json
import logging

import requests


class __Email(object):
    """Super Class for the TempMail Class"""

    def __init__(self):
        """Request for new email
        Return:
            email: str of email as Mail@Domain
            Mail: str of Mail 
            Domain: str of Domain"""
        super().__init__()
        logging.basicConfig(
            format='%(name)s - %(levelname)s: %(message)s', level=logging.DEBUG)
        self._logger = logging.getLogger("TempMail")
        self._api = "https://www.1secmail.com/api/v1/?"
        action = "genRandomMailbox"
        count = 1
        new_mail_request = f"{self._api}action={action}&count={count}"
        new_mail_response = self._request_handler(new_mail_request)
        self._email = self.__extract_email(new_mail_response)
        self._mail, self._domain = self._email.split("@")
        self._logger.info(f"Super TempMailAPI initialized with {self._email}")

    def __extract_email(self, response):
        """Extracting the email from the response
            Args:
                response: requests.Response
            Return:
                email: str of email as Mail@Domain"""
        email = response.text
        for symbol in email:
            if symbol == "[" or symbol == "\"" or symbol == "]":
                email = email.replace(symbol, "")
        self._logger.info(f"Extracted email: {email}")
        return email

    def __try(self, request, exception, count=3):
        """Retry the request for Counter times
        if the request is not successful raises exception
        Args:
            request: str of request
            exception: Exception
            count: int of Counter
        Return:
            response: requests.Response
        Raises:
            exception: Exception"""
        if count:
            try:
                self._logger.debug(f"Retrying request: {request}")
                return requests.get(request)
            except exception:
                self._logger.error(f"Exception: {exception}")
                self._logger.debug(f"Retrying request: {request}")
                return self.__try(request, exception, count-1)
        else:
            self._logger.error(f"Exception: {exception}")
            self._logger.critical(f"Request failed: {request}")
            raise exception

    def _request_handler(self, request):
        """Handling the request by retrying the request for Counter times
        if the request is not successful raises exception
        Args:
            request: str of request
        Return:
            response: requests.Response
        Raises:
            exception: Exception"""
        try:
            self._logger.debug(f"Requesting: {request}")
            return requests.get(request)
        except requests.exceptions.ConnectionError as ex:
            self._logger.debug(f"ConnectionError: {ex}")
            return self.__try(request, ex)
        except requests.exceptions.Timeout as ex:
            self._logger.debug(f"Timeout: {ex}")
            return self.__try(request, ex)
        except requests.exceptions.TooManyRedirects as ex:
            self._logger.debug(f"TooManyRedirects: {ex}")
            return self.__try(request, ex)

    def get_mail(self):
        """foo"""
        self._logger.info(f"Returning mail: {self._mail}")
        return self._mail

    def get_domain(self):
        """foo"""
        self._logger.info(f"Returning domain: {self._domain}")
        return self._domain

    def get_email(self):
        """foo"""
        self._logger.info(f"Returning email: {self._email}")
        return self._email


class TempMail(__Email):
    """foo"""

    # constructor for test purposes
    def __init__(self, test=True):
        """Initialize Temporary Mail"""
        super().__init__()
        if test:
            self._logger.info("Test mode activated")

    def __init__(self):
        """Initialize Temporary Mail"""
        super().__init__()

    def __json_handler(self, data):
        """Handling the json data
        Args:
            data: json
        Return:
            message: str of message"""
        try:
            self._logger.debug(f"Handling json data: {data}")
            return json.loads(data)
        except:
            self._logger.error("Message not found")
            return {}

    def __data_handler(self, data, attribute: str):
        """Handling the data extraction"""
        try:
            return data[0][attribute]
        except:
            try:
                return data[attribute]
            except IndexError as ex:
                self._logger.error(f"No attribute found: {ex}", exc_info=True)
                return []
            except TypeError as ex:
                self._logger.error(f"No attribute found: {ex}", exc_info=True)
                return []
            except KeyError as ex:
                self._logger.error(f"No attribute found: {ex}", exc_info=True)
                return []

    def __last_received_mail(self):
        """Request for the last received mail
        Return:
            response: requests.Response"""
        action = "getMessages"
        mail_request = f"{self._api}action={action}&login={self._mail}&domain={self._domain}"
        self._logger.debug(f"Requesting: {mail_request}")
        mail_response = self._request_handler(mail_request)
        self._logger.debug(
            f"Returning last received mail: {mail_response.text}")
        return self.__json_handler(mail_response.text)

    def __last_received_id(self):
        """Gets the last mail id
        Return:
            id: int of id"""
        mail = self.__last_received_mail()
        self._logger.debug(f"Returning last received id.")
        return self.__data_handler(mail, "id")

    def __last_received_message(self):
        """Request for the last received message
        Return:
            message: str of message"""
        id = self.__last_received_id()
        action = "readMessage"
        message_request = f"{self._api}action={action}&login={self._mail}&domain={self._domain}&id={id}"
        self._logger.debug(f"Requesting: {message_request}")
        message_response = self._request_handler(message_request)
        self._logger.debug(
            f"Returning last received message: {message_response.text}")
        return self.__json_handler(message_response.text)

    def __last_received_subject(self):
        """Request for the last received subject
        Return:
            subject: str of subject"""
        message = self.__last_received_message()
        self._logger.debug(f"Returning last received subject.")
        return self.__data_handler(message, "subject")

    def __last_received_body(self):
        """Request for the last received body
        Return:
            body: str of body"""
        message = self.__last_received_message()
        self._logger.debug(f"Returning last received body.")
        return self.__data_handler(message, "body")

    def get_subject(self):
        """Gets the last received subject
        Return:
            subject: str of subject"""
        self._logger.info(
            f"Returning subject: {self.__last_received_subject()}")
        return self.__last_received_subject()

    def get_body(self):
        """Gets the last received body
        Return:
            body: str of body"""
        self._logger.info(f"Returning body: {self.__last_received_body()}")
        return self.__last_received_body()

    def receive_mail(self):
        """foo"""
        subject = self.__last_received_subject()
        body = self.__last_received_body()
        received_mail = {
            "subject": subject,
            "body": body
        }
        self._logger.info(f"Returning received mail: {received_mail}")
        return received_mail


if __name__ == '__main__':
    tm = TempMail()
    print(tm.get_mail())
    print(tm.get_domain())
    print(tm.get_email())
    print(tm.get_subject())
    print(tm.get_body())
    print(tm.receive_mail())
