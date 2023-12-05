import os
import string
import hashlib
import gnupg

checksum_prefix_extension = '.checksum'


def create_unsigned_checksum_file(file_name: str):
    file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]
    checksum_file_name = file_name_without_extension + checksum_prefix_extension
    create_named_unsigned_checksum_file(file_name, checksum_file_name)
    return checksum_file_name


def create_signed_checksum_file(file_name: str, pgp_key_id: str):
    file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]
    checksum_file_name = file_name_without_extension + checksum_prefix_extension
    create_named_signed_checksum_file(file_name, checksum_file_name, pgp_key_id)
    return checksum_file_name


def create_named_unsigned_checksum_file(file_name: str, checksum_file_name: str):
    file_sum = create_file_sum(file_name)
    write_checksum_file(file_name, file_sum, checksum_file_name)


def create_named_signed_checksum_file(file_name: str, checksum_file_name: str, pgp_key_id: str):
    create_named_unsigned_checksum_file(file_name, checksum_file_name)
    sign_checksum_file(checksum_file_name, pgp_key_id)


def create_file_sum(file_name: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_name, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def write_checksum_file(file_name: str, file_sum: str, checksum_file_name: str):
    file_stats = os.stat(file_name)
    template = string.Template('#$FILE_NAME $FILE_SIZE_BYTES bytes\nSHA256 ($FILE_NAME) = $FILE_SUM')
    output = template.substitute({
        'FILE_NAME': file_name,
        'FILE_SIZE_BYTES': file_stats.st_size,
        'FILE_SUM': file_sum
    })
    with open(checksum_file_name, 'w') as f:
        f.write(output)


def sign_checksum_file(checksum_file_name: str, pgp_key_id: str):
    gnupg.GPG().sign_file(checksum_file_name, keyid=pgp_key_id, output=checksum_file_name)
