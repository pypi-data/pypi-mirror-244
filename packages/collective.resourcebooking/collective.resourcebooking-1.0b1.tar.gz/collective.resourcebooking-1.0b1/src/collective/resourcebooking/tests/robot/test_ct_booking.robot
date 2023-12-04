# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.resourcebooking -t test_booking.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.resourcebooking.testing.COLLECTIVE_RESOURCEBOOKING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/resourcebooking/tests/robot/test_booking.robot
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

Scenario: As a site administrator I can add a Booking
  Given a logged-in site administrator
    and an add Bookings form
   When I type 'My Booking' into the title field
    and I submit the form
   Then a Booking with the title 'My Booking' has been created

Scenario: As a site administrator I can view a Booking
  Given a logged-in site administrator
    and a Booking 'My Booking'
   When I go to the Booking view
   Then I can see the Booking title 'My Booking'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Bookings form
  Go To  ${PLONE_URL}/++add++Bookings

a Booking 'My Booking'
  Create content  type=Bookings  id=my-booking  title=My Booking

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Booking view
  Go To  ${PLONE_URL}/my-booking
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Booking with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Booking title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
