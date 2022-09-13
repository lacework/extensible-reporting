def generate_report(_shared, report_save_path, use_dummy_data):
    import datapane as dp
    
    lw_provider = _shared.p_lw_dummy if use_dummy_data else _shared.p_lw

    events = lw_provider.events(_shared._7_days_ago, _shared._now)
    
    report = dp.Report(
        "## Events Raw",
        dp.Table(_shared.t_lw.events_raw(events,severities=["Critical", "High", "Medium"]))
    )

    report.save(path=report_save_path)
    