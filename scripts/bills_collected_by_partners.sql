CREATE OR REPLACE VIEW `mesc`.`bills_collected_by_partners` AS
SELECT
    `bbd`.`collected_date` AS `collected_date`,
    `bbd`.`collected_bills` AS `collected_bills`,
    `bbd`.`amount` AS `amount`,
    `bbd`.`changed_by_fk` AS `changed_by_fk`,
    `ubr`.`first_name` AS `first_name`,
    `ubr`.`last_name` AS `last_name`,
    `ubr`.`username` AS `username`,
    `ubr`.`ref_code` AS `ref_code`,
    `ubr`.`role_id` AS `role_id`,
    `ubr`.`role` AS `role`,
    `bbd`.`collected_date` AS `id`
FROM
    (((
    SELECT
        date_format(`mesc`.`bills`.`changed_on`, '%Y-%m-%d 00:00:00') AS `collected_date`,
        count(`mesc`.`bills`.`id`) AS `collected_bills`,
        sum(`mesc`.`bills`.`grand_total`) AS `amount`,
        `mesc`.`bills`.`changed_by_fk` AS `changed_by_fk`
    FROM
        `mesc`.`bills`
    WHERE
        (`mesc`.`bills`.`is_billed` = 1)
    GROUP BY
        date_format(`mesc`.`bills`.`changed_on`, '%Y-%m-%d 00:00:00'),
        `mesc`.`bills`.`changed_by_fk`)) `bbd`
LEFT JOIN (
    SELECT
        `au`.`id` AS `id`,
        `au`.`first_name` AS `first_name`,
        `au`.`last_name` AS `last_name`,
        `au`.`username` AS `username`,
        `au`.`ref_code` AS `ref_code`,
        `ar`.`id` AS `role_id`,
        `ar`.`name` AS `role`
    FROM
        ((`mesc`.`ab_user` `au`
    LEFT JOIN `mesc`.`ab_user_role` `aur` ON
        ((`au`.`id` = `aur`.`user_id`)))
    LEFT JOIN `mesc`.`ab_role` `ar` ON
        ((`aur`.`role_id` = `ar`.`id`)))) `ubr` ON
    ((`bbd`.`changed_by_fk` = `ubr`.`id`)));
