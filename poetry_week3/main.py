from dotenv import load_dotenv
import argparse
from poetry_week3.bucket.crud import Bucket_Crud
from poetry_week3.bucket.policy import Bucket_Policy
from poetry_week3.client import Client
from poetry_week3.object.crud import Object_Crud
from poetry_week3.object.policy import Object_Policy


load_dotenv()


def main(command_line=None):
    parser = argparse.ArgumentParser('AWS S3 Client BTU TASK')
    parser.add_argument(
        '--showBuckets',
        action='store_true',
        help='Print buckets'
    )
    subparsers = parser.add_subparsers(dest='command')
    bucket = subparsers.add_parser('bucket', help='work with bucket')
    bucket.add_argument(
        '--name',
        type=str, help="Enter Bucket Name", required=True
    )

    group = bucket.add_mutually_exclusive_group()
    group.add_argument('--createBucket', action='store_true')
    group.add_argument('--deleteBucket', action='store_true')
    group.add_argument('--showPolicy', action='store_true')
    group.add_argument("-arp",
                       "--assign_read_policy",
                       help="flag to assign read bucket policy.",
                       choices=[
                            "False", "True"],
                       type=str,
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument("-amp",
                       "--assign_missing_policy",
                       help="flag to assign read bucket policy.",
                       choices=["False", "True"],
                       type=str,
                       nargs="?",
                       const="True",
                       default="False")

    group.add_argument('-makePublic', '-mp', '--makePublic',  action='store_true',
                       help="make Public(read) file", dest="makePublic")
    group.add_argument('--uploadFile', type=str,
                       help="Enter file url.",)
    bucket.add_argument('--filename', type=str,
                        help="Enter File name format for uploading.")
    bucket.add_argument('-save', '-s', '--save',  action='store_true',
                        help="Keep/Save local when uploading image", dest="save")

    args = parser.parse_args(command_line)

    if args.showBuckets:
        s3_client = Client()
        buckets = Bucket_Crud.buckets()
        if buckets:
            for bucket in buckets:
                print(f' {bucket["Name"]}')

    if args.command == 'bucket':
        s3_client = Client(args.name)
        if args.createBucket:
            Bucket_Crud.create_bucket()
        if args.showPolicy:
            Bucket_Policy.read_bucket_policy()
        if args.deleteBucket:
            Bucket_Crud.delete_bucket()
        if args.assign_read_policy == "True":
            Bucket_Policy.assign_policy(
                s3_client, "public_read_policy")

        if args.assign_missing_policy == "True":
            Bucket_Policy.assign_policy(
                s3_client, "multiple_policy")

        if args.uploadFile:
            file_name = ""
            if args.filename:
                file_name = args.filename
            Object_Crud.download_file_and_upload_to_s3(
                args.uploadFile, file_name, keep_local=args.save)
        if args.makePublic and args.filename:
            Object_Policy.set_object_access_policy(args.filename)


if __name__ == "__main__":
    main()