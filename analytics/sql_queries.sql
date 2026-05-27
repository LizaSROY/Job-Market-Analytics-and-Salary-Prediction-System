-- ==================================================
-- Job Market Analytics SQL
-- Database: job_market
-- ==================================================


-- 1. Average salary by country

SELECT
    country,
    COUNT(*) AS total_jobs,
    ROUND(
        AVG(salary),
        2
    ) AS average_salary

FROM job_market_clean

GROUP BY country

ORDER BY average_salary DESC;



-- 2. Top 10 occupations

SELECT
    occupation,
    COUNT(*) AS total_jobs,
    ROUND(
        AVG(salary),
        2
    ) AS average_salary

FROM job_market_clean

GROUP BY occupation

ORDER BY average_salary DESC

LIMIT 10;



-- 3. Salary by education level

SELECT
    education_level,

    COUNT(*) AS total_jobs,

    ROUND(
        AVG(salary),
        2
    ) AS average_salary

FROM job_market_clean

GROUP BY education_level

ORDER BY average_salary DESC;



-- 4. Experience level vs salary

SELECT
    experience_level,

    COUNT(*) AS total_jobs,

    ROUND(
        AVG(salary),
        2
    ) AS average_salary

FROM job_market_clean

GROUP BY experience_level

ORDER BY average_salary;



-- 5. Monthly hiring trend

SELECT
    year,
    month,

    COUNT(*) AS total_jobs

FROM job_market_clean

GROUP BY
    year,
    month

ORDER BY
    year,
    month;



-- 6. Top cities

SELECT
    city,
    country,

    COUNT(*) AS total_jobs

FROM job_market_clean

GROUP BY
    city,
    country

ORDER BY total_jobs DESC

LIMIT 10;



-- 7. Salary category distribution

SELECT
    salary_level,

    COUNT(*) AS total_jobs

FROM job_market_clean

GROUP BY salary_level;



-- 8. Company size analysis

SELECT
    company_size,

    COUNT(*) AS total_jobs,

    ROUND(
        AVG(salary),
        2
    ) AS average_salary

FROM job_market_clean

GROUP BY company_size

ORDER BY average_salary DESC;

