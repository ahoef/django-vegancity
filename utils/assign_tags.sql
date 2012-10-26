DROP FUNCTION add_cuisine_tag(varchar, varchar);

CREATE OR REPLACE FUNCTION add_cuisine_tag (
       vendor varchar, tag varchar
       ) RETURNS varchar as $$
       DECLARE
                var_vendor_id integer := (select id from vegancity_vendor where name=vendor);
                var_tag_id integer := (select id from vegancity_cuisinetag where name=tag);
                tag_already_entered boolean := exists (select id from vegancity_vendor_cuisine_tags
                                                      where vendor_id=var_vendor_id and
                                                      cuisinetag_id=var_tag_id);
       BEGIN
               IF tag_already_entered THEN
                                      return 'ALREADY ENTERED.  DID NOTHING';
                           END IF;
                IF exists (select id from vegancity_vendor where name=vendor) AND
                   exists (select id from vegancity_cuisinetag where name=tag) THEN
                             return 2;
                          END IF;
                RETURN 0;
        END;
        $$ LANGUAGE plpgsql;




select add_cuisine_tag('Mi Lah Vegetarian', 'salads');
select add_cuisine_tag('Mi Lah Vegetarian', 'chinese');
select add_cuisine_tag('Mi Lah Vegetarian', 'asian_fusion');
-- BEGIN;
-- insert into vegancity_vendor_cuisine_tags (vendor_id, cuisinetag_id)
-- select (select id from vegancity_vendor where name='Mi Lah Vegetarian'),
--        (select id from vegancity_cuisinetag where name='salads');
-- commit;
