import mysql.connector
import csv
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='/path/to/cdr/cdr_processing.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
db_config = {
    'user': 'USERNAME',
    'password': 'PASSWORD',
    'host': 'localhost',
    'database': 'DB_NAME'
}

# Function to create table if it does not exist
def create_table_if_not_exists(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cdr_records (
        cdrRecordType INT,
        globalCallID_callManagerId INT,
        globalCallID_callId INT,
        origLegCallIdentifier INT,
        dateTimeOrigination INT,
        origNodeId INT,
        origSpan INT,
        origIpAddr VARCHAR(50),
        callingPartyNumber VARCHAR(50),
        callingPartyUnicodeLoginUserID VARCHAR(128),
        origCause_location INT,
        origCause_value INT,
        origPrecedenceLevel INT,
        origMediaTransportAddress_IP VARCHAR(50),
        origMediaTransportAddress_Port INT,
        origMediaCap_payloadCapability INT,
        origMediaCap_maxFramesPerPacket INT,
        origMediaCap_g723BitRate INT,
        origVideoCap_Codec INT,
        origVideoCap_Bandwidth INT,
        origVideoCap_Resolution INT,
        origVideoTransportAddress_IP VARCHAR(50),
        origVideoTransportAddress_Port INT,
        origRSVPAudioStat VARCHAR(64),
        origRSVPVideoStat VARCHAR(64),
        destLegIdentifier INT,
        destNodeId INT,
        destSpan INT,
        destIpAddr VARCHAR(50),
        originalCalledPartyNumber VARCHAR(50),
        finalCalledPartyNumber VARCHAR(50),
        finalCalledPartyUnicodeLoginUserID VARCHAR(128),
        destCause_location INT,
        destCause_value INT,
        destPrecedenceLevel INT,
        destMediaTransportAddress_IP VARCHAR(50),
        destMediaTransportAddress_Port INT,
        destMediaCap_payloadCapability INT,
        destMediaCap_maxFramesPerPacket INT,
        destMediaCap_g723BitRate INT,
        destVideoCap_Codec INT,
        destVideoCap_Bandwidth INT,
        destVideoCap_Resolution INT,
        destVideoTransportAddress_IP VARCHAR(50),
        destVideoTransportAddress_Port INT,
        destRSVPAudioStat VARCHAR(64),
        destRSVPVideoStat VARCHAR(64),
        dateTimeConnect INT,
        dateTimeDisconnect INT,
        lastRedirectDn VARCHAR(50),
        pkid VARCHAR(36),
        originalCalledPartyNumberPartition VARCHAR(50),
        callingPartyNumberPartition VARCHAR(50),
        finalCalledPartyNumberPartition VARCHAR(50),
        lastRedirectDnPartition VARCHAR(50),
        duration INT,
        origDeviceName VARCHAR(129),
        destDeviceName VARCHAR(129),
        origCallTerminationOnBehalfOf INT,
        destCallTerminationOnBehalfOf INT,
        origCalledPartyRedirectOnBehalfOf INT,
        lastRedirectRedirectOnBehalfOf INT,
        origCalledPartyRedirectReason INT,
        lastRedirectRedirectReason INT,
        destConversationId VARCHAR(50),
        globalCallId_ClusterID VARCHAR(50),
        joinOnBehalfOf INT,
        comment VARCHAR(2048),
        authCodeDescription VARCHAR(50),
        authorizationLevel INT,
        clientMatterCode VARCHAR(32),
        origDTMFMethod INT,
        destDTMFMethod INT,
        callSecuredStatus INT,
        origConversationId VARCHAR(32),
        origMediaCap_Bandwidth INT,
        destMediaCap_Bandwidth INT,
        authorizationCodeValue VARCHAR(50),
        outpulsedCallingPartyNumber VARCHAR(50),
        outpulsedCalledPartyNumber VARCHAR(50),
        origIpv4v6Addr VARCHAR(64),
        destIpv4v6Addr VARCHAR(64),
        origVideoCap_Codec_Channel2 INT,
        origVideoCap_Bandwidth_Channel2 INT,
        origVideoCap_Resolution_Channel2 INT,
        origVideoTransportAddress_IP_Channel2 VARCHAR(50),
        origVideoTransportAddress_Port_Channel2 INT,
        origVideoChannel_Role_Channel2 INT,
        destVideoCap_Codec_Channel2 INT,
        destVideoCap_Bandwidth_Channel2 INT,
        destVideoCap_Resolution_Channel2 INT,
        destVideoTransportAddress_IP_Channel2 VARCHAR(50),
        destVideoTransportAddress_Port_Channel2 INT,
        destVideoChannel_Role_Channel2 INT,
        IncomingProtocolID INT,
        IncomingProtocolCallRef VARCHAR(32),
        OutgoingProtocolID INT,
        OutgoingProtocolCallRef VARCHAR(32),
        currentRoutingReason INT,
        origRoutingReason INT,
        lastRedirectingRoutingReason INT,
        huntPilotPartition VARCHAR(50),
        huntPilotDN VARCHAR(50),
        calledPartyPatternUsage INT,
        IncomingICID VARCHAR(50),
        IncomingOrigIOI VARCHAR(50),
        IncomingTermIOI VARCHAR(50),
        OutgoingICID VARCHAR(50),
        OutgoingOrigIOI VARCHAR(50),
        OutgoingTermIOI VARCHAR(50),
        outpulsedOriginalCalledPartyNumber VARCHAR(50),
        outpulsedLastRedirectingNumber VARCHAR(50),
        wasCallQueued INT,
        totalWaitTimeInQueue INT,
        callingPartyNumber_uri VARCHAR(255),
        originalCalledPartyNumber_uri VARCHAR(255),
        finalCalledPartyNumber_uri VARCHAR(255),
        lastRedirectDn_uri VARCHAR(255),
        mobileCallingPartyNumber VARCHAR(50),
        finalMobileCalledPartyNumber VARCHAR(50),
        origMobileDeviceName VARCHAR(129),
        destMobileDeviceName VARCHAR(129),
        origMobileCallDuration INT,
        destMobileCallDuration INT,
        mobileCallType INT,
        originalCalledPartyPattern VARCHAR(50),
        finalCalledPartyPattern VARCHAR(50),
        lastRedirectingPartyPattern VARCHAR(50),
        huntPilotPattern VARCHAR(50),
        origDeviceType VARCHAR(100),
        destDeviceType VARCHAR(100),
        origDeviceSessionID VARCHAR(129),
        destDeviceSessionID VARCHAR(129),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_query)

# Function to insert CDR records into the database
def insert_cdr_record(cursor, record):
    # Convert empty strings to None (NULL in SQL)
    sanitized_record = {k: (None if v == '' else v) for k, v in record.items()}
    placeholders = ', '.join(['%s'] * len(sanitized_record))
    columns = ', '.join(sanitized_record.keys())
    sql = f"INSERT INTO cdr_records ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, list(sanitized_record.values()))

# Main function to parse the file and insert data
def process_cdr_files():
    try:
        # Change the working directory
        os.chdir('/path/to/cdr')

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create table if not exists
        create_table_if_not_exists(cursor)

        # Process each CDR file
        cdr_files = [f for f in os.listdir() if f.startswith('cdr_') and os.path.isfile(f)]
        for file_name in cdr_files:
            logging.info(f"Processing file: {file_name}")
            with open(file_name, mode='r') as file:
                csv_reader = csv.DictReader(file)
                header = next(csv_reader)  # Skip the header row
                if 'cdrRecordType' in header:
                    for row in csv_reader:
                        logging.debug(f"Processing row: {row}")
                        try:
                            insert_cdr_record(cursor, row)
                            logging.debug(f"Inserted row: {row}")
                        except Exception as e:
                            logging.error(f"Error inserting row: {row}, Error: {e}")
            
            # Delete the processed file
            os.remove(file_name)
            logging.info(f"Deleted file: {file_name}")

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()
        logging.info("Database connection closed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    process_cdr_files()

