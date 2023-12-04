# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.resourcebooking -t test_ressources.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.resourcebooking.testing.COLLECTIVE_RESOURCEBOOKING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/resourcebooking/tests/robot/test_ressources.robot
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

Scenario: As a site administrator I can add a Ressources
  Given a logged-in site administrator
    and an add RessourceBooking form
   When I type 'My Ressources' into the title field
    and I submit the form
   Then a Ressources with the title 'My Ressources' has been created

Scenario: As a site administrator I can view a Ressources
  Given a logged-in site administrator
    and a Ressources 'My Ressources'
   When I go to the Ressources view
   Then I can see the Ressources title 'My Ressources'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add RessourceBooking form
  Go To  ${PLONE_URL}/++add++RessourceBooking

a Ressources 'My Ressources'
  Create content  type=RessourceBooking  id=my-ressources  title=My Ressources

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Ressources view
  Go To  ${PLONE_URL}/my-ressources
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Ressources with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Ressources title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
