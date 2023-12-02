# Created by alexander at 2023-11-04
Feature: Login
  # In order to access the dashboard and application features
  # users must be able to login to the application.

  Scenario: Valid Login
    Given I am anonymous
    And I am on the login page
    When I submit a valid login form
    Then I should be logged in
    And I should see the dashboard

  Scenario: Invalid Login
    Given I am anonymous
    And I am on the login page
    When I submit an invalid login form
    Then I should see the login form
    And I should see an error message

  Scenario: Already Logged In
    When I am logged in
    And I am on the login page
    Then I should be redirected to /entry/
    And I should see the dashboard
