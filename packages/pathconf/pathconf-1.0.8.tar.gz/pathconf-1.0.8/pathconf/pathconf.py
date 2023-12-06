import os
import json
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def search_directories(directory, target, stop_event):
    """
    Search for a file in a given directory and its subdirectories.

    Parameters:
        directory (str): Directory to start search from.
        target (str): Filename to search for.
        stop_event (threading.Event): Threading event to signal
        other threads to stop.

    Returns:
        str or None: Path to the found file or None.
    """
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            dirnames[:] = [d for d in dirnames if 'Deprecated' not in d]
            if stop_event.is_set():
                break
            if target in filenames:
                stop_event.set()
                return os.path.join(dirpath, target)
    except IOError as e:
        logging.error(f"IOError occurred: {e}")
    return None


def find_file(start_path, target):
    """
    Find the file starting from the start_path.

    Parameters:
        start_path (str): Path to start the search from.
        target (str): Filename to search for.

    Returns:
        list: List of found file paths.
    """
    stop_event = threading.Event()
    found_paths = []
    try:
        directories = [os.path.join(start_path, d)
                       for d in os.listdir(start_path)
                       if os.path.isdir(os.path.join(start_path, d))]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(
                       search_directories, d, target, stop_event
                       )for d in directories]
            for future in as_completed(futures):
                file_path = future.result()
                if file_path:
                    found_paths.append(file_path)
    except IOError as e:
        logging.error(f"IOError occurred: {e}")
    return found_paths


def load_json_config(file_path):
    """
    Load JSON configuration file.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON object or empty dictionary if file is invalid.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error("JSON Decode Error occurred")
        return {}
    except IOError as e:
        logging.error(f"IOError occurred: {e}")
        return {}


def find_path(target_file):
    """
    Main function to find the path of a target file. If multiple files
    with the same name exist on the same machine, then the most recently
    modified will be used.

    Parameters:
        target_file (str): Filename to search for.

    Returns:
        str: Path to the found file.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    config_path_part = os.path.join(os.path.expanduser("~"), '.config')
    config_path = os.path.join(config_path_part, 'pathconf')
    config_filename = '.file_paths.json'
    config_file_path = os.path.join(config_path, config_filename)

    try:
        os.makedirs(config_path, exist_ok=True)

        config = {}

        if os.path.isfile(config_file_path):
            config = load_json_config(config_file_path)
            file_path = config.get(target_file)

            if file_path and os.path.isfile(file_path):
                return file_path

        found_paths = find_file(os.path.expanduser("~"), target_file)
        if found_paths:
            file_path = max(found_paths, key=os.path.getmtime)
            config[target_file] = file_path
            with open(config_file_path, 'w+') as f:
                json.dump(config, f)
            return file_path
        else:
            raise FileNotFoundError(f"{target_file} not found.")
    except IOError as e:
        logging.error(f"IOError occurred: {e}")
