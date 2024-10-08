UPDATE Business
SET num_checkins = (
    SELECT COALESCE(SUM(Checkin.count), 0)
    FROM Checkin
    WHERE Checkin.business_id = Business.business_id
);

UPDATE Business
SET review_count = (
    SELECT COUNT(*)
    FROM Review
    WHERE Review.business_id = Business.business_id
);

UPDATE Business
SET review_rating = (
    SELECT AVG(stars)
    FROM Review
    WHERE Review.business_id = Business.business_id
);
