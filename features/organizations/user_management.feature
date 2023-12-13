# Created by alexander at 2023-12-12
Feature: User Management
  # We should be able to view, edit, and delete users

  Scenario: A User has forgotten their password
    Given I am logged in
    And I am a Lead Scout
    And Another user exists
    When I access the user management page
    And I view the user
    Then I should be able to view the User's password

  Scenario: I want to disable a user
    Given I am logged in
    And I am a Lead Scout
    And Another user exists
    When I access the user management page
    And I view the user
    Then I should be able to disable the User
    And The user should be disabled