# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.resourcebooking -t test_bookings.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.resourcebooking.testing.COLLECTIVE_RESOURCEBOOKING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/resourcebooking/tests/robot/test_bookings.robot
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

Scenario: As a site administrator I can add a Bookings
  Given a logged-in site administrator
    and an add RessourceBooking form
   When I type 'My Bookings' into the title field
    and I submit the form
   Then a Bookings with the title 'My Bookings' has been created

Scenario: As a site administrator I can view a Bookings
  Given a logged-in site administrator
    and a Bookings 'My Bookings'
   When I go to the Bookings view
   Then I can see the Bookings title 'My Bookings'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add RessourceBooking form
  Go To  ${PLONE_URL}/++add++RessourceBooking

a Bookings 'My Bookings'
  Create content  type=RessourceBooking  id=my-bookings  title=My Bookings

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Bookings view
  Go To  ${PLONE_URL}/my-bookings
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Bookings with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Bookings title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
