import numpy as np
import pandas as pd
from datetime import timedelta
from ddaptools.dda_constants import EDetermination
from ddaptools.dda_constants import RECIPIENT_NUMBER_ROW, SOURCEID_ROW, timestamp_client_local_ROW, DATEUTC_ROW, MONTH_ROW, MONTHNAME_ROW, WEEKDAY_ROW, WEEKDAYNAME_ROW, WEEK_NUMBER, DAYS_ROW, HOUR_ROW, MINUTES_ROW, DATE_ROW, TIMESLOT_ROW, OPERATION_ROW, APPLICATION_ROW, APPLICATIONTYPE_ROW, EVENTYPE_ROW, RECORD_NUMBER_ROW, OPERATIONTYPE_ROW, user_ESCAPE_DATES, user_WORK_WEEK_DAYS
from typing import List

# This should be enhancer instead. The idea that every enhancement just has different log settings available for it.


from pytz import timezone
import math, datetime, pytz
from dateutil import parser

class DateParser():
    """
    Dependencies: 
    
    import dateutil.parser as parser
    from datetime import datetime
    """
    def __init__(self, date, set_timezone="", comments=False, slot_splits=1):
        # Parse the date string into a datetime object
        localParsedDatetime = parser.parse(date)

        # Convert to the target timezone if specified
        if set_timezone:
            from_zone = pytz.timezone('UTC')
            target_tz = pytz.timezone(set_timezone)
            utc_parsed_date = localParsedDatetime.replace(tzinfo=from_zone)
            localParsedDatetime = utc_parsed_date.astimezone(target_tz)
        
        # Extract the date and time components
        time_tuple = localParsedDatetime.timetuple()

        
        def get_week_number(date):
            week_number = date.isocalendar()[1]
            return week_number

        # Set attributes for the various date components
        setattr(self, DATE_ROW, localParsedDatetime.strftime("%Y-%m-%d"))
        setattr(self, MONTH_ROW, time_tuple[1])
        setattr(self, MONTHNAME_ROW, datetime.datetime.strftime(localParsedDatetime, "%B"))
        setattr(self, WEEKDAY_ROW, time_tuple[6])
        setattr(self, WEEKDAYNAME_ROW, datetime.datetime.strftime(localParsedDatetime, "%a"))
        setattr(self, DAYS_ROW, time_tuple[2])
        setattr(self, HOUR_ROW, time_tuple[3])
        setattr(self, MINUTES_ROW, time_tuple[4])
        setattr(self, timestamp_client_local_ROW, localParsedDatetime.strftime("%Y-%m-%dT%X"))
        setattr(self, TIMESLOT_ROW, self.get_timeslot(slot_splits=slot_splits))
        setattr(self, WEEK_NUMBER, get_week_number(localParsedDatetime))

        
        self.timestamp_utc = localParsedDatetime.timestamp()

        # Optionally print the parsed datetime for debugging purposes
        if comments:
            print(f"Date field created with date:\n{date} -> Local {set_timezone} as:\n{localParsedDatetime}")
 
    def __str__(self):
        return str(list([self.date, "Month: ", self.monthNumber, self.monthName, "Weekday: ", self.weekdayNumber, self.weekdayName, "Time (UTC)", self.timeUTC, "Hour", self.hour]))
    
    def get_timeslot(self, slot_splits: int = 1):
        # Calculate the timeslot based on the given slot_splits
        slot_duration = 60/slot_splits
        return getattr(self, HOUR_ROW) * slot_splits + math.floor(getattr(self, MINUTES_ROW) / slot_duration)

    def get_values_as_list(self, datefields_toparse):
        # Return a list of attribute values for the specified date fields
        row_dict = {}
        for datefield in datefields_toparse:
            row_dict[datefield] = getattr(self, datefield)
        return row_dict.values()


class ConfigMapper:

    def __init__(self, configDict: dict, bucketDict: dict ):
        
        
        self.configDict = configDict #This is to be removed_as they dont actually makesense to have them here.
        self.bucketDict = bucketDict

        
        self.mappedDict = {} # To be populated with the mapped dict
        self.constants = {}
        self.mappedDF = pd.DataFrame()
        self.bucketMapper = {}
        self.createMappingDict()
        self.user_information_table = pd.DataFrame() #Employee Dataframe to extract information from. 


     # Static methods   
    def event_normalization( stagging_event: dict) -> List[dict]:
        """Events and batch information (relevant) are normalized

        Args:
            stagging_event (dict): Get the sample Stagign Event

        Returns:
            List[dict]: Returns as a list of normalized events.
        """
        KEY = 'key'
        RENAME = 'rename' # Indicates what the renamed result should be, if empty then it just means not to rename.
        instructions = [
            { KEY : 'guid', RENAME: 'staging_guid'},
            { KEY : 'version' },
            { KEY : 'organization_guid'}
        ] # Events form batch and how to conver thtem



        # add from stagging_events takes the events and adds the columns from batch from it.
        normalized_events = []
        # for each event in events push it as a dict with those values

        for event in stagging_event['details']:
            normalized_event = event.__dict__.copy()
            # print("Normalized Event", normalized_event)
            for instruction in instructions:
                if RENAME in instruction:
                    normalized_event[instruction[RENAME]] = stagging_event[instruction[KEY]]
                else:
                    normalized_event[instruction[KEY]] = stagging_event[instruction[KEY]]
        
            normalized_events.append(normalized_event)
        # print("Count of normalized events", len(normalized_events))
        return normalized_events

    def join_organization_fields(normalized_events: List[dict], user_information_table: List[dict], on="user_id") -> List[dict]:
        """
        Joins the employee information table with the table it has currently on the dataframe
        """
        # Create a dictionary to store employee information for quick lookups
        user_info_dict = {}
        for user_info in user_information_table:
            # remove the organization_id from the user_info
            user_info.pop("organization_guid")
            user_info_dict[user_info[on]] = user_info

        
        # Join the normalized events with the employee information using the user_guid field
        joined_events = []
        for event in normalized_events:
            user_id = event[on]
            print('user id search:', user_id)
            user_info = user_info_dict.get(user_id) # Fetches otherwise gets none. (wont run the following.)
            if user_info:
                joined_event = {**event, **user_info}
                joined_events.append(joined_event)
        
        return joined_events
        
    def event_population(event: dict):
        timestamp: datetime.datetime = parser.parse(event['timestamp']).replace(tzinfo=pytz.utc)
        timezone_str: str = event['user_timezone']
        local_timestamp: datetime.datetime = timestamp.astimezone(timezone(timezone_str))
        event['timestamp_local'] = local_timestamp.isoformat()
        event["local_timezone"] = timezone_str

        # Extract timeslot
        
        timeslot = (timestamp.hour * 60 + timestamp.minute) // 10
        timeslot_local = (local_timestamp.hour * 60 + local_timestamp.minute) // 10
        event['timeslot'] = timeslot
        event['timeslot_local'] = timeslot_local

        # Extract UTC date and time components
        event['hour'] = timestamp.hour
        event['minute'] = timestamp.minute
        event['day'] = timestamp.day
        event['month'] = timestamp.month
        event['year'] = timestamp.year
        event['week'] = timestamp.isocalendar()[1]
        event['weekday'] = timestamp.weekday()

        # Extract local date and time components
        event['hour_local'] = local_timestamp.hour
        event['minute_local'] = local_timestamp.minute
        event['day_local'] = local_timestamp.day
        event['month_local'] = local_timestamp.month
        event['year_local'] = local_timestamp.year
        event['week_local'] = local_timestamp.isocalendar()[1]
        event['weekday_local'] = local_timestamp.weekday()


        duration = event["duration"]
            
        if(duration is not None and event["end_time"] is None ):
            duration_seconds = timedelta(seconds=duration)
            end_time = timestamp + duration_seconds
            event['end_time'] = end_time.isoformat()


        # Check if end_time is None
        if event['end_time'] is not None:
            # Convert end_time to datetime object
            endtime = parser.parse(event['end_time'])

            # Convert timestamp and end_time to the specified timezone
            local_endtime = endtime.astimezone(timezone(timezone_str))

            # Populate the timestamp_local, end_time_local, and duration fields as isoformat strings
            event['end_time_local'] = local_endtime.isoformat()
            event['duration'] = (endtime - timestamp).total_seconds()
        else:
            # If end_time is None, set the remaining fields to None as well
            event['end_time'] = None
            event['end_time_local'] = None
            # TODO CHANGE
            event["duration"] = 0 if event["duration"] is None else event["duration"]

    def date_related_population(join_events: List[dict]) -> List[dict]:
        """
        For each of the events, populate the date-related items.
        Probably for some toher events will just that be the case.
        """
        for event in join_events:
            # print("Attempting date_related", event)
            # Convert timestamp to datetime object
            try:
                ConfigMapper.event_population(event)
                continue
            except Exception as e:
                print(e)
                print(event)
        return join_events

    def mapping_application(date_mapped_events_df: pd.core.frame.DataFrame, bucket_instructions: dict)->pd.core.frame.DataFrame:
        """maps application column, receives general business instruction.

        Args:
            date_mapped_events_df (pd.core.frame.DataFrame): _description_
            bucket_instructions (dict): {
            "operation": {
                "description": "Bucket that maps into different activity categories: https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema",
                "buckets": {
                "Create": "Create",
                "New-Mailbox": "Create",
                ...
                }
            },
            "application_type": {
                "description":"Bucket that maps Application Mapper",
                "buckets": {
                "Exchange":"Email",
                ...
                }
            }
            }

        Returns:
            pd.core.frame.DataFrame: _description_
        """
        bucket_instructions:dict = bucket_instructions[APPLICATIONTYPE_ROW]["buckets"]
        return ConfigMapper.mapping_job(date_mapped_events_df=date_mapped_events_df, mapping_instruction = bucket_instructions, target_row=APPLICATION_ROW, result_row = APPLICATIONTYPE_ROW)
        
    def mapping_operation(date_mapped_events_df: pd.core.frame.DataFrame, bucket_instructions: dict)->pd.core.frame.DataFrame:
        bucket_instructions:dict = bucket_instructions[OPERATION_ROW]["buckets"]
        return ConfigMapper.mapping_job(date_mapped_events_df=date_mapped_events_df, mapping_instruction = bucket_instructions, target_row=OPERATION_ROW, result_row=OPERATIONTYPE_ROW)
        
    def mapping_job(date_mapped_events_df: pd.core.frame.DataFrame, mapping_instruction: dict, target_row: str, result_row: str) -> pd.core.frame.DataFrame:
        """Classifies based on the specific bucket mapping for the code.

        Args:
            date_mapped_event (List[dict]): [{Event...., application: "Word"}]
            mapping_instructions (dict):  {
                "description":"Bucket that maps Application Mapper",
                "buckets": {
                "Exchange":"Email",
                "MicrosftTeams": "Chat",
                "Word": "Editor",
                "SharePoint": "Files",
                "OneDrive": "Files",
                "SecurityComplianceCenter": "Authentication",
                "AzureActiveDirectory": "Authentication"
                
            }
            target_row: str
        Returns:
            classified_events: List[dict]
        """
        # Iterate every event and replace all cases where target_row is x 

        date_mapped_events_df[result_row] = date_mapped_events_df[target_row].replace(mapping_instruction)
        return date_mapped_events_df

    def classify_events(date_mapped_events_df: pd.core.frame.DataFrame)->pd.core.frame.DataFrame:
        """

        Args:
            date_mapped_events (pd.core.frame.DataFrame): _description_
            
        Res: 
            (pd.core.frame.DataFrame): Pandas Core Dataframe

        """

        def classifyEventType(dfRow: dict, strategy="ARRAY")->str:
                """
                Takes an individual DF Row and produces the proper response
                """
                hours_start = "user_work_hours_start"
                hours_end = "user_work_hours_end"

                # for DICT strategy
                user_work_settings = "user_work_settings"
                
                weekday = int(dfRow[WEEKDAY_ROW])
                # print("weekday", weekday)

                # # print("Failing at", weekday, dfRow[hours_start], "from", dfRow)
                try:
                    if(strategy == "ARRAY"):
                        if(dfRow[WEEKDAY_ROW] not in dfRow[user_WORK_WEEK_DAYS]):
                            return EDetermination.WEEKENDS.value

                        elif(dfRow[DATE_ROW] in dfRow[user_ESCAPE_DATES]):
                            return EDetermination.DAYOFF.value

                        
                        elif not (dfRow[hours_start][weekday] == 0 and dfRow[hours_end][weekday] == 0):
                            if(dfRow[HOUR_ROW] < dfRow[hours_start][weekday] or dfRow[HOUR_ROW] > dfRow[hours_end][weekday]):
                                return EDetermination.AFTERHOURS.value
                    elif(strategy == "DICT"):
                        work_settings = dfRow[user_work_settings]
                        


                except Exception as e:
                    print("Failing at", weekday, dfRow[hours_start], "from", dfRow)

                return EDetermination.WORKHOURS.value

        date_mapped_events_df[EVENTYPE_ROW] = date_mapped_events_df.apply(classifyEventType, axis=1)

        return date_mapped_events_df
    
    def categorization_jobs(date_mapped_events: List[dict])->List[dict]:
        """

        Args:
            date_mapped_events (List[dict]): _description_
            
        Res: 
            (List[dict]): Pandas Core Dataframe

        """
        date_mapped_events_df = pd.DataFrame(date_mapped_events)
        bucket_instructions = {
             "operation": {
                "description": "Bucket that maps into different activity categories: https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema",
                "buckets": {
                "Create": "Create",
                "New-Mailbox": "Create",
                "MipLabel": "Admin",
                "FolderRecycled": "Admin",
                "AddedToGroup": "Admin",
                "SharingPolicyChanged": "Admin",
                "UserLoggedIn": "Login",
                "FolderCreated": "Organize",
                "FolderRenamed": "Organize",
                "FileRenamed": "Organize",
                "GroupAdded": "Organize",
                "FileDownloaded": "Download",
                "FileAccessed": "Read",
                "FilePreviewed": "Read",
                "PageViewed": "Read",
                "FileAccessedExtended": "Read",
                "SoftDelete": "Delete",
                "MoveToDeletedItems": "Delete",
                "HardDelete": "Delete",
                "SearchQueryPerformed": "Search",
                "FileModified": "Update",
                "FileUploaded": "Update",
                "FolderModified": "Update",
                "FileModifiedExtended": "Update"
                }
            },
            "application_type": {
                "description":"Bucket that maps Application Mapper",
                "buckets": {
                "Exchange":"Email",
                "MicrosftTeams": "Chat",
                "Word": "Editor",
                "SharePoint": "Files",
                "OneDrive": "Files",
                "SecurityComplianceCenter": "Authentication",
                "AzureActiveDirectory": "Authentication"
                }
            }
        }

    
        # classified_events: pd.core.frame.DataFrame = ConfigMapper.classify_events(date_mapped_events_df=date_mapped_events_df)
        # classified_events: pd.core.frame.DataFrame = ConfigMapper.mapping_application(date_mapped_events_df=classified_events, bucket_instructions=bucket_instructions)
        # classified_dicts = classified_events.to_dict(orient="records")
        classified_dicts = date_mapped_events_df.to_dict(orient="records")
        # print("Classified Events: ", classified_dicts)
        return classified_dicts

    def dfEnhancement(self):
        
        # print("DF Enhancement activated using: ", self.mappedDF.columns )
        DATEFIELDS_TOPARSE = [MONTH_ROW, MONTHNAME_ROW, WEEKDAY_ROW, WEEKDAYNAME_ROW, DAYS_ROW , HOUR_ROW, MINUTES_ROW ,DATE_ROW, timestamp_client_local_ROW, TIMESLOT_ROW]

        
        def datetimePopulation(dfRow)->str:
            date = dfRow["start_time"]
            dt = DateParser(date, set_timezone=dfRow["user_timezone"], slot_splits=dfRow["user_time_slot_split"])
            return dt.getValuesAsList(DATEFIELDS_TOPARSE)

        def classifyEventType(dfRow)->str:
            """
            Takes an individual DF Row and produces the proper response
            """
            hours_start = "user_work_hours_start"
            hours_end = "user_work_hours_end"
            
            weekday = int(dfRow[WEEKDAY_ROW])
            if(dfRow[WEEKDAY_ROW] not in dfRow["user_work_days"]):
                return EDetermination.WEEKENDS.value

            # 
            elif(dfRow[DATE_ROW] in self.employeeData.escape_dates):
                return EDetermination.DAYOFF.value

            # If the time is earlier or later than the regular workday, then this is marked as afterhours
            elif not (dfRow[hours_start][weekday] == 0 and dfRow[hours_end][weekday] == 0):
                if(dfRow[HOUR_ROW] < dfRow[hours_start][weekday] or dfRow[HOUR_ROW] > dfRow[hours_end][weekday]):
                    return EDetermination.AFTERHOURS.value
            

            return EDetermination.WORKHOURS.value # For now just return the date to prove that successfullmapping can be done.

        for operationKey in self.configDict.keys():
            
            if operationKey == "map":
                for functionName in self.configDict[operationKey].keys():
                    toReplaceRow = self.configDict[operationKey][functionName]
                    self.mappedDF[functionName] = self.mappedDF[toReplaceRow]

            if operationKey == "bucket":
                for functionName in self.configDict[operationKey].keys():
                    
                    toReplaceRow = self.configDict[operationKey][functionName]
                    # print("Looping for function bucket key: ", functionName)
                    if functionName == OPERATION_ROW:
                        # di = {1: "A", 2: "B", "MipLabel": "Admin"}
                        di = self.bucketDict[OPERATION_ROW]["buckets"]
                        self.mappedDF[functionName] = self.mappedDF[toReplaceRow].replace(di)

                    if functionName == APPLICATIONTYPE_ROW:
                        di = self.bucketDict[APPLICATIONTYPE_ROW]["buckets"]
                        # print("Application Mapping for: ", APPLICATIONTYPE_ROW , "Using",  APPLICATION_ROW, di)
                        self.mappedDF[functionName] = self.mappedDF[toReplaceRow].replace(di)
                    

            if operationKey == "functions":
                for functionName in self.configDict[operationKey].keys():
                    # # print("Operation Running:", functionName)
                    if functionName == timestamp_client_local_ROW:
                        zipResults = zip(*self.mappedDF.apply(datetimePopulation, axis=1))
                        self.mappedDF[MONTH_ROW], self.mappedDF[MONTHNAME_ROW], self.mappedDF[WEEKDAY_ROW], self.mappedDF[WEEKDAYNAME_ROW], self.mappedDF[DAYS_ROW], self.mappedDF[HOUR_ROW], self.mappedDF[MINUTES_ROW],  self.mappedDF[DATE_ROW], self.mappedDF[timestamp_client_local_ROW], self.mappedDF[TIMESLOT_ROW] = zipResults
                    elif functionName == EVENTYPE_ROW:
                        self.mappedDF[EVENTYPE_ROW] = self.mappedDF.apply(classifyEventType, axis=1)

    def createMappingDict(self):
        """
        Initializes everything as a dictionary to later use for mapping
        From:
        {a: [x, y, z]} => {x: a, y: a, z: a}
        """
        # Loop for each bucketSetting, and each nested key to create the dictionary
        for bucketType in self.bucketDict.keys():
            targetBucket = self.bucketDict[bucketType]["buckets"]
            self.bucketMapper[bucketType] = {}
            for mapValue in targetBucket.keys():
                for mapKey in targetBucket[mapValue]:
                    self.bucketMapper[bucketType][mapKey] = mapValue












