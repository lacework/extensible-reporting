def generate_report(_shared, report_save_path, use_cached_data):
    import datapane as dp
    
    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw

    host_vulns = lw_provider.host_vulns(_shared._25_hours_ago, _shared._now)

    # style
    host_vulns_summary_by_host = _shared.t_lw.host_vulns_summary_by_host(host_vulns)
    host_vulns_summary_by_host = host_vulns_summary_by_host.style.set_table_styles({"Severity Count" : [
        {
            "selector" :"td",
            "props": "white-space: pre-wrap; text-align:left"
        }
    ]})

    report = dp.Report(
        "## Total Evaluated Hosts",
        "* " + str(_shared.t_lw.host_vulns_total_evaluated(host_vulns)),
        "## Summary of total vulnerabilities",
        dp.Table(_shared.t_lw.host_vulns_summary(host_vulns)),
        "## Breakdown by host",
        dp.Table(host_vulns_summary_by_host),
        "## Full Export",
        dp.Table(_shared.t_lw.host_vulns_full_table(host_vulns))
    )

    report.save(path=report_save_path)
    