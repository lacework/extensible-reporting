import pandas as pd
import datapane as dp
import numpy as np

def container_vulns_total_evaluated(container_vulns):
    df = pd.DataFrame(container_vulns)

    unique_containers = df['imageId'].nunique()

    return unique_containers
