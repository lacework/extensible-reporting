import providers.lacework as p_lw

import datapane as dp
import pandas as pd
import transformers.lacework as t_lw

def main():

    integrations = p_lw.integrations()
    
    report = dp.Report(
        "## Integrations AWS",
        t_lw.integrations_aws(integrations)
    )

    report.save(path="integrations-report.html")
    
main()