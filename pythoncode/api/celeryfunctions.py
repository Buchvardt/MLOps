import time

def long_running_function(message: str="", seconds: int=10) -> None: 
    """Simulate a long running function.

    Args:
        message (str): A string, no longer than 100 chars
        seconds (int): An Integer, no larger than 30

    Returns:
        None

    Raises:
        ValueError: If length of `message` > 100
        ValueError: If `seconds` > 30

    Example:
        When executing the function, there will be printed a status

        >>> long_running_function(message="TEST", seconds=5)
        long_running_function processing TEST - time left: 4 sec.
        long_running_function processing TEST - time left: 3 sec.
        long_running_function processing TEST - time left: 2 sec.
        long_running_function processing TEST - time left: 1 sec.
        long_running_function processing TEST - time left: 0 sec.
        long_running_function done

    """

    if len(message) > 100:
        raise ValueError('n chars in message must be <= 100')

    if seconds > 30:
        raise ValueError('seconds must be <= 30')

    for i in range(seconds):

        print(f'long_running_function processing {message} - time left: {seconds-i} sec.')

        time.sleep(1)        

    print(f'long_running_function done')

    return

if __name__ == "__main__":

    long_running_function(message="TEST", seconds=5)