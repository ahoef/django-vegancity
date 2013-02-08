BEGIN;
DELETE from vegancity_veglevel;
insert into vegancity_veglevel (name, description, super_category)
VALUES 

('vegan', '100% Vegan', 'Vegan'),
('veg_mostly_vegan', 'Vegetarian - Very Vegan Friendly', 'Vegetarian'),
('veg_several_vegan', 'Vegetarian - Several Vegan Options', 'Vegetarian'),
('veg_few_vegan', 'Vegetarian - Few Vegan Options', 'Vegetarian'),
('not_veg_very_vegan', 'Very Vegan Friendly', 'Non-Vegetarian'),
('not_veg_several_vegan', 'Several Vegan Options', 'Non-Vegetarian'),
('not_veg_few_vegan', 'Few Vegan Options', 'Non-Vegetarian'),
('beware','Beware!','Beware')
;


delete from vegancity_featuretag;
insert into vegancity_featuretag (name, description)
VALUES

('halal', 'Halal'),
('kosher', 'Kosher'),
('gluten_free_options', 'Gluten Free Options'),
('all_gluten_free', '100% Gluten Free'),
('gluten_free_desserts', 'Gluten Free Desserts'),
('vegan_desserts', 'Vegan Desserts'),
('fake_meat', 'Fake Meat'),
('cheese_steaks', 'Vegan Cheese Steaks'),
('sandwiches', 'Sandwiches'),
('coffeehouse', 'Coffeehouse'),
('food_cart', 'Food Cart'),
('cash_only', 'Cash Only'),
('delivery','Offers Delivery'),
('beer', 'Beer'),
('wine', 'Wine'),
('full_bar', 'Full Bar'),
('cheap', 'Cheap'),
('expensive', 'Expensive'),
('open_late', 'Open after 10pm'),
('smoothies', 'Smoothies/Juice Bar'),
('great_tea', 'Great Tea Selection'),
('byob', 'BYOB')
;

delete from vegancity_cuisinetag;
insert into vegancity_cuisinetag (name, description)
VALUES
('chinese', 'Chinese'),
('thai', 'Thai'),
('mexican', 'Mexican'),
('italian', 'Italian'),
('middle_eastern', 'Middle Eastern'),
('southern', 'Southern'),
('soul_food', 'Soul Food'),
('vietnamese', 'Vietnamese'),
('indian', 'Indian'),
('ethiopian', 'Ethiopian'),
('pizza', 'Pizza'),
('bar_food', 'Bar Food'),
('fast_food', 'Fast Food'),
('pan_asian', 'Pan-Asian'),
('sushi', 'Sushi'),
('japanese', 'Japanese'),
('asian_fusion', 'Asian Fusion'),
('barbecue', 'Barbecue'),
('bakery', 'Bakery'),
('diner', 'Diner'),
('dim_sum', 'Dim Sum'),
('gastropub', 'Gastropub'),
('moroccan', 'Moroccan'),
('pakistani', 'Pakistani'),
('salads', 'Salads'),
('tapas', 'Tapas'),
('greek', 'Greek'),
('korean', 'Korean'),
('turkish', 'Turkish'),
('american', 'American'),
('african', 'African'),
('caribbean', 'Caribbean'),
('cajun', 'Cajun'),
('burgers', 'Burgers')
;

COMMIT;

