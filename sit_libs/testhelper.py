import yaml, os

def read_yaml(file):
    """Returns a dict containing the contents of the yaml file.

    Parameters:
    arg1: filename of yaml file

    Returns:
    dict: parsed contents of a yaml file
    """
    with open(file) as f:
        test_info = yaml.load(f, Loader=yaml.FullLoader)
    return test_info

def gen_mount_params(host, share, username, password):
    """Generate a dict of parameters required to mount a SMB share.

    Parameters:
    host: hostname
    share: exported share name
    username: username
    password: password for the user

    Returns:
    dict: mount parameters in a dict
    """
    ret = {
        "host" : host,
        "share" : share,
        "username" : username,
        "password" : password
    }
    return ret

def get_default_mount_params(test_info):
    """Pass a dict of type mount_params containing the first parameters to mount the share.

    Parameters:
    test_info: Dict containing the parsed yaml file.

    Returns:
    Dict: of type mount_params containing the parameters to mount the share.
    """
    return gen_mount_params(
        test_info["public_interfaces"][0],
        test_info["exported_sharenames"][0],
        test_info["test_users"][0]["username"],
        test_info["test_users"][0]["password"]
    )

def get_total_mount_parameter_combinations(test_info):
    """Get total number of combinations of mount parameters for each share.
    This is essentially "number of public  interfaces * number of test users"

    Parameters:
    test_info: Dict containing the parsed yaml file.

    Returns:
    int: number of possible combinations.
    """
    return len(test_info["public_interfaces"]) * len(test_info["test_users"])

def get_mount_parameter(test_info, share, combonum):
    """Get the mount_params dict for a given share and given combination number

    Parameters:
    test_info: Dict containing the parsed yaml file.
    share: The share for which to get the mount_params
    combonum: The combination number to use.
    """
    if (combonum > get_total_mount_parameter_combinations(test_info)):
        assert False, "Invalid combination number"
    num_public = combonum / len(test_info["test_users"])
    num_users = combonum % len(test_info["test_users"])
    return gen_mount_params(
        test_info["public_interfaces"][num_public],
        share,
        test_info["test_users"][num_users]["username"],
        test_info["test_users"][num_users]["password"]
    )

def cifs_mount(mount_params, mount_point, opts="vers=2.1"):
    """Use the cifs module to mount a share.

    Parameters:
    mount_params: Dict containing mount parameters
    mount_point: Directory location to mount the share.
    opts: Additional options to pass to the mount command

    Returns:
    int: return value of the mount command.
    """
    mount_options = opts + ",username=" + mount_params["username"] + ",password=" + mount_params["password"]
    share = "//" + mount_params["host"] + "/" + mount_params["share"]
    cmd = "mount -t cifs -o " + mount_options + " " + share + " " + mount_point
    ret = os.system(cmd)
    assert ret == 0, "Error mounting: ret %d cmd: %s\n" % (ret, cmd)
    return ret

def cifs_umount(mount_point):
    """Unmount a mounted filesystem.

    Parameters:
    mount_point: Directory of the mount point.

    Returns:
    int: return value of the umount command.
    """
    cmd = "umount -fl %s" % (mount_point)
    ret = os.system(cmd)
    assert ret == 0, "Error mounting: ret %d cmd: %s\n" % (ret, cmd)
    return ret

TMP_DIR = "/tmp/"
def get_tmp_root():
    """Returns a temporary directory for use

    Parameters:
    none

    Returns:
    tmp_root: Location of the temporary directory.
    """
    tmp_root = TMP_DIR + "/" + str(os.getpid())
    i=0
    while (os.path.exists(tmp_root)):
        tmp_root = tmp_root + str(i)
        i = i + 1
    os.mkdir(tmp_root)
    return tmp_root

def get_tmp_mount_point(tmp_root):
    """Return a mount point within the temporary directory

    Parameters:
    tmp_root: Directory in which to create mount point.

    Returns:
    mnt_point: Directory location in which you can mount a share.
    """
    i = 0
    mnt_point = tmp_root + "/mnt_" + str(i)
    while (os.path.exists(mnt_point)):
        i = i + 1
        mnt_point = tmp_root + "/" + str(i)
    os.mkdir(mnt_point)
    return mnt_point

def get_tmp_file(tmp_root):
    """Return a temporary file within the temporary directory

    Parameters:
    tmp_root: Directory in which to create temporary file.

    Returns:
    tmp_file: Location of temporary file.
    """
    i = 0
    tmp_file = tmp_root + "/tmp_file_" + str(i)
    while (os.path.exists(tmp_file)):
        i = i + 1
        tmp_file = tmp_root + "/tmp_file_" + str(i)
    f = open(tmp_file, 'w')
    f.close()
    return tmp_file

def get_tmp_dir(tmp_root):
    """Return a temporary directory within the temporary directory

    Parameters:
    tmp_root: Directory in which to create temporary directory.

    Returns:
    tmp_dir: Location of temporary directory.
    """
    i = 0
    tmp_dir = tmp_root + "/tmp_dir_" + str(i)
    while (os.path.exists(tmp_dir)):
        i = i + 1
        tmp_dir = tmp_root + "/tmp_dir_" + str(i)
        os.mkdir(tmp_dir)
    return tmp_dir
