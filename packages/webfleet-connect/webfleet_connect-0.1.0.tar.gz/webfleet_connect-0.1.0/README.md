# WebfleetConnect

![Webfleet logo](./webfleet_logo.svg)

#

Package to consume WEBFLEET.connect API.

[![PyPI version](https://badge.fury.io/py/webfleet-connect-python.svg)](https://badge.fury.io/py/webfleet-connect-python)

The WEBFLEET.connect API connects software appli­ca­tions with the Webfleet fleet management solution. Via WEBFLEET.connect you can enhance the value of all types of business solutions, including routing and scheduling optimization, ERP, Transport Management System (TMS), supply chain planning, asset management, and much more.

Check also the version for:

- [ruby](https://github.com/movomx/webfleet_connect)
- [javascript](https://github.com/movomx/webfleet_connect_js)

## Installation

Install it with:

    $ pip install webfleet_connect

## Usage

```python
from webfleet_connect import WebfleetConnect

webfleet_connect = WebfleetConnect.create()
response = webfleet_connect.show_object_report_extern()
response.to_hash() # [{:objectno=>"858EU4", :objectname=>"YRT-MMD2439", :objectclassname=>"sales", ...
```

`WebfleetConnect.create()` returns a new `Session` object which has the capabilities to request info from the WEBFLEET.connect API.

The Webfleet credential are taken from the env variables `WEBFLEET_CONNECT_ACCOUNT`, `WEBFLEET_CONNECT_USERNAME`, `WEBFLEET_CONNECT_PASSWORD` and `WEBFLEET_CONNECT_APIKEY` (if you want to know more about env variables check [this link](https://www.freecodecamp.org/news/python-env-vars-how-to-get-an-environment-variable-in-python/)).

If your system needs to work with multiple accounts or you need to specify the credentials dynamically for some other reason, you can do it this way:

```python
params = {
  'account': 'companyName',
  'username': 'dev',
  'password': 'VLm5PpiZST6U',
  'apikey': 'ZSksD88s-F7Uf'
}

webfleet_connect = WebfleetConnect.create(params)
```

When you use one of the methods of this gem, like for example `show_vehicle_report_extern`, this returns a `WebfleetConnectResponse` object which you can do:

```python
response = webfleet_connect.show_vehicle_report_extern()

response.url()         # gets the url to fetch the informtion from WEBFLEET.connect
response.status_code() # gets the status code of the request
response.str()         # returns the response message as plain text as is returned by WEBFLEET.connectby WEBFLEET.connect
response.to_hash()     # returns the data as a ruby Array/Hash object
```

The methods available in this package are the same that are documented in the [WEBFLEET.connect docs page](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html) just changed from cammelCase to snake_case. See below the list of methods.

### Params

In order to add params to a request is as easy as passing a hash of options in the request like:

```python
params = {
  'filterstring': 'ECO',
  'objectgroupname': 'Vehiculos',
  'ungroupedonly': True
}

response = webfleet_connect.show_vehicle_report_extern(params)
```

The `rangefrom_string` and `rangeto_string` can accept `Time` objects:

```python
from datetime import datetime, timedelta

start_date = datetime.now()
end_date = start_date + timedelta(days=1)

params = {
  'range_pattern': 'ud',
  'rangefrom_string': start_date,
  'rangeto_string': end_date
}

response = webfleet_connect.show_event_report_extern(params)
```

The `range_pattern` can accept the values:
`today`,
`yesterday`,
`two_days_ago`,
`three_days_ago`,
`four_days_ago`,
`five_days_ago`,
`six_days_ago`,
`current_week`,
`last_week`,
`two_weeks_ago`,
`three_weeks_ago`,
`floating_week`,
`last_floating_week`,
`two_floating_weeks_ago`,
`three_floating_weeks_ago`,
`current_month`,
`last_month`,
`two_months_ago`,
`three_months_ago`,
`user_defined_range`,
`ud`


```python
params = { 'range_pattern': 'today' }

response = webfleet_connect.show_event_report_extern(params)
```

### Extra config

The `WebfleetConnect::Session` object works with the default configuration:

`'lang': 'en', 'format': 'json', 'useUTF8': False, 'useISO8601': False`

but you can change the default configuration when you create the object:

```python
credentials = {
  'account': 'companyName',
  'username': 'dev',
  'password': 'VLm5PpiZST6U',
  'apikey': 'ZSksD88s-F7Uf'
}

config = {
  'lang': 'de',
  'format': 'csv',
  'useUTF8': True
}

params = credentials.update(config)

webfleet_connect = WebfleetConnect.create(params)
```

### Methods list

Mesage queues:

- [create_queue_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/createqueueextern.html)
- [delete_queue_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deletequeueextern.html)
- [pop_queue_messages_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/popqueuemessagesextern.html)
- [ack_queue_messages_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/ackqueuemessagesextern.html)

Objects:

- [show_object_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showobjectreportextern.html)
- [show_vehicle_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showvehiclereportextern.html)
- [show_nearest_vehicles](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/shownearestvehicles.html)
- [show_contracts](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showcontracts.html)
- [update_vehicle](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatevehicle.html)
- [show_object_groups](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showobjectgroups.html)
- [show_object_group_objects](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showobjectgroupobjects.html)
- [attach_object_to_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/attachobjecttogroup.html)
- [detach_object_from_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/detachobjectfromgroup.html)
- [insert_object_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertobjectgroup.html)
- [delete_object_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deleteobjectgroup.html)
- [update_object_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updateobjectgroup.html)
- [switch_output](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/switchoutput.html)
- [show_wakeup_timers](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showwakeuptimers.html)
- [update_wakeup_timers](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatewakeuptimers.html)
- [get_object_features](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getobjectfeatures.html)
- [update_contract_info](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatecontractinfo.html)
- [get_object_can_signals](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getobjectcansignals.html)
- [get_object_can_malfunctions](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getobjectcanmalfunctions.html)
- [get_electric_vehicle_data](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getelectricvehicledata.html)
- [get_active_asset_couplings](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getactiveassetcouplings.html)

Orders:

- [send_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/sendorderextern.html)
- [send_destination_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/senddestinationorderextern.html)
- [update_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updateorderextern.html)
- [update_destination_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatedestinationorderextern.html)
- [insert_destination_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertdestinationorderextern.html)
- [cancel_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/cancelorderextern.html)
- [assign_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/assignorderextern.html)
- [reassign_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/reassignorderextern.html)
- [delete_order_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deleteorderextern.html)
- [clear_orders_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/clearordersextern.html)
- [show_order_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showorderreportextern.html)
- [show_order_waypoints](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showorderwaypoints.html)

Messages:

- [send_text_message_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/sendtextmessageextern.html)
- [clear_text_messages_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/cleartextmessagesextern.html)
- [show_messages](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showmessages.html)
- [send_binary_message](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/sendbinarymessage.html)
- [reset_binary_messages](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/resetbinarymessages.html)
- [clear_binary_messages](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/clearbinarymessages.html)

Drivers:

- [show_driver_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showdriverreportextern.html)
- [insert_driver_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertdriverextern.html)
- [update_driver_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatedriverextern.html)
- [delete_driver_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deletedriverextern.html)
- [show_opti_drive_indicator](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showoptidriveindicator.html)
- [show_driver_groups](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showdrivergroups.html)
- [show_driver_group_drivers](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showdrivergroupdrivers.html)
- [attach_driver_to_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/attachdrivertogroup.html)
- [detach_driver_from_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/detachdriverfromgroup.html)
- [insert_driver_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertdrivergroup.html)
- [delete_driver_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deletedrivergroup.html)
- [update_driver_group](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatedrivergroup.html)
- [attach_driver_to_vehicle](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/attachdrivertovehicle.html)
- [detach_driver_from_vehicle](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/detachdriverfromvehicle.html)
- [get_driver_rdt_rules](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getdriverrdtrules.html)
- [update_driver_rdt_rules](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatedriverrdtrules.html)

Addresses:

- [show_address_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showaddressreportextern.html)
- [show_address_group_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showaddressgroupreportextern.html)
- [show_address_group_address_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showaddressgroupaddressreporte.html)
- [insert_address_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertaddressextern.html)
- [updateAddressExtern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updateaddressextern.html)
- [delete_address_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deleteaddressextern.html)
- [attach_address_to_group_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/attachaddresstogroupextern.html)
- [detach_address_from_group_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/detachaddressfromgroupextern.html)
- [insert_address_group_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertaddressgroupextern.html)
- [delete_address_group_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deleteaddressgroupextern.html)

Events:

- [show_event_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showeventreportextern.html)
- [acknowledge_event_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/acknowledgeeventextern.html)
- [resolve_event_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/resolveeventextern.html)
- [get_event_forward_configs](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/geteventforwardconfigs.html)
- [get_event_forward_config_recipients](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/geteventforwardconfigrecipient.html)
- [insert_event_forward_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/inserteventforwardconfig.html)
- [update_event_forward_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updateeventforwardconfig.html)
- [delete_event_forward_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deleteeventforwardconfig.html)

Trips and working times:

- [show_trip_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showtripreportextern.html)
- [show_trip_summary_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showtripsummaryreportextern.html)
- [show_tracks](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showtracks.html)
- [update_logbook](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatelogbook.html)
- [show_logbook](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showlogbook.html)
- [show_logbook_history](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showlogbookhistory.html)
- [update_logbook_mode](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatelogbookmode.html)
- [update_logbook_driver](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatelogbookdriver.html)
- [show_working_times](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showworkingtimes.html)
- [show_stand_stills](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showstandstills.html)
- [show_idle_exceptions](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showidleexceptions.html)
- [get_object_kpis](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getobjectkpis.html)
- [get_driver_kpis](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getdriverkpis.html)
- [get_remaining_driving_times_eu](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getremainingdrivingtimeseu.html)

Miscellaneous reports:

- [get_charger_connections](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getchargerconnections.html)
- [show_io_report_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showioreportextern.html)
- [show_acceleration_events](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showaccelerationevents.html)
- [show_speeding_events](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showspeedingevents.html)
- [show_digital_input_state_mileage](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showdigitalinputstatemileage.html)
- [get_charger_connections](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getchargerconnections.html)

Geocoding and routing:

- [geocode_address](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/geocodeaddress.html)
- [calc_route_simple_extern](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/calcroutesimpleextern.html)

Configuration and security:

- [show_settings](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showsettings.html)
- [create_session](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/createsession.html)
- [terminate_session](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/terminatesession.html)
- [show_account_order_states](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showaccountorderstates.html)
- [update_account_order_state](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updateaccountorderstate.html)
- [show_account_order_automations](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showaccountorderautomations.html)
- [update_account_order_automation](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updateaccountorderautomation.html)
- [get_account_status_messages](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getaccountstatusmessages.html)
- [get_status_messages](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getstatusmessages.html)
- [set_vehicle_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/setvehicleconfig.html)
- [get_vehicle_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getvehicleconfig.html)
- [set_status_messages](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/setstatusmessages.html)
- [set_account_status_messages](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/setaccountstatusmessages.html)

User management:

- [show_users](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showusers.html)
- [change_password](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/changepassword.html)

Vehicle maintenance:

- [insert_maintenance_schedule](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertmaintenanceschedule.html)
- [update_maintenance_schedule](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatemaintenanceschedule.html)
- [delete_maintenance_schedule](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deletemaintenanceschedule.html)
- [show_maintenance_schedules](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showmaintenanceschedules.html)
- [show_maintenance_tasks](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/showmaintenancetasks.html)
- [resolve_maintenance_task](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/resolvemaintenancetask.html)

Reporting:

- [get_archived_report_list](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getarchivedreportlist.html)
- [get_archived_report](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getarchivedreport.html)
- [delete_archived_report](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deletearchivedreport.html)
- [get_report_list](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getreportlist.html)
- [create_report](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/createreport.html)
- [send_report_via_mail](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/sendreportviamail.html)

Areas:

- [get_areas](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getareas.html)
- [insert_area](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertarea.html)
- [delete_area](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deletearea.html)
- [update_area](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/updatearea.html)
- [get_area_points](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getareapoints.html)
- [get_area_assignments](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getareaassignments.html)
- [insert_area_assignment](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertareaassignment.html)
- [delete_area_assignment](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deleteareaassignment.html)
- [get_area_schedules](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getareaschedules.html)
- [insert_area_schedule](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertareaschedule.html)
- [delete_area_schedule](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/deleteareaschedule.html)

LINK.connect:

- [send_aux_device_data](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/sendauxdevicedata.html)
- [get_local_aux_device_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getlocalauxdeviceconfig.html)
- [configure_local_aux_device](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/configurelocalauxdevice.html)
- [get_remote_aux_device_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/getremoteauxdeviceconfig.html)
- [configure_remote_aux_device](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/configureremoteauxdevice.html)
- [remove_remote_aux_device_config](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/removeremoteauxdeviceconfig.html)
- [clear_aux_device_data_queue](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/clearauxdevicedataqueue.html)
- [reset_aux_device_data](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/resetauxdevicedata.html)

Plugins:

- [insert_external_event](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/insertexternalevent.html)
- [set_external_object_data](https://www.webfleet.com/static/help/webfleet-connect/en_gb/index.html#data/setexternalobjectdata.html)
