def generate_report(_shared, report_save_path, use_cached_data):
    import datapane as dp
    
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw

    integrations = lw_provider.integrations()

    report = dp.Report(
        "## Integrations AWS",
        dp.Table(_shared.t_lw.integrations_aws(integrations))
    )

    report.save(path=report_save_path)
    