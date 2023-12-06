from connection import Connection
from actions.action import Action

class Session:
  def __init__(self, credentials, config):
    self._credentials = credentials
    self._config = config
    self._connection = Connection()

  def has_json(self):
    return self.config.has_json()
  
  def _exec(self, action):
    return self._connection.exec(self._url(action))

  def _url(self, action):
    return f'{self._config.str()}&{self._credentials.str()}&{action.str()}'

  def create_queue_extern(self, args):
    action = Action('createQueueExtern', args)
    return self._exec(action)

  def delete_queue_extern(self, args):
    action = Action('deleteQueueExtern', args)
    return self._exec(action)

  def pop_queue_messages_extern(self, args):
    action = Action('popQueueMessagesExtern', args)
    return self._exec(action)

  def ack_queue_messages_extern(self, args):
    action = Action('ackQueueMessagesExtern', args)
    return self._exec(action)

  def show_object_report_extern(self, args):
    action = Action('showObjectReportExtern', args)
    return self._exec(action)

  def show_vehicle_report_extern(self, args):
    action = Action('showVehicleReportExtern', args)
    return self._exec(action)

  def show_nearest_vehicles(self, args):
    action = Action('showNearestVehicles', args)
    return self._exec(action)

  def show_contracts(self, args):
    action = Action('showContracts', args)
    return self._exec(action)

  def update_vehicle(self, args):
    action = Action('updateVehicle', args)
    return self._exec(action)

  def show_object_groups(self, args):
    action = Action('showObjectGroups', args)
    return self._exec(action)

  def show_object_group_objects(self, args):
    action = Action('showObjectGroupObjects', args)
    return self._exec(action)

  def attach_object_to_group(self, args):
    action = Action('attachObjectToGroup', args)
    return self._exec(action)

  def detach_object_from_group(self, args):
    action = Action('detachObjectFromGroup', args)
    return self._exec(action)

  def insert_object_group(self, args):
    action = Action('insertObjectGroup', args)
    return self._exec(action)

  def delete_object_group(self, args):
    action = Action('deleteObjectGroup', args)
    return self._exec(action)

  def update_object_group(self, args):
    action = Action('updateObjectGroup', args)
    return self._exec(action)

  def switch_output(self, args):
    action = Action('switchOutput', args)
    return self._exec(action)

  def show_wakeup_timers(self, args):
    action = Action('showWakeupTimers', args)
    return self._exec(action)

  def update_wakeup_timers(self, args):
    action = Action('updateWakeupTimers', args)
    return self._exec(action)

  def get_object_features(self, args):
    action = Action('getObjectFeatures', args)
    return self._exec(action)

  def update_contract_info(self, args):
    action = Action('updateContractInfo', args)
    return self._exec(action)

  def get_object_can_signals(self, args):
    action = Action('getObjectCanSignals', args)
    return self._exec(action)

  def get_object_can_malfunctions(self, args):
    action = Action('getObjectCanMalfunctions', args)
    return self._exec(action)

  def get_electric_vehicle_data(self, args):
    action = Action('getElectricVehicleData', args)
    return self._exec(action)

  def get_active_asset_couplings(self, args):
    action = Action('getActiveAssetCouplings', args)
    return self._exec(action)

  def send_order_extern(self, args):
    action = Action('sendOrderExtern', args)
    return self._exec(action)

  def send_destination_order_extern(self, args):
    action = Action('sendDestinationOrderExtern', args)
    return self._exec(action)

  def update_order_extern(self, args):
    action = Action('updateOrderExtern', args)
    return self._exec(action)

  def update_destination_order_extern(self, args):
    action = Action('updateDestinationOrderExtern', args)
    return self._exec(action)

  def insert_destination_order_extern(self, args):
    action = Action('insertDestinationOrderExtern', args)
    return self._exec(action)

  def cancel_order_extern(self, args):
    action = Action('cancelOrderExtern', args)
    return self._exec(action)

  def assign_order_extern(self, args):
    action = Action('assignOrderExtern', args)
    return self._exec(action)

  def reassign_order_extern(self, args):
    action = Action('reassignOrderExtern', args)
    return self._exec(action)

  def delete_order_extern(self, args):
    action = Action('deleteOrderExtern', args)
    return self._exec(action)

  def clear_orders_extern(self, args):
    action = Action('clearOrdersExtern', args)
    return self._exec(action)

  def show_order_report_extern(self, args):
    action = Action('showOrderReportExtern', args)
    return self._exec(action)

  def show_order_waypoints(self, args):
    action = Action('showOrderWaypoints', args)
    return self._exec(action)

  def send_text_message_extern(self, args):
    action = Action('sendTextMessageExtern', args)
    return self._exec(action)

  def clear_text_messages_extern(self, args):
    action = Action('clearTextMessagesExtern', args)
    return self._exec(action)

  def show_messages(self, args):
    action = Action('showMessages', args)
    return self._exec(action)

  def send_binary_message(self, args):
    action = Action('sendBinaryMessage', args)
    return self._exec(action)

  def reset_binary_messages(self, args):
    action = Action('resetBinaryMessages', args)
    return self._exec(action)

  def clear_binary_messages(self, args):
    action = Action('clearBinaryMessages', args)
    return self._exec(action)

  def show_driver_report_extern(self, args):
    action = Action('showDriverReportExtern', args)
    return self._exec(action)

  def insert_driver_extern(self, args):
    action = Action('insertDriverExtern', args)
    return self._exec(action)

  def update_driver_extern(self, args):
    action = Action('updateDriverExtern', args)
    return self._exec(action)

  def delete_driver_extern(self, args):
    action = Action('deleteDriverExtern', args)
    return self._exec(action)

  def show_opti_drive_indicator(self, args):
    action = Action('showOptiDriveIndicator', args)
    return self._exec(action)

  def show_driver_groups(self, args):
    action = Action('showDriverGroups', args)
    return self._exec(action)

  def show_driver_group_drivers(self, args):
    action = Action('showDriverGroupDrivers', args)
    return self._exec(action)

  def attach_driver_to_group(self, args):
    action = Action('attachDriverToGroup', args)
    return self._exec(action)

  def detach_driver_from_group(self, args):
    action = Action('detachDriverFromGroup', args)
    return self._exec(action)

  def insert_driver_group(self, args):
    action = Action('insertDriverGroup', args)
    return self._exec(action)

  def delete_driver_group(self, args):
    action = Action('deleteDriverGroup', args)
    return self._exec(action)

  def update_driver_group(self, args):
    action = Action('updateDriverGroup', args)
    return self._exec(action)

  def attach_driver_to_vehicle(self, args):
    action = Action('attachDriverToVehicle', args)
    return self._exec(action)

  def detach_driver_from_vehicle(self, args):
    action = Action('detachDriverFromVehicle', args)
    return self._exec(action)

  def get_driver_rdt_rules(self, args):
    action = Action('getDriverRdtRules', args)
    return self._exec(action)

  def update_driver_rdt_rules(self, args):
    action = Action('updateDriverRdtRules', args)
    return self._exec(action)

  def show_address_report_extern(self, args):
    action = Action('showAddressReportExtern', args)
    return self._exec(action)

  def show_address_group_report_extern(self, args):
    action = Action('showAddressGroupReportExtern', args)
    return self._exec(action)

  def show_address_group_address_report_extern(self, args):
    action = Action('showAddressGroupAddressReportExtern', args)
    return self._exec(action)

  def insert_address_extern(self, args):
    action = Action('insertAddressExtern', args)
    return self._exec(action)

  def updateAddressExtern(self, args):
    action = Action('updateAddressExtern', args)
    return self._exec(action)

  def delete_address_extern(self, args):
    action = Action('deleteAddressExtern', args)
    return self._exec(action)

  def attach_address_to_group_extern(self, args):
    action = Action('attachAddressToGroupExtern', args)
    return self._exec(action)

  def detach_address_from_group_extern(self, args):
    action = Action('detachAddressFromGroupExtern', args)
    return self._exec(action)

  def insert_address_group_extern(self, args):
    action = Action('insertAddressGroupExtern', args)
    return self._exec(action)

  def delete_address_group_extern(self, args):
    action = Action('deleteAddressGroupExtern', args)
    return self._exec(action)

  def show_event_report_extern(self, args):
    action = Action('showEventReportExtern', args)
    return self._exec(action)

  def acknowledge_event_extern(self, args):
    action = Action('acknowledgeEventExtern', args)
    return self._exec(action)

  def resolve_event_extern(self, args):
    action = Action('resolveEventExtern', args)
    return self._exec(action)

  def get_event_forward_configs(self, args):
    action = Action('getEventForwardConfigs', args)
    return self._exec(action)

  def get_event_forward_config_recipients(self, args):
    action = Action('getEventForwardConfigRecipients', args)
    return self._exec(action)

  def insert_event_forward_config(self, args):
    action = Action('insertEventForwardConfig', args)
    return self._exec(action)

  def update_event_forward_config(self, args):
    action = Action('updateEventForwardConfig', args)
    return self._exec(action)

  def delete_event_forward_config(self, args):
    action = Action('deleteEventForwardConfig', args)
    return self._exec(action)

  def show_trip_report_extern(self, args):
    action = Action('showTripReportExtern', args)
    return self._exec(action)

  def show_trip_summary_report_extern(self, args):
    action = Action('showTripSummaryReportExtern', args)
    return self._exec(action)

  def show_tracks(self, args):
    action = Action('showTracks', args)
    return self._exec(action)

  def update_logbook(self, args):
    action = Action('updateLogbook', args)
    return self._exec(action)

  def show_logbook(self, args):
    action = Action('showLogbook', args)
    return self._exec(action)

  def show_logbook_history(self, args):
    action = Action('showLogbook_history', args)
    return self._exec(action)

  def update_logbook_mode(self, args):
    action = Action('updateLogbookMode', args)
    return self._exec(action)

  def update_logbook_driver(self, args):
    action = Action('updateLogbookDriver', args)
    return self._exec(action)

  def show_working_times(self, args):
    action = Action('showWorkingTimes', args)
    return self._exec(action)

  def show_stand_stills(self, args):
    action = Action('showStandStills', args)
    return self._exec(action)

  def show_idle_exceptions(self, args):
    action = Action('showIdleExceptions', args)
    return self._exec(action)

  def get_object_kpis(self, args):
    action = Action('getObjectKpis', args)
    return self._exec(action)

  def get_driver_kpis(self, args):
    action = Action('getDriverKpis', args)
    return self._exec(action)

  def get_remaining_driving_times_eu(self, args):
    action = Action('getRemainingDrivingTimesEu', args)
    return self._exec(action)

  def get_charger_connections(self, args):
    action = Action('getChargerConnections', args)
    return self._exec(action)

  def show_io_report_extern(self, args):
    action = Action('showIoReportExtern', args)
    return self._exec(action)

  def show_acceleration_events(self, args):
    action = Action('showAccelerationEvents', args)
    return self._exec(action)

  def show_speeding_events(self, args):
    action = Action('showSpeedingEvents', args)
    return self._exec(action)

  def show_digital_input_state_mileage(self, args):
    action = Action('showDigitalInputStateMileage', args)
    return self._exec(action)

  def get_charger_connections(self, args):
    action = Action('getChargerConnections', args)
    return self._exec(action)

  def geocode_address(self, args):
    action = Action('geocodeAddress', args)
    return self._exec(action)

  def calc_route_simple_extern(self, args):
    action = Action('calcRouteSimpleExtern', args)
    return self._exec(action)

  def show_settings(self, args):
    action = Action('showSettings', args)
    return self._exec(action)

  def create_session(self, args):
    action = Action('createSession', args)
    return self._exec(action)

  def terminate_session(self, args):
    action = Action('terminateSession', args)
    return self._exec(action)

  def show_account_order_states(self, args):
    action = Action('showAccountOrderStates', args)
    return self._exec(action)

  def update_account_order_state(self, args):
    action = Action('updateAccountOrderState', args)
    return self._exec(action)

  def show_account_order_automations(self, args):
    action = Action('showAccountOrderAutomations', args)
    return self._exec(action)

  def update_account_order_automation(self, args):
    action = Action('updateAccountOrderAutomation', args)
    return self._exec(action)

  def get_account_status_messages(self, args):
    action = Action('getAccountStatusMessages', args)
    return self._exec(action)

  def get_status_messages(self, args):
    action = Action('getStatusMessages', args)
    return self._exec(action)

  def set_vehicle_config(self, args):
    action = Action('setVehicleConfig', args)
    return self._exec(action)

  def get_vehicle_config(self, args):
    action = Action('getVehicleConfig', args)
    return self._exec(action)

  def set_status_messages(self, args):
    action = Action('setStatusMessages', args)
    return self._exec(action)

  def set_account_status_messages(self, args):
    action = Action('setAccountStatusMessages', args)
    return self._exec(action)

  def show_users(self, args):
    action = Action('showUsers', args)
    return self._exec(action)

  def change_password(self, args):
    action = Action('changePassword', args)
    return self._exec(action)

  def insert_maintenance_schedule(self, args):
    action = Action('insertMaintenanceSchedule', args)
    return self._exec(action)

  def update_maintenance_schedule(self, args):
    action = Action('updateMaintenanceSchedule', args)
    return self._exec(action)

  def delete_maintenance_schedule(self, args):
    action = Action('deleteMaintenanceSchedule', args)
    return self._exec(action)

  def show_maintenance_schedules(self, args):
    action = Action('showMaintenanceSchedules', args)
    return self._exec(action)

  def show_maintenance_tasks(self, args):
    action = Action('showMaintenanceTasks', args)
    return self._exec(action)

  def resolve_maintenance_task(self, args):
    action = Action('resolveMaintenanceTask', args)
    return self._exec(action)

  def get_archived_report_list(self, args):
    action = Action('getArchivedReportList', args)
    return self._exec(action)

  def get_archived_report(self, args):
    action = Action('getArchivedReport', args)
    return self._exec(action)

  def delete_archived_report(self, args):
    action = Action('deleteArchivedReport', args)
    return self._exec(action)

  def get_report_list(self, args):
    action = Action('getReportList', args)
    return self._exec(action)

  def create_report(self, args):
    action = Action('createReport', args)
    return self._exec(action)

  def send_report_via_mail(self, args):
    action = Action('sendReportViaMail', args)
    return self._exec(action)

  def get_areas(self, args):
    action = Action('getAreas', args)
    return self._exec(action)

  def insert_area(self, args):
    action = Action('insertArea', args)
    return self._exec(action)

  def delete_area(self, args):
    action = Action('deleteArea', args)
    return self._exec(action)

  def update_area(self, args):
    action = Action('updateArea', args)
    return self._exec(action)

  def get_area_points(self, args):
    action = Action('getAreaPoints', args)
    return self._exec(action)

  def get_area_assignments(self, args):
    action = Action('getAreaAssignments', args)
    return self._exec(action)

  def insert_area_assignment(self, args):
    action = Action('insertAreaAssignment', args)
    return self._exec(action)

  def delete_area_assignment(self, args):
    action = Action('deleteAreaAssignment', args)
    return self._exec(action)

  def get_area_schedules(self, args):
    action = Action('getAreaSchedules', args)
    return self._exec(action)

  def insert_area_schedule(self, args):
    action = Action('insertAreaSchedule', args)
    return self._exec(action)

  def delete_area_schedule(self, args):
    action = Action('deleteAreaSchedule', args)
    return self._exec(action)

  def send_aux_device_data(self, args):
    action = Action('sendAuxDeviceData', args)
    return self._exec(action)

  def get_local_aux_device_config(self, args):
    action = Action('getLocalAuxDeviceConfig', args)
    return self._exec(action)

  def configure_local_aux_device(self, args):
    action = Action('configureLocalAuxDevice', args)
    return self._exec(action)

  def get_remote_aux_device_config(self, args):
    action = Action('getRemoteAuxDeviceConfig', args)
    return self._exec(action)

  def configure_remote_aux_device(self, args):
    action = Action('configureRemoteAuxDevice', args)
    return self._exec(action)

  def remove_remote_aux_device_config(self, args):
    action = Action('removeRemoteAuxDeviceConfig', args)
    return self._exec(action)

  def clear_aux_device_data_queue(self, args):
    action = Action('clearAuxDeviceDataQueue', args)
    return self._exec(action)

  def reset_aux_device_data(self, args):
    action = Action('resetAuxDeviceData', args)
    return self._exec(action)

  def insert_external_event(self, args):
    action = Action('insertExternalEvent', args)
    return self._exec(action)

  def set_external_object_data(self, args):
    action = Action('setExternalObjectData', args)
    return self._exec(action)
