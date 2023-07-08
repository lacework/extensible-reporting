import pandas as pd
from logzero import logger
from datetime import *


class Secrets:

    def __init__(self, raw_data):

        self.data = raw_data['data']
        print(self.data)

    def count_secrets(self):
        return len(self.data)

    def processed_secrets(self):
        df = pd.DataFrame(self.data)
        df.rename(
            columns={'HOSTNAME': 'Hostname', 'FILE_PATH': 'File Path', 'SSH_KEY_TYPE': 'SSH Key Type'}, inplace=True)
        print(df)
        return df
