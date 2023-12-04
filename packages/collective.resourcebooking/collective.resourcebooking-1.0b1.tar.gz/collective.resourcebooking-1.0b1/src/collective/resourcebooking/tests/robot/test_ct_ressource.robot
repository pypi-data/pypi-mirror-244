# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.resourcebooking -t test_ressource.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.resourcebooking.testing.COLLECTIVE_RESOURCEBOOKING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/resourcebooking/tests/robot/test_ressource.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Ressource
  Given a logged-in site administrator
    and an add Ressources form
   When I type 'My Ressource' into the title field
    and I submit the form
   Then a Ressource with the title 'My Ressource' has been created

Scenario: As a site administrator I can view a Ressource
  Given a logged-in site administrator
    and a Ressource 'My Ressource'
   When I go to the Ressource view
   Then I can see the Ressource title 'My Ressource'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Ressources form
  Go To  ${PLONE_URL}/++add++Ressources

a Ressource 'My Ressource'
  Create content  type=Ressources  id=my-ressource  title=My Ressource

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Ressource view
  Go To  ${PLONE_URL}/my-ressource
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Ressource with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Ressource title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
