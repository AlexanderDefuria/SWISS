# Created by alexander at 2023-11-04
Feature: Registration
 # Enter feature description here

 Scenario: Accessing the registration page
   Given I am anonymous
   When I access the registration page
   Then I should see the registration form

 Scenario: Authenticated user accesses the registration page
   Given I am logged in
   When I access the registration page
   Then I should be redirected to /entry/
   And I should see the dashboard

 Scenario: Registering a new organization
   Given I am logged in
   When I access the registration page
   Then I should see the registration form
   When I register a new user
   And a new organization
   And click ""
   Then I should be redirected to /entry/
   And I should see the dashboard
