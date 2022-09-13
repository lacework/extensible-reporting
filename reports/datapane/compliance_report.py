def generate_report(_shared, report_save_path, use_dummy_data):
    import datapane as dp
    
    lw_provider = _shared.p_lw_dummy if use_dummy_data else _shared.p_lw
    
    # get aws accounts
    integrations = lw_provider.integrations()
    aws_config_accounts = _shared.t_lw.integrations_config_accounts(integrations)

    # get compliance reports
    compliance_reports = lw_provider.compliance_reports(accounts=aws_config_accounts)
    
    report = dp.Report(
        "## Compliance Summary",
        dp.Table(_shared.t_lw.compliance_reports_summary(compliance_reports)),
        "## Compliance Report Raw",
        dp.Table(_shared.t_lw.compliance_reports_raw(compliance_reports))
    )

    report.save(path=report_save_path)
