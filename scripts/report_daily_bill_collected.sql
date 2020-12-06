CREATE VIEW report_daily_bill_collected AS SELECT STR_TO_DATE(DATE_FORMAT(changed_on, "%Y-%m-%d"), "%Y-%m-%d") AS "collected_date", COUNT(is_billed) AS "total" FROM bills 
WHERE is_billed = 1 GROUP BY STR_TO_DATE(DATE_FORMAT(changed_on, "%Y-%m-%d"), "%Y-%m-%d");
