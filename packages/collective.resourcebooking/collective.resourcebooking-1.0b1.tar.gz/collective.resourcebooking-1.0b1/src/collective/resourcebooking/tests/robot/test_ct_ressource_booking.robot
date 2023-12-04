# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.resourcebooking -t test_ressource_booking.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.resourcebooking.testing.COLLECTIVE_RESOURCEBOOKING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/resourcebooking/tests/robot/test_ressource_booking.robot
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

Scenario: As a site administrator I can add a RessourceBooking
  Given a logged-in site administrator
    and an add RessourceBooking form
   When I type 'My RessourceBooking' into the title field
    and I submit the form
   Then a RessourceBooking with the title 'My RessourceBooking' has been created

Scenario: As a site administrator I can view a RessourceBooking
  Given a logged-in site administrator
    and a RessourceBooking 'My RessourceBooking'
   When I go to the RessourceBooking view
   Then I can see the RessourceBooking title 'My RessourceBooking'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add RessourceBooking form
  Go To  ${PLONE_URL}/++add++RessourceBooking

a RessourceBooking 'My RessourceBooking'
  Create content  type=RessourceBooking  id=my-ressource_booking  title=My RessourceBooking

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the RessourceBooking view
  Go To  ${PLONE_URL}/my-ressource_booking
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a RessourceBooking with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the RessourceBooking title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
