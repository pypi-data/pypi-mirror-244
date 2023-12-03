import os
import uuid
from pyrogram import filters
from pyrogram import Client, filters
from pymongo import MongoClient
from bson.json_util import dumps, loads
import os
from pymongo import MongoClient
from bson.json_util import dumps, loads
from pyrogram import Client, filters
import os
import time
from pyromod import listen
from .paid_config import *
from .premium import *
from pyrogram import Client as DKBOTZ, filters

try:
    from bot import Bot as DKBOTZ
except ModuleNotFoundError as e:
    pass
except ImportError as e:
    pass
except Exception as e:
    pass



@DKBOTZ.on_message(filters.command("export"))
async def export_to_json(client, message):
    try:

        MONGODB_URI = MANGODB_URL
        DATABASE_NAME = SESSION_NAME


        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[DATABASE_NAME]


        collection_names = collection_name

        source_collection = mongo_db[collection_names]
        data_to_export = source_collection.find()
        json_data = dumps(data_to_export)

        export_file_path = f'exported_data_{collection_names}.json'
        with open(export_file_path, 'w') as export_file:
            export_file.write(json_data)

        await message.reply_document(document=export_file_path, caption=f'Exported data from {collection_name}')
        
        await message.reply_text('Data exported successfully!')

    except Exception as e:
        await message.reply_text(f'Error exporting data: {str(e)}')



# Import command
@DKBOTZ.on_message(filters.command("import"))
async def import_from_json(client, message):
    try:
        MONGODB_URI = MANGODB_URL
        DATABASE_NAME = SESSION_NAME
        collection_names = collection_name

        await client.send_message(message.chat.id, "Please send the exported JSON file.")
        document_message = await client.listen(message.chat.id)


        if document_message and document_message.document:
            folder_path = f"{message.chat.id}_imported_data"
            os.makedirs(folder_path, exist_ok=True)

            # Generate a random file name
            random_file_name = str(uuid.uuid4()) + ".json"
            file_path = os.path.join(folder_path, random_file_name)

            # Download the document
            await client.download_media(document_message.document.file_id, file_name=file_path)

            with open(file_path, 'r') as import_file:
                json_data = import_file.read()

            data_to_import = loads(json_data)

            # Connect to the specified MongoDB
            mongo_client = MongoClient(MONGODB_URI)
            mongo_db = mongo_client[DATABASE_NAME]
            destination_collection = mongo_db[collection_names]

            # Import data into the specified collection
            for document in data_to_import:
                destination_collection.insert_one(document)

            await message.reply_text('Data imported successfully!')

            # Clean up: remove the downloaded file and folder
            os.remove(file_path)
            os.rmdir(folder_path)

        else:
            await message.reply_text('No document (file) found. Please send the exported JSON file.')

    except Exception as e:
        await message.reply_text(f'Error importing data: {str(e)}')
