import sys
import fcsigner

args: [] = sys.argv
if len(args) < 3 or len(args) > 4:
    print("usage fcsigner [file_to_sign] [PGP_ID]\n OR fcsigner --no-sign [file_to_sign]")

else:
    if args[1] == '--no-sign':
        fcsigner.create_unsigned_checksum_file(args[2])
    else:
        fcsigner.create_signed_checksum_file(args[1], args[2])
