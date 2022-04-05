-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE street = 'Chamberlin Street' AND month = 7 AND day = 28;

SELECT * FROM airports;

SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28;
/*
---------------------------------------------------------------------------------------------------------------------------+
| 293 | 2021 | 7     | 28  | Axmark Road     | Vandalism took place at 12:04. No known witnesses.                                                                                                                                                                       |
| 294 | 2021 | 7     | 28  | Boyce Avenue    | Shoplifting took place at 03:01. Two people witnessed the event.                                                                                                                                                         |
| 295 | 2021 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
| 296 | 2021 | 7     | 28  | Widenius Street | Money laundering took place at 20:30. No known witnesses.                                                                                                                                                                |
| 297 | 2021 | 7     | 28  | Humphrey Street | Littering took place at 16:36. No known witnesses.                                                                                                                                                                       |
+-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
*/


SELECT * FROM interviews WHERE transcript LIKE '%bakery%' AND month = 7;

/*
+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 161 | Ruth    | 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
| 193 | Emma    | 2021 | 7     | 28  | I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour. They never bought anything.                                                                                                                                                                                 |
+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
*/
SELECT caller,receiver,duration FROM phone_calls WHERE month = 7 AND day = 28 AND duration <= 60 ORDER BY duration ASC;

/*
+----------------+----------------+----------+
|     caller     |    receiver    | duration |
+----------------+----------------+----------+
| (499) 555-9472 | (892) 555-8872 | 36       |
| (031) 555-6622 | (910) 555-3251 | 38       |
| (286) 555-6063 | (676) 555-6554 | 43       |
| (367) 555-5533 | (375) 555-8161 | 45       |
| (770) 555-1861 | (725) 555-3243 | 49       |
| (499) 555-9472 | (717) 555-1342 | 50       |
| (130) 555-0289 | (996) 555-8899 | 51       |
| (338) 555-6650 | (704) 555-2131 | 54       |
| (826) 555-1652 | (066) 555-9701 | 55       |
| (609) 555-5876 | (389) 555-5198 | 60       |
+----------------+----------------+----------+
*/

SELECT p.passport_number FROM passengers AS p WHERE p.flight_id IN (SELECT f.id FROM flights AS f WHERE f.month = 7 AND f.day = 29 AND f.origin_airport_id = 8);


SELECT DISTINCT name from people AS p
    INNER JOIN passengers AS p1 ON p1.passport_number = p.passport_number;

SELECT p.name FROM people AS p INNER JOIN bakery_security_logs AS b1 ON b1.license_plate IN (SELECT p.name FROM people INNER JOIN bank_accounts AS b ON b.person_id = p.id INNER JOIN atm_transactions as a ON a.account_number = b.account_number WHERE a.atm_location LIKE '%Leggett Street%' AND a.transaction_type LIKE '%withdraw%' AND a.month = 7 AND a.day = 28) AND p.passport_number IN (SELECT p.passport_number FROM passengers AS p1 WHERE p1.flight_id IN (SELECT f.id FROM flights AS f WHERE f.month = 7 AND f.day = 29 AND f.origin_airport_id = 8));

/*
+---------+
|  name   |
+---------+
| Bruce   |
| Diana   |
| Brooke  |
| Kenny   |
| Iman    |
| Luca    |
| Taylor  |
| Benista |
+---------+
*/

/*
+---------+
|  name   |
+---------+
| Kenny   |
| Iman    |
| Benista |
| Taylor  |
| Brooke  |
| Luca    |
| Diana   |
| Bruce   |
+---------+
*/

SELECT * FROM