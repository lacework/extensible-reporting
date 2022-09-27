def generate_report(_shared, report_save_path, use_cached_data):
    import datapane as dp

    lw_provider = _shared.p_lw_cached if use_cached_data else _shared.p_lw

    container_vulns = lw_provider.container_vulns(_shared._25_hours_ago,_shared._now)
    
    # style disabled due to large data set
    container_vulns_summary_by_image = _shared.t_lw.container_vulns_summary_by_image(container_vulns)
    # container_vulns_summary_by_image = container_vulns_summary_by_image.style.set_table_styles({"Severity Count" : [
    #     {
    #         "selector" :"td",
    #         "props": "white-space: pre-wrap; text-align:left"
    #     }],
    #     "Tags" : [
    #         {
    #             "selector" :"td",
    #             "props": "white-space: pre-wrap; text-align:left"
    #         }
    #     ]
    # })

    report = dp.Report(
        "## Summary by Severity",
        dp.Table(_shared.t_lw.container_vulns_summary(container_vulns)),
        "## Breakdown by Image",
        dp.DataTable(container_vulns_summary_by_image),
    )

    report.save(path=report_save_path)
