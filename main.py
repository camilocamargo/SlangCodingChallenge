from get_user_session import GetUserSessions
from send_user_sessions import SendUserSession
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects

if __name__ == '__main__':
    # get the information of user sessions
    try:
        get_us = GetUserSessions()
        user_sessions = get_us.get_sessions()
    except ConnectionError as error:
        print(f'Connection error occurred: {error}')
    except HTTPError as error:
        print(f'HTTP error occurred: {error}')
    except Timeout as error:
        print(f'The request times out: {error}')
    except TooManyRedirects as error:
        print(f'The request times out: {error}')
    except Exception as error:
        print(f'Other error occurred: {error}')
    else:
        try:
            send_us = SendUserSession()
            post_response = send_us.send_user_session(user_sessions)
        except ConnectionError as error:
            print(f'Connection error occurred: {error}')
        except HTTPError as error:
            print(f'HTTP error occurred: {error}')
        except Timeout as error:
            print(f'The request times out: {error}')
        except TooManyRedirects as error:
            print(f'The request times out: {error}')
        except Exception as error:
            print(f'Other error occurred: {error}')
        else:
            print(post_response)
