import json
import requests
import pandas as pd
from settings import GET_ENDPOINT, HEADERS


class GetUserSessions:

    def get_sessions(self):
        final_response = {}
        response = requests.get(GET_ENDPOINT, headers=HEADERS)
        dict_response = json.loads(response.content)
        df_response = pd.DataFrame(dict_response['activities'])
        df_response['first_seen_at'] = pd.to_datetime(df_response['first_seen_at'])
        df_response['answered_at'] = pd.to_datetime(df_response['answered_at'])
        df_response.sort_values(by=['user_id', 'first_seen_at'], ascending=[True, True], inplace=True)
        user_activities = []
        users_ids = df_response['user_id'].unique()
        final_response = {'user_sessions': {}}
        for user_id in users_ids:
            user_activities_list = []
            final_response['user_sessions'][user_id] = []
            user_session = []
            df_user_activities = df_response[df_response['user_id'] == user_id]
            df_user_activities.reset_index(inplace=True)
            elapsed_time = []
            for index, activity in df_user_activities.iterrows():
                if index < df_user_activities.shape[0] - 1:
                    elapsed_time.append({
                        'activity 1':
                            activity['id'],
                        'activity 2':
                            df_user_activities.iloc[index + 1]['id'],
                        'elapsed_time':
                            float((df_user_activities.iloc[index + 1]['first_seen_at'] - activity[
                                'answered_at']).seconds / 60)})
            session_activities = []
            started_at = None
            ended_at = None
            for time in elapsed_time:
                if time['elapsed_time'] > 5.0:
                    session_activities.append(time['activity 1'])
                    started_at = (df_user_activities[df_user_activities['id']
                                                     == session_activities[0]]['first_seen_at']).reset_index(
                        drop=True)
                    ended_at = (df_user_activities[df_user_activities['id'] ==
                                                   session_activities[len(session_activities) - 1]]['answered_at']) \
                        .reset_index(drop=True)
                    final_response['user_sessions'][user_id].append({'ended_at': pd.to_datetime(ended_at[0]).asm8.__str__(),
                                                                     'started_at': pd.to_datetime(started_at[0]).asm8.__str__(),
                                                                     'activity_ids': session_activities,
                                                                     'duration_seconds': float(
                                                                         (ended_at - started_at)[0].seconds)})
                    user_activities_list = []
                    started_at = None
                    ended_at = None
                    session_activities = []
                else:
                    session_activities.append(time['activity 1'])
        return json.dumps(final_response)
