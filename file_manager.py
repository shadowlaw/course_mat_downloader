import os

# Constant holding all allowed file types for course material download
FILE_LIST = ['.docx', '.doc', '.pdf', '.txt', '.ppt', '.pptx', '.ppsx', '.pptm',
             '.docm', '.dotx', '.dotm', '.docb', '.xlsx', '.xlsm', '.xltx',
             '.xltm', '.xlsb', '.xla', '.xlam', '.xll', '.xlw', '.zip']


def create_folder(path):
    '''Creates folder if not present exists.

    Argument list:
    project: file path to be tested and created.
    '''

    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)


def create_file(filename):
    '''Creates an empty file.

    Arguemnt list:
    filename: name of the file to create. Absolute filename can also be passed and created.
    '''

    if not os.path.isfile(filename):
        try:
            with open(filename, 'w'):
                pass
        except Exception as e:
            print(e)


def file_list(foldername):
    '''Returns a list of all files in a given folder that matches the FILE_LIST.

    Argument list:
    foldername: relative or absolute folder path
    '''

    try:
        files = os.listdir(foldername)
        results = []
        for item in files:
            if os.path.isfile(os.path.join(foldername, item)):
                if '.'+str(item).split('.')[-1] in FILE_LIST:
                    results.append(item)

        return results
    except Exception as e:
        print(e)
        return []


def downloading_file_check(folder_name):
    '''Checks for a single instance of a partially downloaded file in a given folder.

    Argument list:
    folder_name: relative or absolute folder path to check.
    '''

    try:
        files = os.listdir(folder_name)
        for item in files:
            if os.path.isfile(os.path.join(folder_name, item)):
                if 'download' in '.'+str(item).split('.')[-1]:
                    return True

        return False
    except Exception as e:
        print(e)
        return False


def move_all_files_to(src, dest):
    '''Moves all files from a specified source to a specified destination.

    Argument list:
    src: source folder path
    dest: destination folder path
    '''

    create_folder(dest)
    files = file_list(src)

    for item in files:
        current_location = os.path.join(src, item)
        destination_location = os.path.join(dest, item)
        try:
            os.rename(current_location, destination_location)
        except Exception as e:
            print(e)
