package evcharging;

simple ChargingStation
{
    gates:
        input evIn;        // For receiving messages from ElectricVehicle (EV)
        input cmsIn;       // For receiving messages from CentralManagementSystem (CMS)
        output out;        // For sending power request to Grid
        output cmpOut;     // For sending messages to CentralManagementSystem (CMS)
        input gridIn; // for connection to Central Management System
}