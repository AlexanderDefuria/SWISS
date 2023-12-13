# Created by alexander at 2023-12-12
Feature: Schedule
  # Enter feature description here

  Background:
    Given I am authenticated
    And We have a season
    And I access the home page
    When I click the Schedule tile on the dashboard

  Scenario: View match schedule
    Given lots of scheduled matches
    Then I should see a list of matches

  Scenario Outline: View scheduled match details
    Given a scheduled <status> match
    When I follow the match
    Then I should see the match details
    Examples:
      | status |
      | played |
      | unplayed |

  Scenario: Looking for more details of a team
    Given a scheduled unplayed match
    When I follow the match
    Then I should see the match details
    # Add team to context
    When I am interested in the first team
    # Click first team pill
    Then When I press on the first team pill
    # Move to glance
    Then I should see the team details
    And I should be redirected to 'entry/glance'